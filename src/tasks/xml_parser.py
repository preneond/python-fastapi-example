from enum import Enum
from typing import Dict, Union

from lxml.etree import _Element

from config.annotations import JSONObject


class XMLElementType(str, Enum):
    """
    Enumeration of XML element types.
    """

    FLOAT = "float"
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"
    OBJECT = "object"
    LIST = "list"
    NULL = "null"


def parse_etree_node_value(
    element: _Element,
) -> Union[str, int, float, bool, None]:
    """
    Parses a lxml ElementTree and returns its value.
    :param element: lxml ElementTree
    :return: value of :param element
    """
    element_type = XMLElementType(element.get("type"))
    element_value = element.get("value")
    if (
        element_type in [XMLElementType.NULL, XMLElementType.STRING]
        or not element_value
    ):
        return element_value
    elif element_type is XMLElementType.INTEGER:
        return int(element_value)
    elif element_type is XMLElementType.FLOAT:
        return float(element_value)
    elif element_type is XMLElementType.BOOLEAN:
        return element_value == "true"
    else:
        raise NotImplementedError(f"Etree element type not supported: {element_type}")


def convert_etree_to_json_object(node: _Element) -> JSONObject:
    """
    Converts lxml.etree.ElementTree to a :type JSONObject.
    :param node: etree node
    :return: JSONObject
    """

    # used as a result object only when the node has children
    result: Dict[str, JSONObject] = {}

    for element in node.iterchildren():
        element_type = XMLElementType(element.get("type"))
        element_key = element.get("key")

        if not element_key:
            return parse_etree_node_value(node)

        # if the children element is a dictionary, then save return value of convert_etree_to_json_object
        if element_type is XMLElementType.OBJECT:
            result[element_key] = convert_etree_to_json_object(element)

        # if the element is a list, then save list of convert_etree_to_json_object's return values
        elif element_type is XMLElementType.LIST:
            arr = []
            for child in element.iterchildren():
                obj = convert_etree_to_json_object(child)
                arr.append(obj)
            result[element_key] = arr
        # if the element is not an object nor a list, then return the value of the element
        else:
            result[element_key] = parse_etree_node_value(element)

    # if the result is empty, then return the value of the node
    if not result:
        return parse_etree_node_value(node)

    return result
