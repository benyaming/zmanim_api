from typing import Optional

from fastapi import Query, APIRouter

from ..api_helpers import (
    LanguageChoices,
    SimpleHolidayChoices,
    YomTovChoices,
    FastsChoices,
    HavdalaChoices,
    validate_date_or_get_now,
    validate_datetime_or_get_now
)
from ..models import (
    ZmanimRequest,
    ZmanimResponse,
    Shabbat,
    RoshChodesh,
    DafYomi,
    Holiday,
    YomTov,
    Fast,
    BooleanResp
)
from ..engine.daf_yomi import get_daf_yomi
from ..engine.zmanim_module import get_zmanim, is_asur_bemelaha
from ..engine.shabbat import get_shabbat
from ..engine.rosh_chodesh import get_next_rosh_chodesh
from ..engine import holidays as hd
from . import openapi_desctiptions as ds

lang_param = Query(LanguageChoices.en, description=ds.lang)
cl_param = Query(18, description='qwerrt', ge=0, lt=100)
date_param = Query(None, description=ds.date)
dt_param = Query(None, description=ds.dt)
lat_param = Query(32.09, description=ds.lat, ge=-90, le=90)
lng_param = Query(34.86, description=ds.lng, ge=-180, le=180)
elevation_param = Query(0, description='', ge=0)
havdala_param = Query(HavdalaChoices.tzeis_8_5_degrees, description='tzeit')


main_router = APIRouter()


@main_router.post('/zmanim', response_model=ZmanimResponse, response_model_exclude_none=True)
async def zmanim(
        settings: ZmanimRequest,
        date: Optional[str] = date_param,
        elevation: float = elevation_param,
        lat: float = lat_param,
        lng: float = lng_param,
) -> ZmanimResponse:
    parsed_date = validate_date_or_get_now(date)
    data = get_zmanim(
        date_=parsed_date,
        lat=lat,
        lng=lng,
        elevation=elevation,
        settings=settings)
    return data


@main_router.get('/shabbat', response_model=Shabbat, response_model_exclude_none=True)
async def shabbat(
        cl_offset: int = cl_param,
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: float = elevation_param,
        havdala: HavdalaChoices = havdala_param,
        date: Optional[str] = date_param
) -> Shabbat:
    parsed_date = validate_date_or_get_now(date)
    data = get_shabbat(lat, lng, elevation, cl_offset, havdala, parsed_date)
    return data


@main_router.get('/rosh_chodesh', response_model=RoshChodesh, response_model_exclude_none=True)
async def rosh_chodesh(date: Optional[str] = date_param) -> RoshChodesh:
    parsed_date = validate_date_or_get_now(date)
    data = get_next_rosh_chodesh(parsed_date)
    return data


@main_router.get('/daf_yomi', response_model=DafYomi, response_model_exclude_none=True)
async def daf_yomi(date: Optional[str] = date_param) -> DafYomi:
    parsed_date = validate_date_or_get_now(date)
    data = get_daf_yomi(parsed_date)
    return data


@main_router.get('/holiday', response_model=Holiday, response_model_exclude_none=True)
async def holiday(
        holiday_name: SimpleHolidayChoices = Query(..., description='select holiday name'),  # todo descr
        date: Optional[str] = date_param
):
    parsed_date = validate_date_or_get_now(date)
    resp = hd.get_simple_holiday(name=holiday_name.name, date_=parsed_date)
    return resp


@main_router.get('/yom_tov', response_model=YomTov, response_model_exclude_none=True)
async def yom_tov(
        yomtov_name: YomTovChoices = Query(..., description='select yomtov name'),  # todo descr
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        cl: int = cl_param,
        havdala: HavdalaChoices = havdala_param,
        date: Optional[str] = date_param
):
    parsed_date = validate_date_or_get_now(date)
    resp = hd.get_yom_tov(
        name=yomtov_name.name,
        date_=parsed_date,
        lat=lat,
        lng=lng,
        elevation=elevation,
        cl=cl,
        havdala_opinion=havdala
    )
    return resp


@main_router.get('/fast', response_model=Fast, response_model_exclude_none=True)
async def fast(
        fast_name: FastsChoices = Query(..., description='Select fast name'),
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        havdala: HavdalaChoices = havdala_param,
        date: Optional[str] = date_param
) -> Fast:
    parsed_date = validate_date_or_get_now(date)
    data = hd.fast(
        name=fast_name.name,
        date_=parsed_date,
        lat=lat,
        lng=lng,
        elevation=elevation,
        havdala_opinion=havdala
    )
    return data


@main_router.get('/is_asur_bemelacha', response_model=BooleanResp)
async def is_asur_bemelacha(
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        dt: Optional[str] = dt_param
) -> BooleanResp:
    parsed_dt = validate_datetime_or_get_now(dt)
    resp = is_asur_bemelaha(parsed_dt, lat, lng, elevation)
    return resp
