import logging
from os import getenv

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from betterlogging import get_colorized_logger, DEBUG

from zmanim_api.api_helpers import DateException
from zmanim_api.settings import ROOT_PATH, SENTRY_PUBLIC_KEY
from zmanim_api.routers.main_router import main_router


logger = get_colorized_logger()
logger.setLevel(DEBUG)

app = FastAPI(root_path=f'/{ROOT_PATH}', docs_url='/', title='Zmanim API', version='1.0.1')

app.include_router(main_router, tags=['Main'])


@app.on_event('startup')
async def on_start():  # pragma: no cover
    logger.info('STARTING ZMANIM API...')


@app.middleware('http')  # pragma: no cover
async def set_sentry_context(request: Request, call_next):
    if SENTRY_PUBLIC_KEY:
        sentry_sdk.set_context('request', dict(request))
        sentry_sdk.set_user({'ip_address': request.client.host})
    return await call_next(request)


@app.exception_handler(DateException)
async def date_exception_handler(request: Request, exc: DateException):
    return JSONResponse(
        status_code=400,
        content={
            'message': f'Invalid date provided! {exc}'
        }
    )


@app.exception_handler(Exception)  # pragma: no cover
async def main_exception_handler(request: Request, e: Exception):
    sentry_sdk.capture_exception(e)

    return JSONResponse(
        status_code=500,
        content={'message': repr(e)}
    )


if __name__ == '__main__':  # pragma: no cover
    uvicorn.run(
        app,
        host='0.0.0.0' if getenv('DOCKER_MODE') else '127.0.0.1',
        port=8000,
        use_colors=True,
        log_level=logging.DEBUG,
        log_config='../uvicorn_logger.json'
    )

# todo return zmanim calculation errors
# todo translate: parshat hashavua names; daf yomi units;
# todo no havdala on fast at 60.591389 90.305912

