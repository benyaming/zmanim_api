from datetime import date, timedelta

from timezonefinder import TimezoneFinder


def get_tz(lat: float, lng: float) -> str:
    """ Calculates timezone from coordinates """
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=lng, lat=lat)
    return tz


def is_diaspora(tz: str) -> bool:
    return False if tz in ['Asia/Tel_Aviv', 'Asia/Jerusalem', 'Asia/Hebron'] else True


def get_next_weekday(d: date, weekday: int) -> date:
    current_day = d.weekday()
    res = weekday - current_day
    if res < 0:
        res = 7 + res
    return d + timedelta(days=res)


