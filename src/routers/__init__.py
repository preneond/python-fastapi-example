from fastapi import APIRouter

from src.routers import user, xml_json

api_router = APIRouter(prefix="")
api_router.include_router(xml_json.router, prefix="", tags=["XML/JSON Conversion"])
api_router.include_router(user.router, prefix="/user", tags=["User"])
