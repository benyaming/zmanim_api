import uvicorn
from fastapi import FastAPI, Query

from zmanim_api.helpers import Languages, CLOffset
from zmanim_api.models import ZmanimSettingsModel
from zmanim_api.api.ou_downloader import daf_yomi, zmanim, shabbos
from zmanim_api import openapi_desctiptions as ds


api = FastAPI()


lang_param = Query(Languages.en, description=ds.lang)
cl_param = Query(CLOffset.cl_18.value, description='qwerrt')  # todo descr
tz_param: str = (Query(..., description=ds.tz))
date_param: str = (Query(..., description=ds.date))
lat_param: str = (Query(..., description=ds.lat))
lng_param: str = Query(..., description=ds.lng)
diaspora_param = Query(False, description='diaspora descr')  # todo descr


@api.get('/')
async def read_root():
    return {'working': 'ok'}


@ api.post('/zmanim')
async def getzmanim(
        settings: ZmanimSettingsModel, lang: Languages = lang_param, tz=tz_param,
        date=date_param, lat=lat_param, lng=lng_param) -> dict:
    data = await zmanim(lang.value, tz, date, lat, lng, settings.dict())
    return data


@api.get('/shabbos')
async def get_shabos(
        cl_offset: CLOffset = cl_param, diaspora: bool = diaspora_param,
        lang: Languages = lang_param, tz=tz_param, lat=lat_param,  lng=lng_param) -> dict:
    data = await shabbos(lang.value, tz, lat, lng, diaspora, cl_offset.value)
    return data


@api.get('/daf_yomi')
async def get_daf_yomi(
        lang: Languages = lang_param, tz=tz_param, date=date_param,
        lat=lat_param, lng=lng_param) -> dict:
    data = await daf_yomi(lang=lang.value, tz=tz, date=date, lat=lat, lng=lng)
    return data





if __name__ == '__main__':
    uvicorn.run(api, host='0.0.0.0', port=1000)


# C:\Users\Benyomin\PycharmProjects\zmanim_api>python c:\Users\Benyomin\AppData\Local\Programs\Python\Python36-32\Tools\i18n\pygettext.py -d zmanim_api -o zmanim_api\api\locales\base.pot zmanim_ap
# i\api\localized_texts.py
