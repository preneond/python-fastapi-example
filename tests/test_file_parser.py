import glob
import json
import os
from typing import List, Tuple

import pytest

from src.tasks.xml_parser import XMLParser


def json_xml_case_files() -> List[Tuple[str, ...]]:
    case_files_array: List[Tuple[str, ...]] = []
    for file in glob.glob("tests/data/xml_json/*"):
        case = glob.glob(os.path.join(file, "test.*"))
        case_files_array.append(tuple(case))
    return case_files_array


@pytest.mark.parametrize("json_file, xml_file", json_xml_case_files())
def test_json_xml_parser(xml_file: str, json_file: str) -> None:
    """
    Test XML parsing and JSON parsing
    by applying equivalent JSONType xml file parsing output and JSON file parsing output

    :param xml_file: path to xml file
    :param json_file: path to json file
    """

    with open(json_file, "r") as json_fp:
        xml_parse_out = XMLParser.parse_file(xml_file)
        json_parse_out = json.load(json_fp)
        assert xml_parse_out == json_parse_out
