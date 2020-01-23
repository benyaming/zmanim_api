from datetime import date as Date, datetime as dt
from typing import TypedDict

from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar

from zmanim_api.api.utils import get_translator, get_tz
from zmanim_api.api.ou_downloader import get_calendar_data
from zmanim_api.models import ZmanimSettingsModel
import zmanim_api.api.localized_texts as txt


_ZMANIM_CALCULATORS = {
    'sunrise': 'sunrise',
    'alos': 'alos',
    'sof_zman_tefila_gra': 'sof_zman_tfila_gra',
    'sof_zman_tefila_ma': 'sof_zman_tfila_mga',
    'talis_ma': '',
    'sof_zman_shema_gra': 'sof_zman_shma_gra',
    'sof_zman_shema_ma': 'sof_zman_shma_mga',
    'chatzos': 'chatzos',
    'mincha_ketana': 'mincha_ketana',
    'mincha_gedola': 'mincha_gedola',
    'plag_mincha': 'plag_hamincha',
    'sunset': 'sunset',
    'tzeis_850_degrees': 'tzais',
    'tzeis_72_minutes': ('tzais', {'offset': 72}),
    'tzeis_42_minutes': ('tzais', {'offset': 42}),
    'tzeis_595_degrees': ('tzais', {'degrees': 5.95}),
    'astronomical_hour_ma': 'shaah_zmanis_mga',
    'astronomical_hour_gra': 'shaah_zmanis_gra',
}


def _calculate_zmanim(calendar: ZmanimCalendar, settings: ZmanimSettingsModel) -> ...:
    calculated_zmanim = {}
    for zman_name, required in settings.dict().items():
        if not required:
            continue
        method_name = _ZMANIM_CALCULATORS.get(zman_name)
        if not method_name:
            continue
        
        if isinstance(method_name, tuple):
            method_name, kwargs = method_name
            zman_value: dt = getattr(calendar, method_name)(kwargs)
        else:
            zman_value: dt = getattr(calendar, method_name)()

        if isinstance(zman_value, dt):
            calculated_zmanim[zman_name] = zman_value.strftime('%H:%M')
        else:
            calculated_zmanim[zman_name] = zman_value

    return calculated_zmanim


async def get_zmanim(
        lang: str,
        date: Date,
        lat: float,
        lng: float,
        elevation: float,
        settings: ZmanimSettingsModel
) -> dict:
    # cl?
    _ = get_translator(lang)
    tz = get_tz(lat, lng)
    
    location = GeoLocation('', lat, lng, tz, elevation)
    calendar = ZmanimCalendar(geo_location=location, date=date)
    zmanim = _calculate_zmanim(calendar, settings)
    return zmanim

    raw_data = await get_calendar_data(tz, date, lat, lng)
    zmanim_data: dict = raw_data['zmanim']

    # select only needed zmanim
    zmanim_data = {k: v for k, v in zmanim_data.items() if settings[k]}

    # translate zmanim
    zmanim_data = {_(txt.zmanim_names[k]): v for k, v in zmanim_data.items()}

    return zmanim_data
