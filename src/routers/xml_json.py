from typing import Any, Dict

from fastapi import APIRouter, Depends
from starlette.requests import Request

from config.annotations import JSONType
from src.utils.responses import success_response
from utils.dependencies import parse_json_input_file, parse_xml_input_file

router = APIRouter()


@router.post("/xml2json")
async def convert_xml2json(
    request: Request, xml_data: JSONType = Depends(parse_xml_input_file)
) -> Dict[str, Any]:
    """
    Convert XML to JSON
    :param request: Request object
    :param xml_data: XML data sent as multipart/form-data file
    """

    return success_response(xml_data)


@router.post("/json2xml")
async def convert_json2xml(
    request: Request, json_data: JSONType = Depends(parse_json_input_file)
) -> Dict[str, Any]:
    """
    Convert JSON to XML
    :param json_data: JSON data sent as multipart/form-data file
    :param request: Request object
    """
    return success_response(json_data)
