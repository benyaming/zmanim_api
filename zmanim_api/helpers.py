from enum import Enum


DATE_PATTERN = r'^\d{1,2}\/\d{1,2}\/\d{1,4}$'
TIME_FORMAT = '%H:%M'
DATE_FORMAT = '%d/%m/%Y'
OU_DATE_FORMAT = '%m/%d/%Y'


class LanguageChoises(Enum):
    en = 'en'
    ru = 'ru'


class FastsChoises(str, Enum):
    fast_gedalia = 'Fast of Gedaliah'
    fast_10_teves = 'Fast of 10 of Teves'
    fast_esther = 'Fast of Esther'
    fast_17_tammuz = 'Fast of 17 of Tammuz'
    fast_9_av = 'Fast of 9 of Av'


class HavdalaChoises(str, Enum):
    tzeis_595_degrees = 'Tzeit ha-kochavim 595°'
    tzeis_850_degrees = 'Tzeit ha-kochavim 850°'
    tzeis_42_minutes = 'Tzeit ha-kochavim 42 minutes after shkia'
    tzeis_72_minutes = 'Tzeit ha-kochavim 72 minutes after shkia'
