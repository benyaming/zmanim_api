import zoneinfo
from typing import Optional
from datetime import date, datetime as dt, time, timedelta, datetime

import arrow
from zmanim.util.geo_location import GeoLocation
from zmanim.zmanim_calendar import ZmanimCalendar
from zmanim.hebrew_calendar.jewish_date import JewishDate

from zmanim_api.utils import get_tz, is_diaspora
from zmanim_api.models import ZmanimRequest, ZmanimResponse, Settings, BooleanResp


GEOMETRIC_ZENITH = 90


class ZmanimCalculator:
    zc: ZmanimCalendar
    jewish_date: str

    def __init__(self, lat: float, lng: float, date_: date, elevation: float):
        tz = get_tz(lat, lng)

        jewish_date = JewishDate(date_).jewish_date
        self.jewish_date = f'{jewish_date[0]}-{jewish_date[1]}-{jewish_date[2]}'

        location = GeoLocation('', lat, lng, tz, elevation)
        self.zc = ZmanimCalendar(geo_location=location, date=date_)

    @property
    def sunrise(self) -> Optional[datetime]:
        return self.zc.sunrise()

    @property
    def alos(self) -> Optional[datetime]:
        return self.zc.alos()

    @property
    def sof_zman_tefila_gra(self) -> datetime:
        return self.zc.sof_zman_tfila_gra()

    @property
    def sof_zman_tefila_ma(self) -> Optional[datetime]:
        return self.zc.sof_zman_tfila_mga()

    @property
    def misheyakir_10_2(self) -> Optional[datetime]:
        return self.zc.sunrise_offset_by_degrees(GEOMETRIC_ZENITH + 10.2)

    @property
    def sof_zman_shema_gra(self) -> datetime:
        return self.zc.sof_zman_shma_gra()

    @property
    def sof_zman_shema_ma(self) -> datetime:
        return self.zc.sof_zman_shma_mga()

    @property
    def chatzos(self) -> Optional[datetime]:
        return self.zc.chatzos()

    @property
    def mincha_ketana(self) -> Optional[datetime]:
        return self.zc.mincha_ketana()

    @property
    def mincha_gedola(self) -> Optional[datetime]:
        return self.zc.mincha_gedola()

    @property
    def plag_mincha(self) -> Optional[datetime]:
        return self.zc.plag_hamincha()

    @property
    def sunset(self) -> Optional[datetime]:
        return self.zc.sunset()

    @property
    def tzeis_8_5_degrees(self) -> Optional[datetime]:
        return self.zc.tzais()

    @property
    def tzeis_72_minutes(self) -> Optional[datetime]:
        return self.zc.tzais({'offset': 72})

    @property
    def tzeis_42_minutes(self) -> Optional[datetime]:
        return self.zc.tzais({'offset': 42})

    @property
    def tzeis_5_95_degrees(self) -> Optional[datetime]:
        return self.zc.tzais({'degrees': 5.95})

    @property
    def astronomical_hour_ma(self) -> time:
        return arrow.get(int(self.zc.shaah_zmanis_mga() / 1000)).time()

    @property
    def astronomical_hour_gra(self) -> time:
        return arrow.get(int(self.zc.shaah_zmanis_gra() / 1000)).time()

    @property
    def chatzot_laila(self) -> Optional[datetime]:
        chatzos = self.zc.chatzos()
        return chatzos and chatzos + timedelta(hours=12)


def get_zmanim(
        date_: date,
        lat: float,
        lng: float,
        elevation: float,
        settings: ZmanimRequest
) -> ZmanimResponse:
    zmanim_calc = ZmanimCalculator(lat, lng, date_, elevation)

    zmanim = {}
    for zman_name, is_active in settings.model_dump().items():
        if not is_active:
            continue

        zmanim[zman_name] = getattr(zmanim_calc, zman_name)

    settings = Settings(date=date_, coordinates=(lat, lng), elevation=elevation, jewish_date=zmanim_calc.jewish_date)
    return ZmanimResponse(settings=settings, **zmanim)


def is_asur_bemelaha(
        dt_: dt,
        lat: float,
        lng: float,
        elevation: float
) -> BooleanResp:
    # todo add tzeis option
    tz = get_tz(lat, lng)
    is_israel = not is_diaspora(tz)

    location = GeoLocation('', lat, lng, tz, elevation)
    calendar = ZmanimCalendar(geo_location=location, date=dt_.date())

    dt_ = dt_.astimezone(zoneinfo.ZoneInfo(tz))
    resp = calendar.is_assur_bemelacha(current_time=dt_, in_israel=is_israel)
    return BooleanResp(result=resp)
