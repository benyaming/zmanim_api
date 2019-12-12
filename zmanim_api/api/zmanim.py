from datetime import date as Date

from zmanim_api.api.utils import get_translator, get_tz
from zmanim_api.api.ou_downloader import get_calendar_data
import zmanim_api.api.localized_texts as txt


async def zmanim(lang: str, date: Date, lat: float, lng: float, settings: dict) -> dict:
    # cl?
    _ = get_translator(lang)
    tz = get_tz(lat, lng)

    raw_data = await get_calendar_data(tz, date, lat, lng)
    zmanim_data: dict = raw_data['zmanim']

    # select only needed zmanim
    zmanim_data = {k: v for k, v in zmanim_data.items() if settings[k]}

    # translate zmanim
    zmanim_data = {_(txt.zmanim_names[k]): v for k, v in zmanim_data.items()}

    return zmanim_data
