from typing import Optional
from datetime import datetime as dt, date as Date

import uvicorn
from fastapi import FastAPI, Query
from starlette.responses import Response, RedirectResponse
from starlette import status

from zmanim_api.helpers import LanguageChoises, FastsChoises, HavdalaChoises, \
    DATE_PATTERN, DATE_FORMAT
from zmanim_api.models import ZmanimSettingsModel
from zmanim_api.api.daf_yomi import get_daf_yomi
from zmanim_api.api.zmanimm import get_zmanim
from zmanim_api.api.shabbos import shabbos
from zmanim_api.api.rosh_chodesh import get_next_rosh_chodesh
from zmanim_api.api import holidays as hd
from zmanim_api import openapi_desctiptions as ds
from zmanim_api.settings import ROOT_PATH


app = FastAPI(openapi_prefix=f'/{ROOT_PATH}')


lang_param = Query(LanguageChoises.en, description=ds.lang)
cl_param = Query(18, description='qwerrt', ge=0, lt=100)
date_param = Query(..., description=ds.date, regex=DATE_PATTERN)
date_optional_param = Query(None, description=ds.date, regex=DATE_PATTERN)
lat_param = Query(..., description=ds.lat, ge=-90, le=90)
lng_param = Query(..., description=ds.lng, ge=-180, le=180)
elevation_param = Query(0, description='', ge=0)
havdala_param = Query(HavdalaChoises.tzeis_850_degrees, description='tzeit')


def parse_date(date: str, with_time: bool = True) -> Optional[Date]:
    try:
        response = dt.strptime(date, DATE_FORMAT)
    except ValueError:
        response = False
    else:
        if not with_time:
            response = response.date()
    return response


@app.get('/')
async def forward_to_swagger():
    prefix = f'/{ROOT_PATH}' if ROOT_PATH else ''
    return RedirectResponse(f'{prefix}/docs')


@app.post('/zmanim')
async def getzmanim(
        response: Response,
        settings: ZmanimSettingsModel,
        lang: LanguageChoises = lang_param,
        date: str = date_param,
        elevation: float = elevation_param,
        lat: float = lat_param,
        lng: float = lng_param,
) -> dict:
    d = parse_date(date)
    if not d:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Date {date} does not exist!'}

    data = await get_zmanim(
        lang=lang.value,
        date=d,
        lat=lat,
        lng=lng,
        elevation=elevation,
        settings=settings)
    return data


@app.get('/shabbos')
async def shabos(
        response: Response,
        cl_offset: int = cl_param,
        # lang: LanguageChoises = lang_param,
        lat: float = lat_param,
        lng: float = lng_param,
        elevation: float = elevation_param,
        havdala: HavdalaChoises = havdala_param,
        date: str = date_optional_param
) -> dict:
    if date:
        parsed_date = parse_date(date, with_time=False)
        if not parsed_date:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'message': f'Date {date} does not exist!'}
    else:
        parsed_date = Date.today()

    data = await shabbos(lat, lng, elevation, cl_offset, havdala, parsed_date)
    return data


@app.get('/rosh_chodesh')
async def rosh_chodesh(response: Response, date: str = date_optional_param) -> dict:

    if not date:
        data = get_next_rosh_chodesh()
        return data
    d = parse_date(date)
    if not d:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Date {date} does not exist!'}
    data = get_next_rosh_chodesh(d)
    return data


@app.get('/daf_yomi')
async def daf_yomi(
        response: Response,
        lang: LanguageChoises = lang_param,
        date: str = date_param,
        lat: float = lat_param,
        lng: float = lng_param
) -> dict:
    d = parse_date(date)
    if not d:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Date {date} does not exist!'}
    data = await get_daf_yomi(lang=lang.value, date=d, lat=lat, lng=lng)
    return data


@app.get('/rosh_hashana')
async def rosh_hashana(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param,
) -> dict:
    data = await hd.rosh_hashana(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@app.get('/yom_kippur')
async def yom_kippur(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param,
) -> dict:
    data = await hd.yom_kippur(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@app.get('/succos')
async def succos(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.succos(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@app.get('/shmini_atzeres')
async def shmini_atzeres(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.shmini_atzeres(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@app.get('/pesach')
async def pesach(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.pesach(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@app.get('/shavuos')
async def shavuos(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.shavuos(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@app.get('/channukah')
async def channukah() -> dict:
    data = hd.channukah()
    return data


@app.get('/tu_bishvat')
async def tu_bishvat() -> dict:
    data = hd.tu_bishvat()
    return data


@app.get('/purim')
async def purim() -> dict:
    data = hd.purim()
    return data


@app.get('/israel_holidays')
async def israel_holidays() -> dict:
    data = hd.israel_holidays()
    return data


@app.get('/fasts')
async def fasts(
        fast_name: FastsChoises = Query(..., description='Select fast name'),
        lat: float = lat_param,
        lng: float = lng_param,
        havdala: HavdalaChoises = havdala_param
) -> dict:
    # todo descr
    data = await hd.fast(fast_name.name, lat, lng, havdala)
    return data


if __name__ == '__main__':
    uvicorn.run(app, port=2000, use_colors=True)

# todo what do we translate? month names? ...?
# todo havdala_param to holidays and fasts (?)
# todo correct time format in all places?

# C:\Users\Benyomin\PycharmProjects\zmanim_api>python c:\Users\Benyomin\AppData\Local\Programs\Python\Python36-32\Tools\i18n\pygettext.py -d zmanim_api -o zmanim_api\api\locales\base.pot zmanim_ap
# i\api\localized_texts.py
