import uvicorn
from fastapi import FastAPI, Query

from zmanim_api.helpers import Languages, CLOffset, Holidays
from zmanim_api.models import ZmanimSettingsModel
from zmanim_api.api.ou_downloader import daf_yomi, zmanim, shabbos
from zmanim_api.api.rosh_chodesh import get_next_rosh_chodesh
from zmanim_api import openapi_desctiptions as ds


api = FastAPI()


lang_param = Query(Languages.en, description=ds.lang)
cl_param = Query(CLOffset.cl_18.value, description='qwerrt')  # todo descr
date_param = (Query(..., description=ds.date))
lat_param = Query(..., description=ds.lat)
lng_param = Query(..., description=ds.lng)
diaspora_param = Query(False, description='diaspora descr')  # todo descr


@api.get('/')
async def read_root():
    return {'working': 'ok'}


@ api.post('/zmanim')
async def getzmanim(
        settings: ZmanimSettingsModel,
        lang: Languages = lang_param,
        date: str = date_param,
        lat: float = lat_param,
        lng: float = lng_param) -> dict:
    data = await zmanim(lang.value, date, lat, lng, settings.dict())
    return data


@api.get('/shabbos')
async def get_shabos(
        cl_offset: CLOffset = cl_param,
        diaspora: bool = diaspora_param,
        lang: Languages = lang_param,
        lat: float = lat_param,
        lng: float = lng_param
) -> dict:
    data = await shabbos(lang.value, lat, lng, diaspora, cl_offset.value)
    return data


@api.get('/rosh_chodesh')
async def get_rosh_chodesh(date: str = Query(None, description='rh_date')) -> dict:
    # todo description
    data = get_next_rosh_chodesh(date)
    return data


@api.get('/daf_yomi')
async def get_daf_yomi(
        lang: Languages = lang_param, date: str = date_param,
        lat: float = lat_param, lng: float = lng_param) -> dict:
    data = await daf_yomi(lang=lang.value, date=date, lat=lat, lng=lng)
    return data


@api.get('/holyday')
async def get_holiday(
        lang: Languages = lang_param, date: str = Query(None, description='...'),
        holiday: Holidays = Query(..., description='holiday type')  # todo descriptions
) -> dict:

    return {}


if __name__ == '__main__':
    uvicorn.run(api, host='0.0.0.0', port=1000)


# C:\Users\Benyomin\PycharmProjects\zmanim_api>python c:\Users\Benyomin\AppData\Local\Programs\Python\Python36-32\Tools\i18n\pygettext.py -d zmanim_api -o zmanim_api\api\locales\base.pot zmanim_ap
# i\api\localized_texts.py
