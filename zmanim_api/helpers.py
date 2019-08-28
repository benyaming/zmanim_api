from enum import Enum


class Languages(Enum):
    en = 'en'
    ru = 'ru'


class Fasts(str, Enum):
    fast_gedalia = 'Fast of Gedaliah'
    fast_10_teves = 'Fast of 10 of Teves'
    fast_esther = 'Fast of Esther'
    fast_17_tammuz = 'Fast of 17 of Tammuz'
    fast_9_av = 'Fast of 9 of Av'
