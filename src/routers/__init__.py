from fastapi import APIRouter

from src.routers import template, user, xml_json

api_router = APIRouter()
api_router.include_router(xml_json.router, tags=["XML/JSON Conversion"])
api_router.include_router(user.router, tags=["User"])
api_router.include_router(template.router, tags=["Form Template"])
