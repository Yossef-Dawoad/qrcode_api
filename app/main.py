import logging
import sys

from fastapi import FastAPI

from app.logs.logconfig import init_loggers
from app.qrcode.routes import free_routes, pro_routes

print(sys.path)


# init our logger
init_loggers(logger_name="app-logs")
log = logging.getLogger("app-logs")

app = FastAPI(docs_url="/")

app.include_router(free_routes.router)
app.include_router(pro_routes.router)
