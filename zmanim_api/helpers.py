from enum import Enum


class Languages(Enum):
    en = 'en'
    ru = 'ru'


class CLOffset(Enum):
    cl_10 = '10'
    cl_15 = '15'
    cl_18 = '18'
    cl_20 = '20'
    cl_22 = '22'
    cl_30 = '30'
    cl_40 = '40'


class Holidays(str, Enum):
    rosh_hashana = 'Rosh ha-Shana'
    yom_kippur = 'Yom Kippur'
    succos = 'Succos'
    shmini_atzeres = 'Shmini Atzeres/Simchas Tora'
    chanukkah = 'Chanukkah'
    tu_bishvat = 'Tu bi-Shvat'
    purim = 'Purim'
    pesach = 'Pesach'
    lag_baomer = 'Lag ba-Omer'
    shavuos = 'Shavuos'
    yom_haatzmaut = 'Israel Independence day',
    yom_yerushalaim = 'Jerusalem day'
    yom_hashoa = 'Yom ha-Shoa'  # todo translate
    yom_hazikaron = 'Yom ha-Zikaron'  # todo translate

    fast_gedalia = 'Fast of Gedaliah'
    fast_10_teves = 'Fast of 10 of Teves'
    fast_esther = 'Fast of Esther'
    fast_17_tammuz = 'Fast of 17 of Tammuz'
    fast_9_av = 'Fast of 9 of Av'
