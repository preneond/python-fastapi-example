import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.config.settings import get_settings
from src.core.database import DatabaseConnection
from src.core.responses import error_response
from src.routers import api_router

settings = get_settings()

app = FastAPI(
    title=settings.api_config.title,
    description=settings.api_config.description,
    version=settings.api_config.version,
    docs_url=settings.api_config.docs_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    # setup logger
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    app.state.logger = logger
    # setup db connection
    db_connection = DatabaseConnection(dsn=settings.db_connection.postgres_uri)
    app.state.db_connection = db_connection


@app.on_event("shutdown")
async def shutdown_event() -> None:
    db_connection = app.state.db_connection
    db_connection.close()


# exception handling
@app.exception_handler(RequestValidationError)
@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger = request.app.state.logger
    logger.error(f"{exc}")
    return error_response(errors=str(exc), status_code=status.HTTP_400_BAD_REQUEST)


app.include_router(api_router)

if __name__ == "__main__":
    settings = get_settings()
    server = settings.uvicorn
    uvicorn.run(
        app="main:app",
        host=server.host,
        port=server.port,
        log_level=server.log_level,
        reload=server.reload,
    )
