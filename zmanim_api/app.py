from typing import Optional

import uvicorn
from fastapi import FastAPI, Query, Request
from fastapi.responses import RedirectResponse, JSONResponse

from zmanim_api.api_helpers import (
    LanguageChoises,
    HolidayChoises,
    FastsChoises,
    HavdalaChoises,
    DATE_PATTERN,
    DateException,
    validate_date_or_get_now
)
from zmanim_api.models import ZmanimSettingsModel
from zmanim_api.engine.daf_yomi import get_daf_yomi
from zmanim_api.engine.zmanim_module import get_zmanim
from zmanim_api.engine.shabbos import shabbos
from zmanim_api.engine.rosh_chodesh import get_next_rosh_chodesh
from zmanim_api.engine import holidays as hd
from zmanim_api import openapi_desctiptions as ds
from zmanim_api.settings import ROOT_PATH


app = FastAPI(openapi_prefix=f'/{ROOT_PATH}')


lang_param = Query(LanguageChoises.en, description=ds.lang)
cl_param = Query(18, description='qwerrt', ge=0, lt=100)
date_param = Query(None, description=ds.date)
lat_param = Query(32.09, description=ds.lat, ge=-90, le=90)
lng_param = Query(34.86, description=ds.lng, ge=-180, le=180)
elevation_param = Query(0, description='', ge=0)
havdala_param = Query(HavdalaChoises.tzeis_8_5_degrees, description='tzeit')


@app.exception_handler(DateException)
async def date_exception_handler(request: Request, exc: DateException):
    return JSONResponse(
        status_code=400,
        content={
            'message': f'Invalid date provided! {exc}'
        }
    )


@app.get('/')
async def forward_to_swagger():
    prefix = f'/{ROOT_PATH}' if ROOT_PATH else ''
    return RedirectResponse(f'{prefix}/docs')


@app.post('/zmanim')
async def zmanim(
        settings: ZmanimSettingsModel,
        # lang: LanguageChoises = lang_param,
        date: Optional[str] = date_param,
        elevation: float = elevation_param,
        lat: float = lat_param,
        lng: float = lng_param,
) -> dict:
    parsed_date = validate_date_or_get_now(date)
    data = get_zmanim(
        # lang=lang.value,
        date=parsed_date,
        lat=lat,
        lng=lng,
        elevation=elevation,
        settings=settings)
    return data


@app.get('/shabbos')
async def shabos(
        cl_offset: int = cl_param,
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: float = elevation_param,
        havdala: HavdalaChoises = havdala_param,
        date: Optional[str] = date_param
) -> dict:
    parsed_date = validate_date_or_get_now(date)
    data = shabbos(lat, lng, elevation, cl_offset, havdala, parsed_date)
    return data


@app.get('/rosh_chodesh')
async def rosh_chodesh(
        date: Optional[str] = date_param
) -> dict:
    parsed_date = validate_date_or_get_now(date)
    data = get_next_rosh_chodesh(parsed_date)
    return data


@app.get('/daf_yomi')
async def daf_yomi(
        date: Optional[str] = date_param
) -> dict:
    parsed_date = validate_date_or_get_now(date)
    data = get_daf_yomi(parsed_date)
    return data


@app.get('/holidays')
async def holidays(
        holiday_name: HolidayChoises = Query(..., description='select holiday name'),  # todo descr
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        cl: int = cl_param,
        havdala: HavdalaChoises = havdala_param,
        date: Optional[str] = date_param
):
    parsed_date = validate_date_or_get_now(date)
    resp = hd.holiday(
        name=holiday_name.name,
        date_=parsed_date,
        lat=lat,
        lng=lng,
        elevation=elevation,
        cl=cl,
        havdala_opinion=havdala
    )
    return resp


@app.get('/fasts')
async def fasts(
        fast_name: FastsChoises = Query(..., description='Select fast name'),
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: int = elevation_param,
        havdala: HavdalaChoises = havdala_param,
        date: Optional[str] = date_param
) -> dict:
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


if __name__ == '__main__':
    uvicorn.run(app, port=2000, use_colors=True)

# todo return zmanim calculation errors

# todo translate: parshat hashavua names; daf yomi units;

# C:\Users\Benyomin\PycharmProjects\zmanim_api>python c:\Users\Benyomin\AppData\Local\Programs\Python\Python36-32\Tools\i18n\pygettext.py -d zmanim_api -o zmanim_api\api\locales\base.pot zmanim_ap
# i\api\localized_texts.py
