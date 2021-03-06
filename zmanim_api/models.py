from __future__ import annotations
from datetime import datetime, time, date
from typing import List, Optional, Tuple
from pydantic import BaseModel


class SimpleSettings(BaseModel):
    date_: Optional[date] = None
    jewish_date: Optional[str] = None
    holiday_name: Optional[str] = None

    class Config:
        fields = {'date_': 'date'}


class Settings(SimpleSettings):
    cl_offset: Optional[int] = None
    havdala_opinion: Optional[str] = None
    coordinates: Optional[Tuple[float, float]] = None
    elevation: Optional[int] = None
    fast_name: Optional[str] = None
    yomtov_name: Optional[str] = None


class ZmanimRequest(BaseModel):
    sunrise: bool = True
    alos: bool = True
    sof_zman_tefila_gra: bool = True
    sof_zman_tefila_ma: bool = True
    misheyakir_10_2: bool = True
    sof_zman_shema_gra: bool = True
    sof_zman_shema_ma: bool = True
    chatzos: bool = True
    mincha_ketana: bool = True
    mincha_gedola: bool = True
    plag_mincha: bool = True
    sunset: bool = True
    tzeis_8_5_degrees: bool = True
    tzeis_72_minutes: bool = True
    tzeis_42_minutes: bool = True
    tzeis_5_95_degrees: bool = True
    chatzot_laila: bool = True
    astronomical_hour_ma: bool = True
    astronomical_hour_gra: bool = True


class ZmanimResponse(BaseModel):
    settings: Settings
    alos: Optional[datetime] = None
    sunrise: Optional[datetime] = None
    misheyakir_10_2: Optional[datetime] = None
    sof_zman_shema_ma: Optional[datetime] = None
    sof_zman_shema_gra: Optional[datetime] = None
    sof_zman_tefila_ma: Optional[datetime] = None
    sof_zman_tefila_gra: Optional[datetime] = None
    chatzos: Optional[datetime] = None
    mincha_gedola: Optional[datetime] = None
    mincha_ketana: Optional[datetime] = None
    plag_mincha: Optional[datetime] = None
    sunset: Optional[datetime] = None
    tzeis_5_95_degrees: Optional[datetime] = None
    tzeis_8_5_degrees: Optional[datetime] = None
    tzeis_42_minutes: Optional[datetime] = None
    tzeis_72_minutes: Optional[datetime] = None
    chatzot_laila: Optional[datetime] = None
    astronomical_hour_ma: Optional[time] = None
    astronomical_hour_gra: Optional[time] = None


class AsurBeMelachaDay(BaseModel):
    date: Optional[date] = None
    candle_lighting: Optional[datetime] = None
    havdala: Optional[datetime] = None


class Shabbat(AsurBeMelachaDay):
    settings: Settings
    torah_part: str = None
    late_cl_warning: bool = False


class RoshChodesh(BaseModel):
    settings: SimpleSettings
    month_name: str
    days: List[date]
    duration: int
    molad: Tuple[datetime, int]

    class Config:
        json_encoders = {
            datetime: lambda d: d.isoformat(timespec='minutes')
        }


class DafYomi(BaseModel):
    settings: SimpleSettings
    masehet: str
    daf: int


class Holiday(BaseModel):
    settings: SimpleSettings
    date: date


class YomTov(BaseModel):
    settings: Settings
    pre_shabbat: Optional[AsurBeMelachaDay] = None
    day_1: AsurBeMelachaDay
    day_2: Optional[AsurBeMelachaDay] = None
    post_shabbat: Optional[AsurBeMelachaDay] = None
    hoshana_rabba: Optional[date] = None

    pesach_part_2_day_1: Optional[AsurBeMelachaDay] = None
    pesach_part_2_day_2: Optional[AsurBeMelachaDay] = None


class Fast(BaseModel):
    settings: Settings
    moved_fast: Optional[bool] = False
    fast_start: Optional[datetime] = None
    chatzot: Optional[datetime] = None
    havdala: Optional[datetime] = None


class BooleanResp(BaseModel):
    result: bool
