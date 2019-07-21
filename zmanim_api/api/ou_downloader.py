from json import loads
from gettext import translation
from datetime import datetime as dt, timedelta

from aiohttp import request
from pytz import timezone

from settings import I18N_DOMAIN
from zmanim_api.api import localized_texts as txt


def get_translator(lang: str):
    translator = translation(domain=I18N_DOMAIN, localedir='api/locales', languages=[lang])
    return translator.gettext


async def _make_calendar_data_request(params: dict) -> dict:
    params['mode'] = 'day'
    calendar_data_url = 'http://db.ou.org/zmanim/getCalendarData.php'
    async with request(method='GET', url=calendar_data_url, params=params) as resp:
        raw_data: dict = loads(await resp.text())
    return raw_data


async def daf_yomi(lang: str, tz: str, date: str, lat: str, lng: str) -> dict:
    _ = get_translator(lang)
    params = {
        'timezone': tz,
        'dateBegin': date,
        'lat': lat,
        'lng': lng
    }
    raw_data = await _make_calendar_data_request(params)
    
    daf_yomi_data = {
        'masehet': _(txt.masehets.get(raw_data['dafYomi']['masechta'])),
        'daf': raw_data['dafYomi']['daf']
    }
    return daf_yomi_data


async def zmanim(lang: str, tz: str, date: str, lat: str, lng: str,
                 settings: dict) -> dict:
    _ = get_translator(lang)
    params = {
        'timezone': tz,
        'dateBegin': date,
        'lat': lat,
        'lng': lng
    }
    raw_data = await _make_calendar_data_request(params)
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


async def shabbos(lang: str, tz: str, lat: str, lng: str, diaspora: bool,
                  cl_offset: str) -> dict:
    _ = get_translator(lang)

    tz_time = timezone(tz)
    now = dt.now(tz_time)

    # calculating nearest Saturday
    delta = timedelta(7 + 5 - now.weekday() % 7)
    shabbos_dt = now + delta

    shabbos_date = f'{shabbos_dt.month}/{shabbos_dt.day}/{shabbos_dt.year}'
    params = {
        'timezone': tz,
        'dateBegin': shabbos_date,
        'lat': lat,
        'lng': lng,
        'candles_offset': cl_offset,
        'israel_holidays': str(diaspora)
    }
    raw_data = await _make_calendar_data_request(params)
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

