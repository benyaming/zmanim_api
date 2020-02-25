# noinspection PyPep8Naming
from datetime import date as Date

import zmanim_api.api.localized_texts as txt
from zmanim_api.api.utils import get_tz, get_translator
from zmanim_api.api.ou_downloader import get_calendar_data


async def get_daf_yomi(lang: str, date: Date, lat: float, lng: float) -> dict:
    _ = get_translator(lang)
    tz = get_tz(lat, lng)
    raw_data = await get_calendar_data(tz, date, lat, lng)

    daf_yomi_data = {
        'masehet': _(txt.masehets.get(raw_data['dafYomi']['masechta'])),
        'daf': raw_data['dafYomi']['daf']
    }
    return daf_yomi_data
