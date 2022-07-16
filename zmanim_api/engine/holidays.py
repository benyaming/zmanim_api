from typing import Optional, Tuple
from datetime import date, timedelta

from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar

from ..utils import get_tz, is_diaspora
from ..api_helpers import HAVDALA_PARAMS, HavdalaChoices
from ..models import Holiday, YomTov, Fast, SimpleSettings, Settings


HOLYDAYS_AND_FASTS_DATES = {
    'rosh_hashana': (1, 7),
    'yom_kippur': (10, 7),
    'succot': (15, 7),
    'shmini_atzeres': (22, 7),
    'chanukah': (25, 9),
    'tu_bi_shvat': (15, 11),
    'purim': (14, 12),
    'pesach': (15, 1),
    'pesach_2': (21, 1),
    'yom_hashoah': (27, 1),
    'yom_hazikaron': (4, 2),
    'yom_haatzmaut': (5, 2),
    'lag_baomer': (18, 2),
    'yom_yerushalaim': (28, 2),
    'shavuot': (6, 3),
    'tu_be_av': (15, 5),
    'fast_gedalia': (3, 7),
    'fast_10_teves': (10, 10),
    'fast_esther': (13, 12),
    'fast_17_tammuz': (17, 4),
    'fast_9_av': (9, 5)
}

NON_YOM_TOV_HOLYDAYS = (
    'chanukah',
    'tu_bi_shvat',
    'purim',
    'lag_baomer',
    'tu_be_av',
    'yom_hashoah',
    'yom_hazikaron',
    'yom_haatzmaut',
    'yom_yerushalaim'
)

LONG_HOLYDAYS = {
    # {name: (length in diaspora, length in israel)}
    'rosh_hashana': (2, 2),
    'succot': (7, 6),
    'shmini_atzeres': (2, 1),
    'chanukah': (8, 8),
    'pesach': (9, 8),
    'shavuot': (2, 1)
}

MOOVABLE_DAYS = {
    'fast_17_tammuz',
    'fast_9_av',
    'fast_gedalia'
}


def _get_first_day_date(name: str, date_: date, diaspora: bool = True) -> JewishCalendar:
    day, month = HOLYDAYS_AND_FASTS_DATES[name]

    now = JewishCalendar(date_)

    if now.is_jewish_leap_year() and month == 12:
        month = 13

    first_day_date = JewishCalendar.from_jewish_date(now.jewish_year, month, day)

    if first_day_date < now:
        # in case of long holyday to protect from return next year holiday during current one
        # mooving backward to length of the holiday
        if name in LONG_HOLYDAYS:
            duration = LONG_HOLYDAYS[name][0] if diaspora else LONG_HOLYDAYS[name][1]
            if now.back(duration) < first_day_date:
                return _get_first_day_date(name, date_ - timedelta(days=duration), diaspora)

        first_day_date = JewishCalendar.from_jewish_date(first_day_date.jewish_year + 1, month, day)

    if month == 12 and first_day_date.is_jewish_leap_year():
        first_day_date.forward(30)

    # if yom hashoa felt on Friday, moove it to Thursday
    if name == 'yom_hashoah' and first_day_date.day_of_week == 6:
        first_day_date.forward(-1)

    # if yom hashoa felt on Sunday, moove it to Monday
    if name == 'yom_hashoah' and first_day_date.day_of_week == 1:
        first_day_date.forward(1)

    # if yom hazikarom felt on thursday and yom haatzmaut on friday,
    # moove them one day to past
    if (name == 'yom_hazikaron' and first_day_date.day_of_week == 5) or \
       (name == 'yom_haatzmaut' and first_day_date.day_of_week == 6):
        first_day_date.forward(-1)

    # if yom hazikarom felt on friday and yom haatzmaut on shabbat,
    # moove them two days to past
    if (name == 'yom_hazikaron' and first_day_date.day_of_week == 6) or \
       (name == 'yom_haatzmaut' and first_day_date.day_of_week == 7):
        first_day_date.forward(-2)

    # if yom hazikarom felt on sunday and yom haatzmaut on monday,
    # moove them one day to future
    if (name == 'yom_hazikaron' and first_day_date.day_of_week == 1) or \
       (name == 'yom_haatzmaut' and first_day_date.day_of_week == 2):
        first_day_date.forward(1)

    return first_day_date


