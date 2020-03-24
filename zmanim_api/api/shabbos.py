from datetime import datetime as dt, timedelta, date as Date

from pytz import timezone
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



    # tz_time = timezone(tz)
    # now = dt.now(tz_time)
    #
    # # calculating nearest Saturday
    # delta = timedelta(5 - now.weekday() % 7)
    # shabbos_date = now + delta
    # eve_date = shabbos_date - timedelta(1)
    #
    # eve_data = await get_calendar_data(tz, eve_date, lat, lng, cl_offset)
    # shabbos_data = await get_calendar_data(tz, shabbos_date, lat, lng)
    # parasha = _(txt.shabbos_names[shabbos_data['parsha_shabbos']])
    #
    # if not shabbos_data['zmanim']['sunset']:
    #     final_data = {
    #         'parasha': parasha,
    #         'cl': None,
    #         'cl_offset': None,
    #         'tzeit_kochavim': None,
    #         'warning': False,
    #         'error': True
    #     }
    #     return final_data
    #
    # warning = True if not shabbos_data['zmanim']['alos_ma'] else False

    final_data = {
        # 'torah_part': '',  # todo
        'cl': friday_calendar.candle_lighting(),
        'cl_offset': cl_offset,
        'havdala': havdala_time,
        'havdala_opinion': havdala.value,
        # 'warning': warning,  # todo
        # 'error': False  # todo
    }

    return final_data
