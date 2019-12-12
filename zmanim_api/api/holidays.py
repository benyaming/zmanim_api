from typing import Tuple
from datetime import date, datetime as dt, timedelta

from pyluach.hebrewcal import HebrewDate, Year

from zmanim_api.helpers import HavdalaChoises
from zmanim_api.api.ou_downloader import get_calendar_data
from zmanim_api.api.utils import get_hebrew_now, get_tz, is_diaspora


DATE_FORMAT = '%m/%d/%Y'
CL = 'candle_lighting'
HAVDALA = 'havdala'


ROSH_HASHANA = (1, 7)
YOM_KIPPUR = (10, 7)
SUCCOS = (15, 7)
SHMINI_ATZERES = (22, 7)
CHANNUKAH = (25, 9)
TU_BISHVAT = (15, 11)
PURIM = (14, 12)
PESACH = (15, 1)
YOM_HASHOAH = (27, 1)
YOM_HAZIKARON = (4, 2)
YOM_HAATZMAUT = (5, 2)
LAG_BAOMER = (18, 2)
YOM_YERUSHALAIM = (28, 2)
SHAVUOS = (6, 3)

FASTS = {
    'fast_gedalia': (3, 1),
    'fast_10_teves': (10, 10),
    'fast_esther': (13, 12),
    'fast_17_tammuz': (17, 4),
    'fast_9_av': (9, 5)
}


def _get_day_1_date(day_1_date: Tuple[int, int]) -> date:
    now = get_hebrew_now()
    holiday_day, holiday_month = day_1_date

    holiday_date = HebrewDate(now.year, holiday_month, holiday_day)

    if now > holiday_date:
        holiday_date = HebrewDate(now.year + 1, holiday_month, holiday_day)

    # check if current year is leap, and move to Adat II if need
    if holiday_month == 12 and Year(holiday_date.year).leap:
        holiday_date = HebrewDate(holiday_date.year, holiday_month + 1, holiday_day)

    # if yom hashoa felt on friday, moove it to thursday
    if day_1_date == YOM_HASHOAH and holiday_date.weekday() == 6:
        holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day - 1)

    # if yom hashoa felt on shabbat, moove it to sunday
    if day_1_date == YOM_HASHOAH and holiday_date.weekday() == 7:
        holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day + 1)

    # if yom hazikarom felt on thursday and yom haatzmaut on friday,
    # moove them one day to past
    if (day_1_date == YOM_HAZIKARON and holiday_date.weekday() == 5) or \
            (day_1_date == YOM_HAATZMAUT and holiday_date.weekday() == 6):
        holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day - 1)

    # if yom hazikarom felt on friday and yom haatzmaut on shabbat,
    # moove them two days to past
    if (day_1_date == YOM_HAZIKARON and holiday_date.weekday() == 6) or \
            (day_1_date == YOM_HAATZMAUT and holiday_date.weekday() == 7):
        holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day - 2)

    # if yom hazikarom felt on sunday and yom haatzmaut on monday,
    # moove them one day to future
    if (day_1_date == YOM_HAZIKARON and holiday_date.weekday() == 1) or \
            (day_1_date == YOM_HAZIKARON and holiday_date.weekday() == 2):
        holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day + 1)

    return holiday_date.to_pydate()