def fast(
        name: str,
        date_: date,
        lat: Optional[float],
        lng: Optional[float],
        elevation: int,
) -> Fast:
    tz = get_tz(lat, lng)
    diaspora = is_diaspora(tz)
    is_9_av = True if name == 'fast_9_av' else None

    data = {'moved_fast': False}

    fast_date = _get_first_day_date(name, date_, diaspora)
    if name in MOOVABLE_DAYS:
        if fast_date.gregorian_date.weekday() == 5:
            # Deferred fast in the future
            fast_date.forward(1)
            data['moved_fast'] = True
        elif date_.year != fast_date.gregorian_year:
            # Probably today is deferred fast
            previous_day = _get_first_day_date(name, date_ - timedelta(days=1), diaspora)
            if date_.year == previous_day.gregorian_year and previous_day.gregorian_date.weekday() == 5:
                fast_date = previous_day

    # Deferred fasts
    if name in ('fast_gedalia', 'fast_17_tammuz', 'fast_9_av') and fast_date.day_of_week == 7:
        fast_date.forward(1)
        data['moved_fast'] = True
    if name == 'fast_esther' and fast_date.day_of_week == 7:
        fast_date.forward(-2)
        data['moved_fast'] = True

    location = GeoLocation('', lat, lng, tz, elevation)
    fast_calc = ZmanimCalendar(geo_location=location, date=fast_date.gregorian_date)
    if is_9_av:
        eve_calc = ZmanimCalendar(geo_location=location, date=(fast_date - 1).gregorian_date)
        data['fast_start'] = eve_calc.shkia()
        data['chatzot'] = fast_calc.chatzos()
    else:
        if fast_calc.alos():
            data['fast_start'] = fast_calc.alos()
        else:
            eve_calc = ZmanimCalendar(geo_location=location, date=(fast_date - 1).gregorian_date)
            data['fast_start'] = eve_calc.chatzos() + timedelta(hours=12)

    # calculate additional fast ending times:
    # sunset = fast_calc.shkia()
    # sba_time = (sunset + timedelta(minutes=31))
    # nvr_time = (sunset + timedelta(minutes=28))
    # ssk_time = (sunset + timedelta(minutes=25))

    data['havdala_8_5_dgr'] = fast_calc.tzais({'degrees': 8.5})
    data['havdala_5_95_dgr'] = fast_calc.tzais({'degrees': 5.95})
    data['havdala_42_min'] = fast_calc.sunset() + timedelta(minutes=42)

    settings = Settings(
        coordinates=(lat, lng),
        elevation=elevation,
        date=date_,
        fast_name=name
    )

    return Fast(settings=settings, **data)


def get_simple_holiday(name: str, date_: date) -> Holiday:
    holiday_date = _get_first_day_date(name, date_).gregorian_date
    data = {'holiday': name, 'date': holiday_date}

    settings = SimpleSettings(date=date_, holiday_name=name)
    return Holiday(settings=settings, **data)


