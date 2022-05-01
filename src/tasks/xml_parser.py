from enum import Enum
from typing import Any, Dict, Union

from lxml.etree import _Element, parse

from config.annotations import JSONType


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


class XMLParser:
    @staticmethod
    def _parse_etree_node_leaf(
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
            raise NotImplementedError(
                f"Etree element type not supported: {element_type}"
            )

    @staticmethod
    def _parse_etree_node_parent(
        element: _Element, element_type: XMLElementType
    ) -> JSONType:
        """
        Parses a lxml Element and returns its value.
        :param element: lxml Elemnt
        :param element_type:
        :return:
        """
        # if the children element is a dictionary, then save return value of _parse_etree_to_json_type
        if element_type is XMLElementType.OBJECT:
            return XMLParser._parse_etree_to_json_type(element)

        # if the element is a list, then save list of _parse_etree_to_json_type's return values
        elif element_type is XMLElementType.LIST:
            arr = []
            for child in element.iterchildren():
                obj = XMLParser._parse_etree_to_json_type(child)
                arr.append(obj)
            return arr
        # if the element is not an object nor a list, then return the value of the element
        else:
            return XMLParser._parse_etree_node_leaf(element)

    @staticmethod
    def _parse_etree_to_json_type(node: _Element) -> JSONType:
        """
        Converts lxml.etree.ElementTree to a :type JSONObject.
        :param node: etree node
        :return: JSONObject
        """

        # used as a result object only when the node has children
        result: Dict[str, JSONType] = {}

        for element in node.iterchildren():
            element_type = XMLElementType(element.get("type"))
            element_key = element.get("key")

            if not element_key:
                return XMLParser._parse_etree_node_leaf(node)

            result[element_key] = XMLParser._parse_etree_node_parent(
                element, element_type
            )

        # if the result is empty, then return the value of the node
        if not result:
            return XMLParser._parse_etree_node_leaf(node)

        return result

    @staticmethod
    def parse_file(file: Any) -> JSONType:
        xml_parsed = parse(file)
        return XMLParser._parse_etree_to_json_type(node=xml_parsed.getroot())
