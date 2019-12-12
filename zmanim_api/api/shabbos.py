from datetime import datetime as dt, timedelta

from pytz import timezone

from zmanim_api.helpers import HavdalaChoises
from zmanim_api.api.utils import get_tz, get_translator
from zmanim_api.api.ou_downloader import get_calendar_data
import zmanim_api.api.localized_texts as txt


async def shabbos(
        lang: str,
        lat: float,
        lng: float,
        cl_offset: int,
        havdala: HavdalaChoises
) -> dict:
    """
    Attention! this function returns correct candle lighting time ONLY for current next
    shabbos! If you need to calculate another shabbos, you need co request friday to
    get real candle lighting time.
    # todo test custom shabbos dates
    :param lang:
    :param lat:
    :param lng:
    :param cl_offset:
    :param havdala:
    :return:
    """
    _ = get_translator(lang)

    tz = get_tz(lat, lng)

    tz_time = timezone(tz)
    now = dt.now(tz_time)

    # calculating nearest Saturday
    delta = timedelta(5 - now.weekday() % 7)
    shabbos_date = now + delta
    eve_date = shabbos_date - timedelta(1)

    eve_data = await get_calendar_data(tz, eve_date, lat, lng, cl_offset)
    shabbos_data = await get_calendar_data(tz, shabbos_date, lat, lng)
    parasha = _(txt.shabbos_names[shabbos_data['parsha_shabbos']])

    if not shabbos_data['zmanim']['sunset']:
        final_data = {
            'parasha': parasha,
            'cl': None,
            'cl_offset': None,
            'tzeit_kochavim': None,
            'warning': False,
            'error': True
        }
        return final_data

    warning = True if not shabbos_data['zmanim']['alos_ma'] else False

    final_data = {
        'parasha': parasha,
        'cl': eve_data['zmanim']['cl'],
        'cl_offset': cl_offset,
        'havdala': shabbos_data['zmanim'][havdala.name],
        'havdala_opinion': havdala.value,
        'warning': warning,
        'error': False
    }

    return final_data
