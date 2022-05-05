import json
from typing import Optional, Union

from fastapi import APIRouter, Depends, File, UploadFile
from lxml import etree
from starlette import status
from starlette.responses import JSONResponse, Response

from src.config.annotations import JSONType
from src.core.dependencies import get_accept_request_header
from src.core.responses import error_response, success_response
from src.core.xml_parser import XMLParser

router = APIRouter()


@router.post("/xml2json")
async def convert_xml2json_request(file: UploadFile = File(...)) -> JSONResponse:
    """
    Convert XML to JSON

    Parameters:
    - **file**: XML file as multipart/form-data**: input JSON file as multipart/form-data

    Returns JSON as a response.
    \f
    :param file: XML file as multipart/form-data
    """
    if file.content_type != "text/xml":
        return error_response(
            "'text/xml' file's content type is required",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    xml_data: JSONType = XMLParser.parse_xml_from_file(file.file)
    return success_response(xml_data)


@router.post("/json2xml")
async def convert_json2xml_request(
    file: UploadFile = File(...),
    accept_header: Optional[str] = Depends(get_accept_request_header),
) -> Union[Response, JSONResponse]:
    """
    Endpoint that converts JSON to XML.
    When `accept` request header is set to `text/xml`, returns XML as response.
    Otherwise, returns JSON as response.

    Request Path parameters:
    - **file**: input JSON file as multipart/form-data
    - **accept_header**: request header `accept`

    \f
    :param file: input JSON file as multipart/form-data
    :param accept_header: request header `accept`
    :returns: XML in data JSON key by default.
    """
    if file.content_type != "application/json":
        return error_response(
            "'application/json' file's content type is required",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # read the file and parse it to json
    file_data = await file.read()
    json_data = json.loads(file_data)

    # parse the xml from the json
    xml_data = XMLParser.parse_xml_from_json(json_data)
    xml_data_str = etree.tostring(xml_data, encoding="utf-8")

    if accept_header == "text/xml":
        return Response(content=xml_data_str, media_type="text/xml")
    else:
        return success_response(xml_data_str)
