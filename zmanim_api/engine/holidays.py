from typing import Optional, Union
from datetime import date, timedelta

from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar


from zmanim_api.utils import get_tz, is_diaspora
from zmanim_api.api_helpers import HAVDALA_PARAMS, HavdalaChoises


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


def _get_first_day_date(name: str, date_: date, diaspora: bool) -> JewishCalendar:
    day, month = HOLYDAYS_AND_FASTS_DATES[name]

    now = JewishCalendar(date_)
    calendar = JewishCalendar.from_jewish_date(now.jewish_year, month, day)

    if calendar < now:
        # in case of long holyday to protect from return next year holiday during current one
        # mooving backward to length of the holiday
        if name in LONG_HOLYDAYS:
            duration = LONG_HOLYDAYS[name][0] if diaspora else LONG_HOLYDAYS[name][1]
            if now.back(duration) < calendar:
                return _get_first_day_date(name, date_ - timedelta(days=duration), diaspora)

        calendar = JewishCalendar.from_jewish_date(calendar.jewish_year + 1, month, day)

    if month == 12 and calendar.is_jewish_leap_year():
        calendar.forward(29)

    # if yom hashoa felt on friday, moove it to thursday
    if name == 'yom_hashoah' and calendar.day_of_week == 6:
        calendar.forward(-1)
    # if first_day_date == YOM_HASHOAH and holiday_date.weekday() == 6:
    #     holiday_date = HebrewDate(holiday_date.year, month, day - 1)

    # if yom hashoa felt on shabbat, moove it to sunday
    if 'yom_hashoah' == (27, 1) and calendar.day_of_week == 7:
        calendar.forward(1)
    # if first_day_date == YOM_HASHOAH and holiday_date.weekday() == 7:
    #     holiday_date = HebrewDate(holiday_date.year, month, day + 1)

    # if yom hazikarom felt on thursday and yom haatzmaut on friday,
    # moove them one day to past
    if (name == 'yom_hazikaron' and calendar.day_of_week == 5) or \
       (name == 'yom_haatzmaut' and calendar.day_of_week == 6):
        calendar.forward(-1)
    # if (first_day_date == YOM_HAZIKARON and holiday_date.weekday() == 5) or \
    #         (first_day_date == YOM_HAATZMAUT and holiday_date.weekday() == 6):
    #     holiday_date = HebrewDate(holiday_date.year, month, day - 1)

    # if yom hazikarom felt on friday and yom haatzmaut on shabbat,
    # moove them two days to past
    if (name == 'yom_hazikaron' and calendar.day_of_week == 6) or \
       (name == 'yom_haatzmaut' and calendar.day_of_week == 7):
        calendar.forward(-2)
    # if (first_day_date == YOM_HAZIKARON and holiday_date.weekday() == 6) or \
    #         (first_day_date == YOM_HAATZMAUT and holiday_date.weekday() == 7):
    #     holiday_date = HebrewDate(holiday_date.year, month, day - 2)

    # if yom hazikarom felt on sunday and yom haatzmaut on monday,
    # moove them one day to future
    if (name == 'yom_hazikaron' and calendar.day_of_week == 1) or \
       (name == 'yom_haatzmaut' and calendar.day_of_week == 2):
        calendar.forward(1)
    # if (first_day_date == YOM_HAZIKARON and holiday_date.weekday() == 1) or \
    #         (first_day_date == YOM_HAZIKARON and holiday_date.weekday() == 2):
    #     holiday_date = HebrewDate(holiday_date.year, month, day + 1)

    return calendar


def fast(
        name: str,
        date_: date,
        lat: Optional[float],
        lng: Optional[float],
        elevation: int,
        havdala_opinion: HavdalaChoises
) -> dict:
    tz = get_tz(lat, lng)
    diaspora = is_diaspora(tz)
    is_9_av = True if name == 'fast_9_av' else None
    havdala_params = HAVDALA_PARAMS[havdala_opinion.name]

    resp = {}

    fast_date = _get_first_day_date(name, date_, diaspora)
    location = GeoLocation('', lat, lng, tz, elevation)
    fast_calc = ZmanimCalendar(geo_location=location, date=fast_date.gregorian_date)
    if is_9_av:
        eve_calc = ZmanimCalendar(geo_location=location, date=(fast_date - 1).gregorian_date)
        resp['fast_start'] = eve_calc.shkia().isoformat(timespec='minutes')
        resp['chatzot'] = fast_calc.chatzos().isoformat(timespec='minutes')
    else:
        if fast_calc.alos():
            resp['fast_start'] = fast_calc.alos().isoformat(timespec='minutes')
        else:
            eve_calc = ZmanimCalendar(geo_location=location, date=(fast_date - 1).gregorian_date)
            resp['fast_start'] = (eve_calc.chatzos() + timedelta(hours=12)).isoformat(timespec='minutes')

    # calculate additional fast ending times:
    sunset = fast_calc.shkia()
    sba_time = (sunset + timedelta(minutes=31)).isoformat(timespec='minutes')
    nvr_time = (sunset + timedelta(minutes=28)).isoformat(timespec='minutes')
    ssk_time = (sunset + timedelta(minutes=25)).isoformat(timespec='minutes')

    resp['fast_end'] = {
        'havdala': fast_calc.tzais(havdala_params).isoformat(timespec='minutes'),
        'sefer_ben_a-shmashot': sba_time,
        'nevareshet': nvr_time,
        'shmirat_shabbat_keilhotah': ssk_time
    }

    return resp


