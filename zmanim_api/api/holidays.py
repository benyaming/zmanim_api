from typing import Tuple, Dict, Union
from datetime import date, timedelta

from pyluach.hebrewcal import HebrewDate, Year

from zmanim_api.api.ou_downloader import get_calendar_data
from zmanim_api.api.utils import get_hebrew_now, get_tz, is_diaspora, formatted_get


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

    # # if yom haatzmaut felt on friday, moove it to thursday
    # if day_1_date == YOM_HAATZMAUT and holiday_date.weekday() == 6:
    #     holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day - 1)

    # # if yom haatzmaut felt on shabbat, moove it to thursday
    # if day_1_date == YOM_HAATZMAUT and holiday_date.weekday() == 7:
    #     holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day - 2)

    # # if yom haatzmaut felt on monday, moove it to tuesday
    # if day_1_date == YOM_HAZIKARON and holiday_date.weekday() == 2:
    #     holiday_date = HebrewDate(holiday_date.year, holiday_month, holiday_day + 1)

    return holiday_date.to_pydate()


async def _get_generic_yomtov_dates(
        day_1_date: Tuple[int, int],
        params: dict,
        is_rosh_hashana: bool = False,
        is_succos: bool = False
) -> dict:
    """

    """
    date_1 = _get_day_1_date(day_1_date)
    date_eve = date_1 - timedelta(1)
    date_2 = date_1 + timedelta(1)
    date_3 = date_1 + timedelta(2)

    data_eve = await _get_calendar_data(_date=date_eve, **params)
    data_1 = await _get_calendar_data(_date=date_1, **params)

    data_2, data_3 = None, None
    diaspora = is_diaspora(get_tz(params['lat'], params['lng']))
    if diaspora or is_rosh_hashana:
        data_2 = await _get_calendar_data(_date=date_2, **params)
    if (diaspora or is_rosh_hashana) and date_2.weekday() == 4:
        data_3 = await _get_calendar_data(_date=date_3, **params)

    eve = {
        'day': date_eve.day,
        'month': date_eve.month
    }
    day_1 = {
        'day': date_1.day,
        'month': date_1.month,
        'weekday': date_1.weekday(),
        'cl': formatted_get(data_eve, CL),
        'havdala': formatted_get(data_1, HAVDALA)
    }

    day_2, day_3 = None, None
    if data_2:
        day_2 = {
            'day': date_2.day,
            'month': date_2.month,
            'weekday': date_2.weekday(),
            'cl': formatted_get(data_1, CL),
            'havdala': formatted_get(data_2, HAVDALA)
        }
    if data_3:
        day_3 = {
            'day': date_3.day,
            'month': date_3.month,
            'weekday': date_3.weekday(),
            'cl': formatted_get(data_2, CL),
            'havdala': formatted_get(data_3, HAVDALA)
        }

    final_data = {
        'year': date_1.year,
        'eve': eve,
        'day_1': day_1,
        'day_2': day_2,
        'day_3': day_3
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
    diaspora = is_diaspora(tz)
    data = await get_calendar_data(
        tz=tz,
        date=_date.strftime(DATE_FORMAT),
        lat=lat,
        lng=lng,
        cl_offset=cl_offset,
        diaspora=diaspora
    )
    return data


async def rosh_hashana(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_dates(ROSH_HASHANA, kwargs, True)
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
            'cl': formatted_get(data_eve, CL),
            'havdala': formatted_get(data_yk, HAVDALA),
        }
    }

    return final_data


async def succos(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_dates(SUCCOS, kwargs, is_succos=True)
    return final_data


async def shmini_atzeres(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_dates(SHMINI_ATZERES, kwargs)
    return final_data


async def pesach(**kwargs) -> dict:
    part_1_data = await _get_generic_yomtov_dates(PESACH, kwargs)
    pesach_7_date = (PESACH[0] + 7, PESACH[1])
    part_2_data = await _get_generic_yomtov_dates(pesach_7_date, kwargs)

    final_data = {
        'year': part_1_data['year'],
        'part_1': {k: v for k, v in part_1_data.items() if k != 'year'},
        'part_2': {k: v for k, v in part_2_data.items() if k != 'year'}
    }
    return final_data


async def shavuos(**kwargs) -> dict:
    final_data = await _get_generic_yomtov_dates(SHAVUOS, kwargs)
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


async def fast(fast_name: str, lat: float, lng: float) -> dict:
    fast_date = _get_day_1_date(FASTS[fast_name])

    fast_data = await _get_calendar_data(lat, lng, fast_date)






# TODO comments. docstrings
