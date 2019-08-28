from typing import Union, Tuple
from datetime import datetime as dt

from timezonefinder import TimezoneFinder
from pyluach.hebrewcal import HebrewDate


def get_tz(lat: float, lng: float) -> str:
    """ Calculates timezone from coordinates """
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=lng, lat=lat)
    return tz


def is_diaspora(tz) -> bool:
    return False if tz in ['Asia/Tel_Aviv', 'Asia/Jerusalem', 'Asia/Hebron'] else True


def get_hebrew_now() -> HebrewDate:
    hebrew_now = HebrewDate.from_pydate(dt.now())
    return hebrew_now


def formatted_get(d: dict, key: str) -> Union[str, None]:
    """ Return `11:11` instead `11:11:11` if key in dict """
    value = d.get(key)
    if value:
        value = value[:-3]
    return value




