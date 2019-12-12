from typing import Union, Tuple
from gettext import translation as tr
from datetime import datetime as dt, date

from timezonefinder import TimezoneFinder
from pyluach.hebrewcal import HebrewDate, Month

from settings import I18N_DOMAIN


def get_translator(lang: str):
    translator = tr(domain=I18N_DOMAIN, localedir='api/locales', languages=[lang])
    return translator.gettext


def get_tz(lat: float, lng: float) -> str:
    """ Calculates timezone from coordinates """
    tf = TimezoneFinder()
    tz = tf.timezone_at(lng=lng, lat=lat)
    return tz


def is_diaspora(tz) -> bool:
    return False if tz in ['Asia/Tel_Aviv', 'Asia/Jerusalem', 'Asia/Hebron'] else True


def _shift_until_next_month(d: HebrewDate) -> HebrewDate:
    # todo EXPLAIN HOW THIS SHIT WORKS!
    if d.month > (d - 1).month:
        return d
    else:
        return _shift_until_next_month(d + 1)


def get_hebrew_now(custom_date: date = None, rh_mode: bool = False) -> HebrewDate:
    now = custom_date if custom_date else dt.now()
    hebrew_now = HebrewDate.from_pydate(now)

    # rosh hashana is not rosh chodesh
    if rh_mode and hebrew_now.month == 6:
        hebrew_now = _shift_until_next_month(hebrew_now)

    print(hebrew_now)
    return hebrew_now


def calculate_cl(shkia: str) -> str:
    ...


