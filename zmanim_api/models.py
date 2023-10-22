from __future__ import annotations

import json
from datetime import datetime, time, date as Date
from pydantic import BaseModel, field_serializer


class SimpleSettings(BaseModel):
    date: Date | None = None
    jewish_date: str | None = None
    holiday_name: str | None = None


class Settings(SimpleSettings):
    cl_offset: int | None = None
    havdala_opinion: str | None = None
    coordinates: tuple[float, float] | None = None
    elevation: int | None = None
    fast_name: str | None = None
    yomtov_name: str | None = None


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
    alos: datetime | None = None
    sunrise: datetime | None = None
    misheyakir_10_2: datetime | None = None
    sof_zman_shema_ma: datetime | None = None
    sof_zman_shema_gra: datetime | None = None
    sof_zman_tefila_ma: datetime | None = None
    sof_zman_tefila_gra: datetime | None = None
    chatzos: datetime | None = None
    mincha_gedola: datetime | None = None
    mincha_ketana: datetime | None = None
    plag_mincha: datetime | None = None
    sunset: datetime | None = None
    tzeis_5_95_degrees: datetime | None = None
    tzeis_8_5_degrees: datetime | None = None
    tzeis_42_minutes: datetime | None = None
    tzeis_72_minutes: datetime | None = None
    chatzot_laila: datetime | None = None
    astronomical_hour_ma: time | None = None
    astronomical_hour_gra: time | None = None


class AsurBeMelachaDay(BaseModel):
    date: Date | None = None
    candle_lighting: datetime | None = None
    havdala: datetime | None = None


class Shabbat(AsurBeMelachaDay):
    settings: Settings
    torah_part: str = None
    late_cl_warning: bool = False


class RoshChodesh(BaseModel):
    settings: SimpleSettings
    month_name: str
    days: list[Date]
    duration: int
    molad: tuple[datetime, int]

    @field_serializer('molad')
    def serialize_molad(self, molad: tuple[datetime, int], _info) -> tuple[str, int]:
        return molad[0].isoformat(timespec='minutes'), molad[1]

    # model_config = ConfigDict(
    #     json_encoders={
    #         datetime: lambda d: d.isoformat(timespec='minutes')
    #     }
    # )


class DafYomi(BaseModel):
    settings: SimpleSettings
    masehet: str
    daf: int


class Holiday(BaseModel):
    settings: SimpleSettings
    date: Date


class YomTov(BaseModel):
    settings: Settings
    pre_shabbat: AsurBeMelachaDay | None = None

    pesach_eating_chanetz_till: datetime | None = None
    pesach_burning_chanetz_till: datetime | None = None

    day_1: AsurBeMelachaDay
    day_2: AsurBeMelachaDay | None = None
    post_shabbat: AsurBeMelachaDay | None = None
    hoshana_rabba: Date | None = None

    pesach_part_2_day_1: AsurBeMelachaDay | None = None
    pesach_part_2_day_2: AsurBeMelachaDay | None = None
    pesach_part_2_post_shabat: AsurBeMelachaDay | None = None


class Fast(BaseModel):
    settings: Settings
    moved_fast: bool | None = False
    fast_start: datetime | None = None
    chatzot: datetime | None = None
    havdala_5_95_dgr: datetime | None = None
    havdala_8_5_dgr: datetime | None = None
    havdala_42_min: datetime | None = None


class BooleanResp(BaseModel):
    result: bool
