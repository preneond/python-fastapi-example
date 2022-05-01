import json

from fastapi import File, UploadFile
from lxml.etree import parse

from config.annotations import JSONObject
from tasks.xml_parser import convert_etree_to_json_object


async def parse_json_input_file(file: UploadFile = File(...)) -> JSONObject:
    """
    Parses a JSON file and returns its content as a JSONObject.
    :param file: input JSON file
    :return: JSONObject with :param file content
    """
    file_data = await file.read()
    json_data = json.loads(file_data)
    return json_data


async def parse_xml_input_file(file: UploadFile = File(...)) -> JSONObject:
    """
    Parses an XML file and returns its content as a
    :param file: input XML file
    :return: JSONObject with :param file content
    """
    xml_parsed = parse(file.file)
    xml_parsed_json_obj = convert_etree_to_json_object(xml_parsed.getroot())
    return xml_parsed_json_obj
