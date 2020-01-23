from typing import Optional
from datetime import datetime as dt, date as Date

import uvicorn
from fastapi import FastAPI, Query
from starlette.responses import Response
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


api = FastAPI()


lang_param = Query(LanguageChoises.en, description=ds.lang)
cl_param = Query(18, description='qwerrt', ge=0, lt=100)
date_param = Query(..., description=ds.date, regex=DATE_PATTERN)
date_optional_param = Query(None, description=ds.date, regex=DATE_PATTERN)
lat_param = Query(..., description=ds.lat, ge=-90, le=90)
lng_param = Query(..., description=ds.lng, ge=-180, le=180)
elevation_param = Query(0, description='', ge=0)
havdala_param = Query(HavdalaChoises.tzeis_850_degrees, description='tzeit')


def convert_date_to_dt(date: str) -> Optional[Date]:
    try:
        response = dt.strptime(date, DATE_FORMAT)
    except ValueError:
        response = False
    return response


@api.get('/')
async def read_root():
    return {'working': 'ok'}


@api.post('/zmanim')
async def getzmanim(
        settings: ZmanimSettingsModel,
        response: Response,
        lang: LanguageChoises = lang_param,
        date: str = date_param,
        elevation: float = elevation_param,
        lat: float = lat_param,
        lng: float = lng_param,
) -> dict:
    d = convert_date_to_dt(date)
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


@api.get('/shabbos')
async def shabos(
        cl_offset: int = cl_param,
        lang: LanguageChoises = lang_param,
        lat: float = lat_param,
        lng: float = lng_param,
        havdala: HavdalaChoises = havdala_param
) -> dict:
    data = await shabbos(lang.value, lat, lng, cl_offset, havdala)
    return data


@api.get('/rosh_chodesh')
async def rosh_chodesh(response: Response, date: str = date_optional_param) -> dict:

    if not date:
        data = get_next_rosh_chodesh()
        return data
    d = convert_date_to_dt(date)
    if not d:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Date {date} does not exist!'}
    data = get_next_rosh_chodesh(d)
    return data


@api.get('/daf_yomi')
async def daf_yomi(
        response: Response,
        lang: LanguageChoises = lang_param,
        date: str = date_param,
        lat: float = lat_param,
        lng: float = lng_param
) -> dict:
    d = convert_date_to_dt(date)
    if not d:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': f'Date {date} does not exist!'}
    data = await get_daf_yomi(lang=lang.value, date=d, lat=lat, lng=lng)
    return data


@api.get('/rosh_hashana')
async def rosh_hashana(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param,
) -> dict:
    data = await hd.rosh_hashana(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@api.get('/yom_kippur')
async def yom_kippur(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param,
) -> dict:
    data = await hd.yom_kippur(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@api.get('/succos')
async def succos(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.succos(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@api.get('/shmini_atzeres')
async def shmini_atzeres(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.shmini_atzeres(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@api.get('/pesach')
async def pesach(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.pesach(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@api.get('/shavuos')
async def shavuos(
        lat: float = lat_param,
        lng: float = lng_param,
        cl_offset: int = cl_param
) -> dict:
    data = await hd.shavuos(lat=lat, lng=lng, cl_offset=cl_offset)
    return data


@api.get('/channukah')
async def channukah() -> dict:
    data = hd.channukah()
    return data


@api.get('/tu_bishvat')
async def tu_bishvat() -> dict:
    data = hd.tu_bishvat()
    return data


@api.get('/purim')
async def purim() -> dict:
    data = hd.purim()
    return data


@api.get('/israel_holidays')
async def israel_holidays() -> dict:
    data = hd.israel_holidays()
    return data


@api.get('/fasts')
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
    uvicorn.run(api, port=1000)

# todo what do we translate? month names? ...?
# todo havdala_param to holidays and fasts (?)
# todo correct time format in all places?

# C:\Users\Benyomin\PycharmProjects\zmanim_api>python c:\Users\Benyomin\AppData\Local\Programs\Python\Python36-32\Tools\i18n\pygettext.py -d zmanim_api -o zmanim_api\api\locales\base.pot zmanim_ap
# i\api\localized_texts.py
