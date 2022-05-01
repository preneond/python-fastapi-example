import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.requests import Request

from src.config.settings import get_settings
from src.routers import api_router
from src.utils.responses import error_response

api_config = dict(
    title="Simple FastAPI Server",
    description="API Documentation for Simple FastAPI Server",
    version="v1",
    docs_url="/docs",
    swagger_favicon_url="https://avatars.githubusercontent.com/u/7658037?s=200&v=4",
)

app = FastAPI(**api_config)  # type: ignore


@app.on_event("startup")
async def startup_event() -> None:
    # setup logger
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    app.state.logger = logger
    # logger.info("Starting application")


# exception handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger = request.app.state.logger
    logger.error(f"{exc} [400]")
    response_json = error_response(errors=str(exc))
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response_json)


@app.exception_handler(Exception)
async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger = request.app.state.logger
    logger.error(f"Error: {exc} [500]")
    response_json = error_response(errors=str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response_json
    )


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
