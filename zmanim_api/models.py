from typing import TypedDict, Optional
from dataclasses import dataclass

from pydantic import BaseModel


class ZmanimSettingsModel(BaseModel):
    sunrise: bool = True
    alos: bool = True
    sof_zman_tefila_gra: bool = True
    sof_zman_tefila_ma: bool = True
    talis_ma: bool = True
    sof_zman_shema_gra: bool = True
    sof_zman_shema_ma: bool = True
    chatzos: bool = True
    mincha_ketana: bool = True
    mincha_gedola: bool = True
    plag_mincha: bool = True
    sunset: bool = True
    tzeis_850_degrees: bool = True
    tzeis_72_minutes: bool = True
    tzeis_42_minutes: bool = True
    tzeis_595_degrees: bool = True
    chatzot_laila: bool = True
    astronomical_hour_ma: bool = True
    astronomical_hour_gra: bool = True


# @dataclass
# class ZmanimSetModel(object):
#     sunrise: Optional[str] = None
#     sof_zman_tefila_gra: Optional[str] = None
#     sof_zman_tefila_ma: Optional[str] = None
#     talis_ma: Optional[str] = None
#     sof_zman_shema_gra: Optional[str] = None
#     sof_zman_shema_ma: Optional[str] = None
#     chatzos: Optional[str] = None
#     mincha_ketana_gra: Optional[str] = None
#     mincha_gedola_ma: Optional[str] = None
#     alos_ma: Optional[str] = None
#     plag_mincha_ma: Optional[str] = None
#     sunset: Optional[str] = None
#     tzeis_850_degrees: Optional[str] = None
#     tzeis_72_minutes: Optional[str] = None
#     tzeis_42_minutes: Optional[str] = None
#     tzeis_595_degrees: Optional[str] = None
#     chatzot_laila: Optional[str] = None
#     astronomical_hour_ma: Optional[str] = None
#     astronomical_hour_gra: Optional[str] = None