async def _get_generic_yomtov_data(
        day_1_date: Tuple[int, int],
        havdala_opinion: HavdalaChoises,
        params: dict,
        is_rosh_hashana: bool = False,
        is_succos: bool = False
) -> dict:
    """

    """
    date_1 = _get_day_1_date(day_1_date)
    date_shabbos = None
    diaspora = is_diaspora(get_tz(params['lat'], params['lng']))

    yt_dates = [date_1]  # Y
    date_eve = date_1 - timedelta(1)

    if diaspora or is_rosh_hashana:  # Y Y
        yt_dates.append(date_1 + timedelta(1))

    if date_1.weekday() == 6:  # S Y Y
        date_eve = date_1 - timedelta(2)
        date_shabbos = date_1 - timedelta(1)
    elif yt_dates[-1].weekday() == 4:  # Y S / Y Y S
        date_shabbos = yt_dates[-1] + timedelta(1)

    # Fetch data from OU #

    data_eve = await _get_calendar_data(_date=date_eve, **params)
    data_1 = await _get_calendar_data(_date=date_1, **params)

    data_2, data_shabbos = None, None
    if len(yt_dates) > 1:
        data_2 = await _get_calendar_data(_date=yt_dates[1], **params)

    if date_shabbos:
        data_shabbos = await _get_calendar_data(_date=date_shabbos, **params)

    eve = {
        'day': date_eve.day,
        'month': date_eve.month
    }
    day_1 = {
        'day': date_1.day,
        'month': date_1.month,
        'weekday': date_1.weekday(),
        'cl': data_eve.get(CL),
        'havdala': data_1.get(HAVDALA)
    }

    day_2, shabbos = None, None
    if data_2:
        day_2 = {
            'day': yt_dates[1].day,
            'month': yt_dates[1].month,
            'weekday': yt_dates[1].weekday(),
            'cl': data_1.get(CL),
            'havdala': data_2.get(HAVDALA)
        }

    yt_datas = [d for d in [data_1, data_2] if d]
    if data_shabbos:
        shabbos = {
            'day': date_shabbos.day,
            'month': date_shabbos.month,
            'weekday': date_shabbos.weekday(),
            'cl': yt_datas[-1].get(CL),
            'havdala': data_shabbos.get(HAVDALA) if date_1.weekday() != 6 else None
        }

    final_data = {
        'year': date_1.year,
        'eve': eve,
        'day_1': day_1,
        'day_2': day_2,
        'shabbos': shabbos
    }

    if is_succos:
        date_hoshana_rabba = date_1 + timedelta(6)
        hoshana_rabba = {
            'day': date_hoshana_rabba.day,
            'month': date_hoshana_rabba.month,
            'weekday': date_hoshana_rabba.weekday()
        }
        final_data['hoshana_rabba'] = hoshana_rabba
    return final_data


async def _get_calendar_data(
        lat: float,
        lng: float,
        _date: date,
        cl_offset: int = 18
) -> dict:
    tz = get_tz(lat, lng)
    data = await get_calendar_data(
        tz=tz,
        date=_date,
        lat=lat,
        lng=lng,
        cl_offset=cl_offset
    )
    return data


