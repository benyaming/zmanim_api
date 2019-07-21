from pydantic import BaseModel


class ZmanimSettingsModel(BaseModel):
    sunrise: bool = True
    sof_zman_tefila_gra: bool = True
    sof_zman_tefila_ma: bool = True
    talis_ma: bool = True
    sof_zman_shema_gra: bool = True
    sof_zman_shema_ma: bool = True
    chatzos: bool = True
    mincha_ketana_gra: bool = True
    mincha_gedola_ma: bool = True
    alos_ma: bool = True
    plag_mincha_ma: bool = True
    sunset: bool = True
    tzeis_850_degrees: bool = True
    tzeis_72_minutes: bool = True
    tzeis_42_minutes: bool = True
    tzeis_595_degrees: bool = True
    chatzot_laila: bool = True
    astronomical_hour_ma: bool = True
    astronomical_hour_gra: bool = True

