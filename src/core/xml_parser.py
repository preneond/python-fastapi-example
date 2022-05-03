import json
from enum import Enum
from typing import Any, Dict, Union

from lxml import etree
from lxml.etree import _Element, parse

from src.config.annotations import JSONType


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

    @staticmethod
    def from_value(value: Any) -> Any:
        """
        Returns the XML Element type from given value
        :param value:
        :return:
        """
        if isinstance(value, str):
            return XMLElementType.STRING
        elif isinstance(value, bool):
            return XMLElementType.BOOLEAN
        elif isinstance(value, int):
            return XMLElementType.INTEGER
        elif isinstance(value, float):
            return XMLElementType.FLOAT
        elif isinstance(value, dict):
            return XMLElementType.OBJECT
        elif isinstance(value, list):
            return XMLElementType.LIST
        elif value is None:
            return XMLElementType.NULL
        else:
            raise ValueError(f"Unsupported type: {type(value)}")


class XMLParser:
    """
    XML parser class
    """

    @staticmethod
    def _parse_etree_node_leaf(
        element: _Element,
    ) -> Union[str, int, float, bool, Dict[Any, Any], None]:
        """
        Parses a lxml ElementTree and returns its value.
        :param element: lxml ElementTree
        :return: value of :param element
        """
        element_type = XMLElementType(element.get("type"))
        element_value = element.get("value")

        # element value validation check
        if element_value is None:
            if element_type is XMLElementType.NULL:
                return None
            elif element_type is XMLElementType.OBJECT:
                # edge case -> when json looks like {}, we do not want to return "null", but <item type="object"/>
                return {}
            else:
                raise ValueError("Invalid XML file schema")

        # element type validation check
        if element_type is XMLElementType.STRING:
            return element_value
        if element_type is XMLElementType.INTEGER:
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
    def _parse_etree_to_json_type(node: _Element) -> JSONType:
        """
        Converts lxml.etree.ElementTree to a :type JSONObject.
        :param node: etree node
        :return: JSONObject
        """

        # if the node is leaf, then return the value of the node with/without its key
        if not node.getchildren():  # type: ignore
            node_key = node.get("key")
            if node_key is None:
                return XMLParser._parse_etree_node_leaf(node)
            else:
                return {node_key: XMLParser._parse_etree_node_leaf(node)}

        # if all children are key-less, then return a list of children
        if all(map(lambda child: child.get("key") is None, node.iterchildren())):
            return [
                XMLParser._parse_etree_to_json_type(child)
                for child in node.iterchildren()
            ]

        # if all children have keys, then return a dictionary of children
        else:
            result: Dict[str, JSONType] = {}
            for children in node.iterchildren():
                children_key = children.get("key")
                children_type = XMLElementType(children.get("type"))

                if children_key is None:
                    raise ValueError("Invalid XML file schema")

                if children_type in [XMLElementType.OBJECT, XMLElementType.LIST]:
                    result[children_key] = XMLParser._parse_etree_to_json_type(children)

                # if the element is not an object nor a list, then return the value of the element
                else:
                    result[children_key] = XMLParser._parse_etree_node_leaf(children)

            return result

    @staticmethod
    def _parse_json_data_to_etree(data: JSONType) -> _Element:
        """
        Converts a :type JSONObject to lxml.etree.ElementTree.
        :param item: JSONObject
        :return: lxml.etree.ElementTree
        """
        item_type = XMLElementType.from_value(data)
        if item_type is XMLElementType.OBJECT:
            element = etree.Element("ITEM", attrib={"type": "object"})
            for key, value in data.items():  # type: ignore
                child = XMLParser._parse_json_data_to_etree(value)
                child.set("key", key)
                element.append(child)
            return element
        elif item_type is XMLElementType.LIST:
            element = etree.Element("ITEM", attrib={"type": "list"})
            for value in data:  # type: ignore
                child = XMLParser._parse_json_data_to_etree(value)
                element.append(child)
            return element
        elif item_type is XMLElementType.STRING:
            return etree.Element("ITEM", attrib={"type": "string", "value": data})  # type: ignore
        elif item_type is XMLElementType.INTEGER:
            return etree.Element(
                "ITEM", attrib={"type": "integer", "value": json.dumps(data)}
            )
        elif item_type is XMLElementType.FLOAT:
            return etree.Element(
                "ITEM", attrib={"type": "float", "value": json.dumps(data)}
            )
        elif item_type is XMLElementType.BOOLEAN:
            return etree.Element(
                "ITEM", attrib={"type": "boolean", "value": json.dumps(data)}
            )
        elif item_type is XMLElementType.NULL:
            return etree.Element("ITEM", attrib={"type": "null"})
        else:
            raise ValueError("Invalid JSON format")

    @staticmethod
    def parse_file(file: Any) -> JSONType:
        """
        Parses XML file to JSONType object
        :param file:
        :return:
        """
        xml_parsed = parse(file)
        return XMLParser._parse_etree_to_json_type(node=xml_parsed.getroot())

    @staticmethod
    def parse_json(data: JSONType) -> _Element:
        """
        Parses JSON string to JSONType object
        :param data: JSONType data
        :return: etree.Element
        """
        return XMLParser._parse_json_data_to_etree(data)
