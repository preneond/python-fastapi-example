import json

from fastapi import File, UploadFile

from config.annotations import JSONType
from tasks.xml_parser import XMLParser


async def parse_json_input_file(file: UploadFile = File(...)) -> JSONType:
    """
    Parses a JSON file and returns its content as a JSONObject.
    :param file: input JSON file
    :return: JSONObject with :param file content
    """
    file_data = await file.read()
    json_data = json.loads(file_data)
    return json_data


async def parse_xml_input_file(file: UploadFile = File(...)) -> JSONType:
    """
    Parses an XML file and returns its content as a
    :param file: input XML file
    :return: JSONObject with :param file content
    """
    return XMLParser.parse_file(file.file)
