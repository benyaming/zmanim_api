from enum import Enum
from typing import Optional
from datetime import date, datetime

DATE_PATTERN = r'^\d{1,2}\/\d{1,2}\/\d{1,4}$'
DATE_FORMAT = '%d/%m/%Y'


class DateException(Exception):
    ...


class LanguageChoises(Enum):
    en = 'en'
    ru = 'ru'


class SimpleHolidayChoises(Enum):
    chanukah = 'chanukah'
    tu_bi_shvat = 'tu_bi_shvat'
    purim = 'purim'
    lag_baomer = 'lag_baomer'
    tu_be_av = 'tu_be_av'
    israel_holidays = 'israel_holidays'
    yom_hashoah = 'yom_hashoah'
    yom_hazikaron = 'yom_hazikaron'
    yom_haatzmaut = 'yom_haatzmaut'
    yom_yerushalaim = 'yom_yerushalaim'


class YomTovChoises(Enum):
    rosh_hashana = 'rosh_hashana'
    yom_kippur = 'yom_kippur'
    succot = 'succot'
    shmini_atzeres = 'shmini_atzeres'
    pesach = 'pesach'
    shavuot = 'shavuot'


class FastsChoises(str, Enum):
    fast_gedalia = 'fast_gedalia'
    fast_10_teves = 'fast_10_teves'
    fast_esther = 'fast_esther'
    fast_17_tammuz = 'fast_17_tammuz'
    fast_9_av = 'fast_9_av'


class HavdalaChoises(str, Enum):
    tzeis_5_95_degrees = 'tzeis_5_95_degrees'
    tzeis_8_5_degrees = 'tzeis_8_5_degrees'
    tzeis_42_minutes = 'tzeis_42_minutes'
    tzeis_72_minutes = 'tzeis_72_minutes'


HAVDALA_PARAMS = {
        'tzeis_8_5_degrees': {'degrees': 8.5},
        'tzeis_72_minutes': {'offset': 72},
        'tzeis_42_minutes': {'offset': 42},
        'tzeis_5_95_degrees': {'degrees': 5.95},
}


def validate_date_or_get_now(date_: Optional[str]) -> date:
    if date_:
        try:
            response = date.fromisoformat(date_)
        except ValueError as e:
            raise DateException(e)
    else:
        response = date.today()
    return response


def validate_datetime_or_get_now(dt: Optional[str]) -> datetime:
    if dt:
        try:
            response = datetime.fromisoformat(dt)
        except ValueError as e:
            raise DateException(e)
    else:
        response = datetime.now()
    return response