def _regular_holiday(name: str, date_: date, diaspora: bool) -> Union[dict, list]:
    dates = []
    resp = {'holiday': name, 'dates': dates}

    calendar = _get_first_day_date(name, date_, diaspora)
    dates.append(calendar.gregorian_date.isoformat())

    if name == 'chanukah':
        calendar.forward(7)
        dates.append(calendar.gregorian_date.isoformat())

    return resp


def _yom_tov(
        name: str,
        date_: date,
        lat: float,
        lng: float,
        elevation: int,
        diaspora: bool,
        cl: int,
        havdala_opinion: HavdalaChoises
) -> dict:
    """
    There are different holiday dates sets:
    [Y] - one yom tov — Generic yom tov in Israel
    [Y Y] - two yom tovs — Generic yom tov in diaspora
    [Y S] - one yom tov and shabbat
    [S Y Y]
    [Y S]
    [Y Y S]
    """
    day_1_date = _get_first_day_date(name, date_, diaspora)

    shabbat_date = None
    day_2_date = None

    eve_date = day_1_date - 1  # Y

    if (diaspora and not name == 'yom_kippur') or name == 'rosh_hashana':  # Y Y
        day_2_date = day_1_date + 1
        # yt_dates.append(first_day + 1)

    last_yt_date = day_1_date if not day_2_date else day_2_date

    if day_1_date.day_of_week == 1:  # S Y Y
        eve_date = day_1_date - 2
        shabbat_date = day_1_date - 1
    elif last_yt_date.day_of_week == 6:  # Y S / Y Y S
        shabbat_date = last_yt_date + 1

    # checks
    assert eve_date.has_candle_lighting()
    assert day_1_date.is_assur_bemelacha()
    if day_2_date:
        assert day_2_date.is_yom_tov_sheni()
        assert day_2_date.is_assur_bemelacha()

    resp = {
        'eve': {'date': eve_date.gregorian_date.isoformat()},
    }
    if not name == 'pesach_2':
        resp['params'] = {'shkiah_offset': cl, 'havdala_opinion': havdala_opinion.value}

    if shabbat_date and shabbat_date < day_1_date:
        resp['shabbat'] = {'date': shabbat_date.gregorian_date.isoformat()}

    resp['day_1'] = {'date': day_1_date.gregorian_date.isoformat()}

    if day_2_date:
        resp['day_2'] = {'date': day_2_date.gregorian_date.isoformat()}

    if shabbat_date and shabbat_date > last_yt_date:
        resp['shabbat'] = {'date': shabbat_date.gregorian_date.isoformat()}

    if name == 'succot':
        date_hoshana_rabba = day_1_date + 6
        resp['hoshana_rabba'] = date_hoshana_rabba.gregorian_date.isoformat()

    # zmanim calculation
    havdala_params = HAVDALA_PARAMS[havdala_opinion.name]

    tz = get_tz(lat, lng)
    location = GeoLocation('', lat, lng, tz, elevation)

    eve_zmanim_calc = ZmanimCalendar(cl, geo_location=location, date=eve_date.gregorian_date)
    first_day_calc = ZmanimCalendar(cl, geo_location=location, date=day_1_date.gregorian_date)

    if shabbat_date:
        shabbat_eve_date = shabbat_date - 1
        eve_shabbat_calc = ZmanimCalendar(cl, geo_location=location, date=shabbat_eve_date.gregorian_date)
        shabbat_calc = ZmanimCalendar(cl, geo_location=location, date=shabbat_date.gregorian_date)
        resp['shabbat']['candle_lighting'] = eve_shabbat_calc.candle_lighting().isoformat(timespec='minutes')

        if shabbat_date > day_1_date:
            resp['shabbat']['havdala'] = shabbat_calc.tzais(havdala_params).isoformat(timespec='minutes')

    resp['day_1']['candle_lighting'] = eve_zmanim_calc.candle_lighting().isoformat(timespec='minutes')

    if not day_2_date:

        resp['day_1']['havdala'] = first_day_calc.tzais(havdala_params).isoformat(timespec='minutes')
        # return resp
    else:
        second_day_calc = ZmanimCalendar(cl, geo_location=location, date=day_2_date.gregorian_date)
        resp['day_2']['candle_lighting'] = first_day_calc.tzais(havdala_params).isoformat(timespec='minutes')
        if not shabbat_date or shabbat_date < day_2_date:
            resp['day_2']['havdala'] = second_day_calc.tzais(havdala_params).isoformat(timespec='minutes')

    if name == 'pesach':
        params = resp.pop('params')
        part_2 = _yom_tov('pesach_2', date_, lat, lng, elevation, diaspora, cl, havdala_opinion)
        resp = {
            'params': params,
            'part_1': resp,
            'part_2': part_2
        }

    return resp


def holiday(
        name: str,
        date_: date,
        lat: Optional[float],
        lng: Optional[float],
        elevation: int,
        cl: int,
        havdala_opinion: HavdalaChoises
) -> dict:
    diaspora = is_diaspora(get_tz(lat, lng))

    if name in NON_YOM_TOV_HOLYDAYS:
        resp = _regular_holiday(name, date_, diaspora)
    else:
        resp = _yom_tov(
            name=name,
            date_=date_,
            lat=lat,
            lng=lng,
            elevation=elevation,
            diaspora=diaspora,
            cl=cl,
            havdala_opinion=havdala_opinion
        )
    return resp


# r = holiday('yom_kippur', date(2020, 3, 1), 55.35, 37.56, 0, 18, 'tzeis_850_degrees')
# for i in r:
#     print(i, r[i])

# r = fast('fast_gedalia', date(2020, 3, 1), 55.35, 37.56, 0, HavdalaChoises.tzeis_8_5_degrees)
# for i in r:
#     print(i, r[i])
