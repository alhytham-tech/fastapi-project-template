from decouple import config as decouple_config
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from config import db
from access_control import router as access_control_router



# Use self-hosted files
USE_LOCAL_DOCS_FILES = decouple_config(
    'USE_LOCAL_DOCS_FILES', cast=bool, default=False
)
DOCS_URL = decouple_config('DOCS_URL')
REDOC_URL = decouple_config('REDOC_URL')
OPENAPI_URL = decouple_config('OPENAPI_URL')
DOCS_AUTH_URL = decouple_config('DOCS_AUTH_URL')
APP_TITLE = decouple_config('APP_TITLE', default='FastAPI')
if USE_LOCAL_DOCS_FILES:
    DOCS_URL = None
    REDOC_URL = None

# Locaal docs urls
local_docs_router = APIRouter(include_in_schema=False)

@local_docs_router.get("/docs")
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=OPENAPI_URL,
        title=APP_TITLE + " - Swagger UI",
        oauth2_redirect_url=DOCS_AUTH_URL,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@local_docs_router.get(DOCS_AUTH_URL)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@local_docs_router.get("/redoc")
async def redoc_html():
    return get_redoc_html(
        openapi_url=OPENAPI_URL,
        title=APP_TITLE + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# Create database tables
db.Base.metadata.create_all(bind=db.engine)

# FastAPI app config
app = FastAPI(title=APP_TITLE, docs_url=DOCS_URL, redoc_url=REDOC_URL)

# Check if to use local docs files or not
if USE_LOCAL_DOCS_FILES:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(local_docs_router)

# Include Routers
app.include_router(access_control_router.perms_router)
app.include_router(access_control_router.roles_router)
app.include_router(access_control_router.groups_router)
