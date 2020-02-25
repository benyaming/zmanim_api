import uvicorn
from fastapi import FastAPI, Query

from zmanim_api.helpers import Languages, Fasts
from zmanim_api.models import ZmanimSettingsModel
from zmanim_api.api.ou_downloader import daf_yomi, zmanim, shabbos
from zmanim_api.api.rosh_chodesh import get_next_rosh_chodesh
from zmanim_api.api import holidays as hd
from zmanim_api import openapi_desctiptions as ds


app = FastAPI()


lang_param = Query(Languages.en, description=ds.lang)
cl_param = Query(18, description='qwerrt')  # todo descr
date_param = (Query(..., description=ds.date))
lat_param = Query(..., description=ds.lat)
lng_param = Query(..., description=ds.lng)


@app.get('/')
async def read_root():
    return {'working': 'ok'}


@app.post('/zmanim')
async def getzmanim(
        settings: ZmanimSettingsModel,
        lang: Languages = lang_param,
        date: str = date_param,
        lat: float = lat_param,
        lng: float = lng_param) -> dict:
    data = await zmanim(lang.value, date, lat, lng, settings.dict())
    return data


@app.get('/shabbos')
async def shabos(
        cl_offset: int = cl_param,
        lang: Languages = lang_param,
        lat: float = lat_param,
        lng: float = lng_param
) -> dict:
    data = await shabbos(lang.value, lat, lng, cl_offset)
    return data


@app.get('/rosh_chodesh')
async def rosh_chodesh(date: str = Query(None, description='rh_date')) -> dict:
    # todo description
    data = get_next_rosh_chodesh(date)
    return data


@app.get('/daf_yomi')
async def daf_yomi(
        lang: Languages = lang_param,
        date: str = date_param,
        lat: float = lat_param,
        lng: float = lng_param
) -> dict:
    data = await daf_yomi(lang=lang.value, date=date, lat=lat, lng=lng)
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
        fast_name: Fasts = Query(..., description='Select fast name'),
        lat: float = lat_param,
        lng: float = lng_param
) -> dict:
    # todo descr
    data = await hd.fast(fast_name.name, lat, lng)
    return data


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=1000)

# todo what do we translate? month names? ...?
# todo havdala time? 850? 42? ...?

# C:\Users\Benyomin\PycharmProjects\zmanim_api>python c:\Users\Benyomin\AppData\Local\Programs\Python\Python36-32\Tools\i18n\pygettext.py -d zmanim_api -o zmanim_api\api\locales\base.pot zmanim_ap
# i\api\localized_texts.py