async def rosh_hashana(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_data(ROSH_HASHANA, kwargs, True)
    return final_data


async def yom_kippur(lat: float, lng: float, cl_offset: int) -> dict:
    date_yk = _get_day_1_date(YOM_KIPPUR)
    date_eve = date_yk - timedelta(1)

    data_eve = await _get_calendar_data(lat, lng, date_eve, cl_offset=cl_offset)
    data_yk = await _get_calendar_data(lat, lng, date_yk, cl_offset=cl_offset)

    final_data = {
        'eve': {
            'day': date_eve.day,
            'month': date_eve.month
        },
        'day_1': {
            'year': date_yk.year,
            'month': date_yk.month,
            'day': date_yk.day,
            'weekday': date_yk.weekday(),
            'cl': data_eve.get(CL),
            'havdala': data_yk.get(HAVDALA),
        }
    }

    return final_data


async def succos(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_data(SUCCOS, kwargs, is_succos=True)
    return final_data


async def shmini_atzeres(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_data(SHMINI_ATZERES, kwargs)
    return final_data


async def pesach(**kwargs) -> dict:
    part_1_data = await _get_generic_yomtov_data(PESACH, kwargs)
    pesach_7_date = (PESACH[0] + 7, PESACH[1])
    part_2_data = await _get_generic_yomtov_data(pesach_7_date, kwargs)

    final_data = {
        'year': part_1_data['year'],
        'part_1': {k: v for k, v in part_1_data.items() if k != 'year'},
        'part_2': {k: v for k, v in part_2_data.items() if k != 'year'}
    }
    return final_data


async def shavuos(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_data(SHAVUOS, kwargs)
    return final_data


def channukah() -> dict:
    date_start = _get_day_1_date(CHANNUKAH)
    date_end = date_start + timedelta(7)

    final_data = {
        'start_date': {
            'day': date_start.day,
            'month': date_start.month,
            'year': date_start.year,
            'weekday': date_start.weekday()
        },
        'end_date': {
            'day': date_end.day,
            'month': date_end.month,
            'year': date_end.year,
            'weekday': date_end.weekday()
        }
    }
    return final_data


def tu_bishvat() -> dict:
    day = _get_day_1_date(TU_BISHVAT)
    final_data = {
        'day': day.day,
        'month': day.month,
        'year': day.year,
        'weekday': day.weekday()
    }
    return final_data


def purim() -> dict:
    day = _get_day_1_date(PURIM)
    shushan_purim_date = day + timedelta(1)
    final_data = {
        'purim': {
            'day': day.day,
            'month': day.month,
            'year': day.year,
            'weekday': day.weekday()
        },
        'shushan_purim': {
            'day': shushan_purim_date.day,
            'month': shushan_purim_date.month,
            'year': shushan_purim_date.year,
            'weekday': shushan_purim_date.weekday()
        }
    }
    return final_data


def lag_baomer() -> dict:
    day = _get_day_1_date(LAG_BAOMER)
    final_data = {
        'day': day.day,
        'month': day.month,
        'year': day.year,
        'weekday': day.weekday()
    }
    return final_data


def israel_holidays() -> dict:
    yom_hashoa = _get_day_1_date(YOM_HASHOAH)
    yom_hazikaron = _get_day_1_date(YOM_HAZIKARON)
    yom_haatzmaut = _get_day_1_date(YOM_HAATZMAUT)
    yom_yerushalaim = _get_day_1_date(YOM_YERUSHALAIM)

    final_data = {
        'year': yom_hashoa.year,
        'yom_hashoa': {
            'day': yom_hashoa.day,
            'month': yom_hashoa.month,
            'weekday': yom_hashoa.weekday()
        },
        'yom_hazikaron': {
            'day': yom_hazikaron.day,
            'month': yom_hazikaron.month,
            'weekday': yom_hazikaron.weekday()
        },
        'yom_haatzmaut': {
            'day': yom_haatzmaut.day,
            'month': yom_haatzmaut.month,
            'weekday': yom_haatzmaut.weekday()
        },
        'yom_yerushalaim': {
            'day': yom_yerushalaim.day,
            'month': yom_yerushalaim.month,
            'weekday': yom_yerushalaim.weekday()
        },
    }
    return final_data


async def fast(fast_name: str, lat: float, lng: float, havdala: HavdalaChoises) -> dict:
    is_9_av = True if fast_name == 'fast_9_av' else None

    fast_date = _get_day_1_date(FASTS[fast_name])
    # The 9 of Av, instead of other fasts, starts at eve of his date, so we need to
    # calculate additional eve and date
    eve_date = fast_date - timedelta(1)

    fast_data = await _get_calendar_data(lat, lng, fast_date)
    eve_data = await _get_calendar_data(lat, lng, eve_date) if is_9_av else None

    eve, chatzot = None, None
    start_time = fast_data['zmanim'].get('alos_ma')
    if is_9_av:
        eve = {
            'day': eve_date.day,
            'month': eve_date.month,
            'year': eve_date.year,
            'weekday': eve_date.weekday()
        }
        start_time = eve_data['zmanim'].get('sunset')
        chatzot = fast_data['zmanim'].get('chatzos')

    # calculate additional fast end times:
    sunset = dt.strptime(fast_data['zmanim']['sunset'], "%H:%M")
    sba_time = (sunset + timedelta(minutes=31)).strftime("%H:%M")
    nvr_time = (sunset + timedelta(minutes=28)).strftime("%H:%M")
    ssk_time = (sunset + timedelta(minutes=25)).strftime("%H:%M")

    final_data = {
        'fast_name': fast_name,
        'eve': eve,
        'date': {
            'day': fast_date.day,
            'month': fast_date.month,
            'year': fast_date.year,
            'weekday': fast_date.weekday()
            },
        'fast': {
            'start_time': start_time,
            'hatzot': chatzot,
            'havdala': fast_data['zmanim'][havdala.name],
            'havdala_opinion': havdala.value,
            'sba_time': sba_time,
            'nvr_time': nvr_time,
            'ssk_time': ssk_time
        }
    }

    return final_data


# TODO comments. docstrings
# TODO class for calendar_data, zmanim_data
# TODO polar area error for holidays and fasts
