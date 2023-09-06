import logging

from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app import limiter
from app.logs.logconfig import init_loggers
from app.qrcode.routes import free_routes, pro_routes

# init our logger
init_loggers(logger_name="app-logs")
log = logging.getLogger("app-logs")

app = FastAPI(docs_url="/")


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get('/health-check')
@limiter.limit("5/minute")
def health_check(request: Request) -> dict:
    return {'status': r'100% good'}


app.include_router(free_routes.router)
app.include_router(pro_routes.router)
