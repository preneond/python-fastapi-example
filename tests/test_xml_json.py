import glob
import json
import os
from json import JSONDecodeError
from typing import List, Tuple

import pytest
from lxml import etree
from lxml.etree import XMLSyntaxError

from src.core.xml_parser import XMLParser


def json_xml_valid_case_files() -> List[Tuple[str, ...]]:
    case_files_array: List[Tuple[str, ...]] = []
    for file in glob.glob("tests/data/xml_json/*"):
        case_files_array.append(
            (os.path.join(file, "test.json"), os.path.join(file, "test.xml"))
        )
    return case_files_array


def json_invalid_format_files() -> List[str]:
    case_files_array: List[str] = []
    for case in glob.glob("tests/data/json_invalid/*/test.json"):
        case_files_array.append(case)
    return case_files_array


def xml_invalid_format_files() -> List[str]:
    case_files_array: List[str] = []
    for case in glob.glob("tests/data/xml_invalid/*/test.xml"):
        case_files_array.append(case)
    return case_files_array


@pytest.mark.parametrize("json_file, xml_file", json_xml_valid_case_files())
def test_input_xml_parser_valid_files(xml_file: str, json_file: str) -> None:
    """
    Test XML parsing and JSON parsing
    by applying equivalent JSONType xml file parsing output and JSON file parsing output

    :param xml_file: path to xml file
    :param json_file: path to json file
    """

    with open(json_file, "r") as json_fp:
        xml_parse_out = XMLParser.parse_xml_from_file(xml_file)
        json_parse_out = json.load(json_fp)
        assert xml_parse_out == json_parse_out


@pytest.mark.parametrize("json_file, xml_file", json_xml_valid_case_files())
def test_output_xml_parser_valid_files(xml_file: str, json_file: str) -> None:
    """
    Test XML parsing and JSON parsing
    by applying equivalent JSONType xml file parsing output and JSON file parsing output

    :param xml_file: path to xml file
    :param json_file: path to json file
    """
    with open(json_file, "r") as json_fp, open(xml_file, "r") as xml_fp:
        xml_fp_str = xml_fp.read()
        json_data = json.load(json_fp)
        xml_parse_out = XMLParser.parse_xml_from_json(json_data)
        xml_parse_out_etree = etree.tostring(xml_parse_out, method="c14n")
        assert xml_parse_out_etree.decode("utf-8") == xml_fp_str


@pytest.mark.parametrize("json_file", json_invalid_format_files())
def test_xml_parser_invalid_json_input(json_file: str) -> None:
    """
    Test JSON parsing exception
    """
    with pytest.raises(JSONDecodeError), open(json_file, "r") as json_fp:
        json.load(json_fp)


@pytest.mark.parametrize("xml_file", xml_invalid_format_files())
def test_xml_parser_invalid_xml_input(xml_file: str) -> None:
    """
    Test XML parsing exception
    """
    with pytest.raises((XMLSyntaxError, ValueError)), open(xml_file, "r") as xml_fp:
        XMLParser.parse_xml_from_file(xml_fp)
