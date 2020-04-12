from datetime import date as Date, datetime as dt

from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar

from zmanim_api.utils import get_translator, get_tz
from zmanim_api.models import ZmanimSettingsModel


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


def get_zmanim(
        # lang: str,
        date: Date,
        lat: float,
        lng: float,
        elevation: float,
        settings: ZmanimSettingsModel
) -> dict:
    # cl?
    # _ = get_translator(lang)
    tz = get_tz(lat, lng)
    
    location = GeoLocation('', lat, lng, tz, elevation)
    calendar = ZmanimCalendar(geo_location=location, date=date)
    zmanim = _calculate_zmanim(calendar, settings)
    return zmanim

