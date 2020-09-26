from datetime import datetime as dt, timedelta, date

from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.hebrew_calendar.jewish_calendar import JewishCalendar
from zmanim.limudim.calculators.parsha import Parsha

from ..models import Shabbat, Settings
from ..api_helpers import HavdalaChoices, HAVDALA_PARAMS
from ..utils import get_next_weekday, get_tz, is_diaspora


def get_shabbat(
        # lang: str,
        lat: float,
        lng: float,
        elevation: float,
        cl_offset: int,
        havdala: HavdalaChoices,
        date_: date
) -> Shabbat:
    # _ = get_translator(lang)
    # 1. get friday nearest to the date
    friday = get_next_weekday(date_, 4)
    saturday = friday + timedelta(days=1)

    tz = get_tz(lat, lng)
    location = GeoLocation('', lat, lng, tz, elevation)

    friday_calendar = ZmanimCalendar(candle_lighting_offset=cl_offset, geo_location=location, date=friday)
    saturday_calendar = ZmanimCalendar(candle_lighting_offset=cl_offset, geo_location=location, date=saturday)

    havdala_params = HAVDALA_PARAMS[havdala.name]

    havdala_time: dt = saturday_calendar.tzais(havdala_params)
    late_cl_warning = False if friday_calendar.alos() else True

    jewish_calendar = JewishCalendar(saturday, in_israel=not is_diaspora(tz))
    if jewish_calendar.is_yom_tov_assur_bemelacha() or jewish_calendar.is_chol_hamoed():
        torah_part = jewish_calendar.significant_day()
    else:
        torah_part = Parsha(in_israel=not is_diaspora(tz)).limud(saturday).description()

    data = {
        'torah_part': torah_part,
        'candle_lighting': friday_calendar.candle_lighting().isoformat(timespec='minutes'),
        'cl_offset': cl_offset,
        'havdala': havdala_time.isoformat(timespec='minutes'),
        'havdala_opinion': havdala.value,
        'late_cl_warning': late_cl_warning
    }
    settings = Settings(
        cl_offset=cl_offset,
        havdala_opinion=havdala,
        coordinates=(lat, lng),
        elevation=elevation,
        date=date_
    )

    return Shabbat(settings=settings, **data)
