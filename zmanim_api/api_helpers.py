from enum import Enum
from typing import Optional
from datetime import date


DATE_PATTERN = r'^\d{1,2}\/\d{1,2}\/\d{1,4}$'
DATE_FORMAT = '%d/%m/%Y'


class DateException(Exception):
    ...


class LanguageChoises(Enum):
    en = 'en'
    ru = 'ru'


class HolidayChoises(Enum):
    rosh_hashana = 'Rosh ha-Shana'
    yom_kippur = 'Yom Kippur'
    succot = 'Succot'
    shmini_atzeres = 'Shmini Atzeres/Simchat Tora'
    chanukah = 'Chanukah'
    tu_bi_shvat = 'Tu bi-Shvat'
    purim = 'Purim'
    pesach = 'Pesach'
    lag_baomer = 'Lag ba-Omer'
    shavuot = 'Shavuot'
    tu_be_av = 'Tu be-Av'
    israel_holidays = 'Israeli Holidays'
    yom_hashoah = 'Yom ha-Shoah'
    yom_hazikaron = 'Yom ha-Zikaron'
    yom_haatzmaut = 'Yom ha-Atzmaut'
    yom_yerushalaim = 'Yom Yerushalaim'


class FastsChoises(str, Enum):
    fast_gedalia = 'Fast of Gedaliah'
    fast_10_teves = 'Fast of 10 of Teves'
    fast_esther = 'Fast of Esther'
    fast_17_tammuz = 'Fast of 17 of Tammuz'
    fast_9_av = 'Fast of 9 of Av'


class HavdalaChoises(str, Enum):
    tzeis_5_95_degrees = 'Tzeit ha-kochavim 5.95°'
    tzeis_8_5_degrees = 'Tzeit ha-kochavim 8.5°'
    tzeis_42_minutes = 'Tzeit ha-kochavim 42 minutes after shkia'
    tzeis_72_minutes = 'Tzeit ha-kochavim 72 minutes after shkia'


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
