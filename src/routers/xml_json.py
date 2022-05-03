from typing import Optional, Union

from fastapi import APIRouter, Depends, File, UploadFile
from lxml import etree
from starlette.responses import JSONResponse, Response

from core.dependencies import get_accept_request_header, load_json_file
from core.responses import success_response
from core.xml_parser import XMLParser
from src.config.annotations import JSONType

router = APIRouter()


@router.post("/xml2json")
async def convert_xml2json_request(file: UploadFile = File(...)) -> JSONResponse:
    """
    Convert XML to JSON
    :param file: XML file as multipart/form-data
    """
    xml_data: JSONType = XMLParser.parse_file(file.file)
    return success_response(xml_data)


@router.post("/json2xml")
async def convert_json2xml_request(
    accept_header: Optional[str] = Depends(get_accept_request_header),
    json_data: JSONType = Depends(load_json_file),
) -> Union[Response, JSONResponse]:
    """
    Endpoint that converts JSON to XML.

    Returns XML in data JSON key by default.
    If `accept` request header is set to `text/xml`, returns XML as response.

    :param accept_header: request header `accept`
    :param json_data: JSON data sent as multipart/form-data file
    """

    xml_data = XMLParser.parse_json(json_data)
    xml_data_str = etree.tostring(xml_data, encoding="utf-8")
    if accept_header == "text/xml":
        return Response(content=xml_data_str, media_type="text/xml")
    else:
        return success_response(xml_data_str)
