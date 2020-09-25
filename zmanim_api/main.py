import logging
from os import getenv

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from zmanim_api.api_helpers import DateException
from zmanim_api.settings import ROOT_PATH
from zmanim_api.routers.main_router import main_router
from better_exceptions import logger


app = FastAPI(root_path=f'/{ROOT_PATH}', docs_url='/', title='Zmanim API', version='1.0.1')
app.include_router(main_router, tags=['Main'])


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


@app.exception_handler(Exception)
async def main_exception_handler(request: Request, e: Exception):
    logger.exception(e)
    return JSONResponse(
        status_code=400,
        content={'message': repr(e)}
    )


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
