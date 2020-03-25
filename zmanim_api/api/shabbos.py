from datetime import datetime as dt, timedelta, date as Date

from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar


from zmanim_api.helpers import HavdalaChoises
from .utils import get_next_weekday, get_tz


async def shabbos(
        # lang: str,
        lat: float,
        lng: float,
        elevation: float,
        cl_offset: int,
        havdala: HavdalaChoises,
        date: Date
) -> dict:
    # _ = get_translator(lang)
    # 1. get friday nearest to the date
    friday = get_next_weekday(date, 4)
    saturday = friday + timedelta(days=1)

    tz = get_tz(lat, lng)
    location = GeoLocation('', lat, lng, tz, elevation)
    friday_calendar = ZmanimCalendar(candle_lighting_offset=cl_offset, geo_location=location, date=friday)
    saturday_calendar = ZmanimCalendar(candle_lighting_offset=cl_offset, geo_location=location, date=saturday)

    havdala_calculators = {
        'tzeis_850_degrees': ('tzais', {'degrees': 8.5}),
        'tzeis_72_minutes': ('tzais', {'offset': 72}),
        'tzeis_42_minutes': ('tzais', {'offset': 42}),
        'tzeis_595_degrees': ('tzais', {'degrees': 5.95}),
    }
    havdala_calculator, kwargs = havdala_calculators[havdala.name]

    havdala_time: dt = getattr(saturday_calendar, havdala_calculator)(kwargs)
    late_cl_warning = False if friday_calendar.alos() else True

    final_data = {
        'torah_part': '',  # todo
        'cl': friday_calendar.candle_lighting(),
        'cl_offset': cl_offset,
        'havdala': havdala_time,
        'havdala_opinion': havdala.value,
        'late_cl_warning': late_cl_warning
    }

    return final_data
