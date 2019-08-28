from json import loads
from gettext import translation as tr
from datetime import datetime as dt, timedelta

from aiohttp import request
from pytz import timezone

from settings import I18N_DOMAIN
from zmanim_api.api import localized_texts as txt
from zmanim_api.api.utils import get_tz, is_diaspora


def get_translator(lang: str):
    translator = tr(domain=I18N_DOMAIN, localedir='api/locales', languages=[lang])
    return translator.gettext


async def get_calendar_data(tz: str, date: str, lat: float, lng: float,
                            cl_offset: int = 18, diaspora: bool = True) -> dict:
    # todo kwargs
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': date,
        'lat': str(lat),
        'lng': str(lng),
        'candles_offset': str(cl_offset)
    }
    if not diaspora:
        params['israel_holidays'] = str(not diaspora)

    calendar_data_url = 'http://db.ou.org/zmanim/getCalendarData.php'
    async with request(method='GET', url=calendar_data_url, params=params) as resp:
        raw_data: dict = loads(await resp.text())
    return raw_data


async def daf_yomi(lang: str, date: str, lat: float, lng: float) -> dict:
    _ = get_translator(lang)
    tz = get_tz(lat, lng)
    raw_data = await get_calendar_data(tz, date, lat, lng)

    daf_yomi_data = {
        'masehet': _(txt.masehets.get(raw_data['dafYomi']['masechta'])),
        'daf': raw_data['dafYomi']['daf']
    }
    return daf_yomi_data


async def zmanim(lang: str, date: str, lat: float, lng: float, settings: dict) -> dict:
    _ = get_translator(lang)
    tz = get_tz(lat, lng)

    raw_data = await get_calendar_data(tz, date, lat, lng)
    zmanim_raw: dict = raw_data['zmanim']

    # delete ou's 'X:XX:XX' from results
    zmanim_data = {k: v for k, v in zmanim_raw.items() if v != 'X:XX:XX'}

    # calculate and append astronomical hour of Magen Avraham, if it possible:
    time_format = '%H:%M:%S'
    if 'sof_zman_shema_ma' in zmanim_data and 'sof_zman_tefila_ma' in zmanim_data:
        begin = dt.strptime(zmanim_data['sof_zman_shema_ma'], time_format)
        end = dt.strptime(zmanim_data['sof_zman_tefila_ma'], time_format)
        hour_ma = str(end - begin)
        zmanim_data['astronomical_hour_ma'] = hour_ma

    # calculate and append astronomical hour of GRA
    gra_hour_begin = dt.strptime(zmanim_data['sof_zman_shema_gra'], time_format)
    gra_hour_end = dt.strptime(zmanim_data['sof_zman_tefila_gra'], time_format)
    hour_gra = str(gra_hour_end - gra_hour_begin)
    zmanim_data['astronomical_hour_gra'] = hour_gra

    # calculate and append midnight time
    chatzot = dt.strptime(zmanim_data['chatzos'], time_format)
    chatzot_laila = str(dt.time(chatzot + timedelta(hours=12)))
    zmanim_data['chatzot_laila'] = chatzot_laila

    # select only needed zmanim
    zmanim_data = {k: v for k, v in zmanim_data.items() if settings[k]}

    # translate zmanim
    zmanim_data = {_(txt.zmanim_names[k]): v[:-3] for k, v in zmanim_data.items()}

    return zmanim_data


async def shabbos(lang: str, lat: float, lng: float, cl_offset: int) -> dict:
    _ = get_translator(lang)

    tz = get_tz(lat, lng)
    diaspora = is_diaspora(tz)
    tz_time = timezone(tz)
    now = dt.now(tz_time)

    # calculating nearest Saturday
    delta = timedelta(7 + 5 - now.weekday() % 7)
    shabbos_dt = now + delta

    shabbos_date = f'{shabbos_dt.month}/{shabbos_dt.day}/{shabbos_dt.year}'

    raw_data = await get_calendar_data(tz, shabbos_date, lat, lng, cl_offset, diaspora)
    parasha = _(txt.shabbos_names[raw_data['parsha_shabbos']])

    if raw_data['zmanim']['sunset'] == 'X:XX:XX':
        shabbos_data = {
            'parasha': parasha,
            'cl': None,
            'cl_offset': None,
            'tzeit_kochavim': None,
            'warning': False,
            'error': True
        }
        return shabbos_data

    if raw_data['zmanim']['tzeis_850_degrees'] == 'X:XX:XX':
        # calculating midnight by adding 12 hours to midday
        chazot_time = dt.strptime(raw_data['zmanim']['chatzos'], "%H:%M:%S")
        chazot_laila = str(dt.time(chazot_time + timedelta(hours=12)))
        raw_data['zmanim']['tzeis_850_degrees'] = chazot_laila

    warning = True if raw_data['zmanim']['alos_ma'] == 'X:XX:XX' else False

    shabbos_data = {
        'parasha': parasha,
        'cl': raw_data['candle_lighting_shabbos'][:-3],
        'cl_offset': cl_offset,
        'tzeit_kochavim': raw_data['zmanim']['tzeis_850_degrees'][:-3],
        'warning': warning,
        'error': False
    }

    return shabbos_data
