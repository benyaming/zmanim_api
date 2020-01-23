from json import loads
from typing import Optional
from dataclasses import dataclass
from datetime import datetime as dt, date as Date, timedelta

from aiohttp import request

from zmanim_api.api.utils import is_diaspora
from zmanim_api.helpers import OU_DATE_FORMAT, TIME_FORMAT


async def get_calendar_data(tz: str, date: Date, lat: float, lng: float,
                            cl_offset: int = None) -> dict:
    # todo kwargs
    diaspora = is_diaspora(tz)

    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': date.strftime(OU_DATE_FORMAT),
        'lat': str(lat),
        'lng': str(lng)
    }
    if not diaspora:
        params['israel_holidays'] = str(not diaspora)

    calendar_data_url = 'http://db.ou.org/zmanim/getCalendarData.php'
    async with request(method='GET', url=calendar_data_url, params=params) as resp:
        raw_data: dict = loads(await resp.text())
        zmanim = _clean_ou_zmanim(raw_data['zmanim'], cl_offset=cl_offset)

    return raw_data


def _clean_ou_zmanim(zmanim_dict: dict, cl_offset: int = None) -> dict:
    """
    Fix and replace all `XX:XX` to `None` or calculate them, if it possible;
    Calculate additional opinions (Magen Avraham and more);
    Calculate candle lighting (cl)
    Format all timings from hh:mm:ss to hh:mm
    :param zmanim_dict: A dictionary that OU returned
    :param cl_offset: number of minutes before shkia
    """

    # remove seconds and :XX from timings:
    zmanim_dict = {k: v[:-3] for k, v in zmanim_dict.items()}

    # replace ou's 'X:XX:XX' by pythonic None
    keys = [key for key in zmanim_dict.keys() if zmanim_dict[key] == 'X:XX']
    for key in keys:
        zmanim_dict[key] = None

    # trying to fix tzeit hakochavim if need by adding 12 hours to midnight
    if not zmanim_dict['tzeis_850_degrees']:
        chatzot = dt.strptime(zmanim_dict['chatzos'], TIME_FORMAT)
        zmanim_dict['tzeis_850_degress'] = str(dt.time(chatzot + timedelta(hours=12)))

    # calculate and append astronomical hour of Magen Avraham, if it possible:
    if zmanim_dict['sof_zman_shema_ma'] and zmanim_dict['sof_zman_tefila_ma']:
        begin = dt.strptime(zmanim_dict['sof_zman_shema_ma'], TIME_FORMAT)
        end = dt.strptime(zmanim_dict['sof_zman_tefila_ma'], TIME_FORMAT)
        print(begin, end)
        zmanim_dict['astronomical_hour_ma'] = str(end - begin)[:-3]

    # calculate and append astronomical hour of GRA
    gra_hour_begin = dt.strptime(zmanim_dict['sof_zman_shema_gra'], TIME_FORMAT)
    gra_hour_end = dt.strptime(zmanim_dict['sof_zman_tefila_gra'], TIME_FORMAT)
    zmanim_dict['astronomical_hour_gra'] = str(gra_hour_end - gra_hour_begin)[:-3]

    # calculate and append midnight time
    chatzot = dt.strptime(zmanim_dict['chatzos'], TIME_FORMAT)
    chatzot_laila = str(dt.time(chatzot + timedelta(hours=12)))[:-3]
    zmanim_dict['chatzot_laila'] = chatzot_laila

    # calculate candle lighting
    if cl_offset:
        shkia = dt.strptime(zmanim_dict['sunset'], TIME_FORMAT)
        cl = (dt.time(shkia - timedelta(minutes=cl_offset))).strftime(TIME_FORMAT)
        zmanim_dict['cl'] = cl

    return zmanim_dict
