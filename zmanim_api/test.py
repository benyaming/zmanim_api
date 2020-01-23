from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.util.geo_location import GeoLocation


location = GeoLocation(name='d', latitude=34.837758, longitude=32.090277, time_zone='Asia/Hebron')
calendar = ZmanimCalendar(geo_location=location)

calendar.tzais()