def get_yom_tov(
        name: str,
        date_: date,
        lat: float,
        lng: float,
        elevation: int,
        cl: int,
        havdala_opinion: HavdalaChoices
) -> YomTov:
    """
    There are different holiday dates sets:
    [Y] - one yom tov — Generic yom tov in Israel
    [Y Y] - two yom tovs — Generic yom tov in diaspora
    [Y S] - one yom tov and shabbat
    [S Y Y]
    [Y S]
    [Y Y S]
    """
    tz = get_tz(lat, lng)
    diaspora = is_diaspora(tz)
    day_1_date = _get_first_day_date(name, date_, diaspora)

    shabbat_date = None
    day_2_date = None

    eve_date = day_1_date - 1  # Y

    if (diaspora and not name == 'yom_kippur') or name == 'rosh_hashana':  # Y Y
        day_2_date = day_1_date + 1

    last_yt_date = day_2_date or day_1_date

    if day_1_date.day_of_week == 1:  # S Y Y
        shabbat_date = day_1_date - 1
    elif last_yt_date.day_of_week == 6:  # Y S / Y Y S
        shabbat_date = last_yt_date + 1

    # checks
    assert eve_date.has_candle_lighting()
    assert day_1_date.is_assur_bemelacha()
    if day_2_date:
        assert day_2_date.is_yom_tov_sheni()
        assert day_2_date.is_assur_bemelacha()

    data = {}
    shabbat_term = None

    if shabbat_date and shabbat_date < day_1_date:
        shabbat_term = 'pre_shabbat'
        data[shabbat_term] = {'date': shabbat_date.gregorian_date}

    data['day_1'] = {'date': day_1_date.gregorian_date}

    if day_2_date:
        data['day_2'] = {'date': day_2_date.gregorian_date}

    if shabbat_date and shabbat_date > last_yt_date:
        shabbat_term = 'post_shabbat'
        data[shabbat_term] = {'date': shabbat_date.gregorian_date}

    if name == 'succot':
        date_hoshana_rabba = day_1_date + 6
        data['hoshana_rabba'] = date_hoshana_rabba.gregorian_date

    # zmanim calculation
    havdala_params = HAVDALA_PARAMS[havdala_opinion.name]

    location = GeoLocation('', lat, lng, tz, elevation)

    eve_zmanim_calc = ZmanimCalendar(cl, geo_location=location, date=eve_date.gregorian_date)
    first_day_calc = ZmanimCalendar(cl, geo_location=location, date=day_1_date.gregorian_date)

    if shabbat_date:
        shabbat_eve_date = shabbat_date - 1
        eve_shabbat_calc = ZmanimCalendar(cl, geo_location=location, date=shabbat_eve_date.gregorian_date)
        shabbat_calc = ZmanimCalendar(cl, geo_location=location, date=shabbat_date.gregorian_date)
        data[shabbat_term]['candle_lighting'] = eve_shabbat_calc.candle_lighting()

        if shabbat_date > day_1_date:
            data[shabbat_term]['havdala'] = shabbat_calc.tzais(havdala_params)

    if shabbat_term == 'pre_shabbat':
        data['day_1']['candle_lighting'] = eve_zmanim_calc.tzais(havdala_params)
    else:
        data['day_1']['candle_lighting'] = eve_zmanim_calc.candle_lighting()

    if not day_2_date:
        if not shabbat_term or shabbat_term == 'pre_shabbat':
            data['day_1']['havdala'] = first_day_calc.tzais(havdala_params)

    else:
        second_day_calc = ZmanimCalendar(cl, geo_location=location, date=day_2_date.gregorian_date)
        if day_1_date.gregorian_date.weekday() == 4:
            data['day_2']['candle_lighting'] = first_day_calc.candle_lighting()
        else:
            data['day_2']['candle_lighting'] = first_day_calc.tzais(havdala_params)
        # data['day_2']['candle_lighting'] = smart_candle_lighting(day_2_date, second_day_calc)
        if not shabbat_date or shabbat_date < day_2_date:
            data['day_2']['havdala'] = second_day_calc.tzais(havdala_params)

    part_2_data = {}
    if name == 'pesach':
        part_2 = get_yom_tov('pesach_2', date_, lat, lng, elevation, cl, havdala_opinion)
        part_2_data = {
            'pesach_part_2_day_1': part_2.day_1,
            'pesach_part_2_day_2': part_2.day_2,
            'pesach_part_2_post_shabat': part_2.pesach_part_2_post_shabat
        }

        data['pesach_eating_chanetz_till'] = eve_zmanim_calc._shaos_into_day(
            eve_zmanim_calc.elevation_adjusted_sunrise(),
            eve_zmanim_calc.elevation_adjusted_sunset(),
            4
        )
        data['pesach_burning_chanetz_till'] = eve_zmanim_calc._shaos_into_day(
            eve_zmanim_calc.elevation_adjusted_sunrise(),
            eve_zmanim_calc.elevation_adjusted_sunset(),
            5
        )

    if name == 'pesach_2' and shabbat_term in data:
        data['pesach_part_2_post_shabat'] = data.pop(shabbat_term)

    settings = Settings(
        cl_offset=cl,
        havdala_opinion=havdala_opinion,
        coordinates=(lat, lng),
        elevation=elevation,
        date=date_,
        yomtov_name=name
    )
    return YomTov(settings=settings, **data, **part_2_data)
