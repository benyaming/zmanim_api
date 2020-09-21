import logging
from typing import Optional
from os import getenv

import uvicorn
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse

from zmanim_api.api_helpers import (
    LanguageChoises,
    SimpleHolidayChoises,
    YomTovChoises,
    FastsChoises,
    HavdalaChoises,
    DateException,
    validate_date_or_get_now,
    validate_datetime_or_get_now
)
from zmanim_api.models import (
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
from zmanim_api.engine.daf_yomi import get_daf_yomi
from zmanim_api.engine.zmanim_module import get_zmanim, is_asur_bemelaha
from zmanim_api.engine.shabbat import get_shabbat
from zmanim_api.engine.rosh_chodesh import get_next_rosh_chodesh
from zmanim_api.engine import holidays as hd
from zmanim_api import openapi_desctiptions as ds
from zmanim_api.settings import ROOT_PATH
from better_exceptions import logger


app = FastAPI(openapi_prefix=f'/{ROOT_PATH}', docs_url='/')


lang_param = Query(LanguageChoises.en, description=ds.lang)
cl_param = Query(18, description='qwerrt', ge=0, lt=100)
date_param = Query(None, description=ds.date)
dt_param = Query(None, description=ds.dt)
lat_param = Query(32.09, description=ds.lat, ge=-90, le=90)
lng_param = Query(34.86, description=ds.lng, ge=-180, le=180)
elevation_param = Query(0, description='', ge=0)
havdala_param = Query(HavdalaChoises.tzeis_8_5_degrees, description='tzeit')


@app.on_event('startup')
async def on_start():
    logger.info('STARTING ZMANIM API...')


@app.exception_handler(DateException)
async def date_exception_handler(request: Request, exc: DateException):
    return JSONResponse(
        status_code=400,
        content={
            'message': f'Invalid date provided! {exc}'
        }
    )


@app.post('/zmanim', response_model=ZmanimResponse, response_model_exclude_none=True)
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


@app.get('/shabbat', response_model=Shabbat, response_model_exclude_none=True)
async def shabbat(
        cl_offset: int = cl_param,
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: float = elevation_param,
        havdala: HavdalaChoises = havdala_param,
        date: Optional[str] = date_param
) -> Shabbat:
    parsed_date = validate_date_or_get_now(date)
    data = get_shabbat(lat, lng, elevation, cl_offset, havdala, parsed_date)
    return data


@app.get('/rosh_chodesh', response_model=RoshChodesh)
async def rosh_chodesh(date: Optional[str] = date_param) -> RoshChodesh:
    parsed_date = validate_date_or_get_now(date)
    data = get_next_rosh_chodesh(parsed_date)
    return data


@app.get('/daf_yomi', response_model=DafYomi)
async def daf_yomi(date: Optional[str] = date_param) -> DafYomi:
    parsed_date = validate_date_or_get_now(date)
    data = get_daf_yomi(parsed_date)
    return data


@app.get('/holiday', response_model=Holiday)
async def holiday(
        holiday_name: SimpleHolidayChoises = Query(..., description='select holiday name'),  # todo descr
        date: Optional[str] = date_param
):
    parsed_date = validate_date_or_get_now(date)
    resp = hd.get_simple_holiday(name=holiday_name.name, date_=parsed_date)
    return resp


@app.get('/yom_tov', response_model=YomTov, response_model_exclude_none=True)
async def yom_tov(
        yomtov_name: YomTovChoises = Query(..., description='select yomtov name'),  # todo descr
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        cl: int = cl_param,
        havdala: HavdalaChoises = havdala_param,
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


@app.get('/fast', response_model=Fast, response_model_exclude_none=True)
async def fast(
        fast_name: FastsChoises = Query(..., description='Select fast name'),
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        havdala: HavdalaChoises = havdala_param,
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


@app.get('/is_asur_bemelacha', response_model=BooleanResp)
async def is_asur_bemelacha(
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        dt: Optional[str] = dt_param
) -> BooleanResp:
    parsed_dt = validate_datetime_or_get_now(dt)
    resp = is_asur_bemelaha(parsed_dt, lat, lng, elevation)
    return resp


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0' if getenv('DOCKER_MODE') else '127.0.0.1',
        port=8000,
        use_colors=True,
        log_level=logging.DEBUG
    )

# todo return zmanim calculation errors

# todo translate: parshat hashavua names; daf yomi units;

# C:\Users\Benyomin\PycharmProjects\zmanim_api>python c:\Users\Benyomin\AppData\Local\Programs\Python\Python36-32\Tools\i18n\pygettext.py -d zmanim_api -o zmanim_api\api\locales\base.pot zmanim_ap
# i\api\localized_texts.py
