import json
from enum import Enum
from typing import Any, Dict, Optional, Union

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

    def parse_element_value(self, value: Optional[str]) -> Any:
        # element value validation check
        if value is None:
            if self is XMLElementType.NULL:
                return None
            elif self is XMLElementType.OBJECT:
                # edge case -> when json looks like {}, we do not want to return "null", but <item type="object"/>
                return {}
            else:
                raise ValueError("Invalid XML file schema")

        # element type validation check
        if self is XMLElementType.STRING:
            return value
        elif self is XMLElementType.INTEGER:
            return int(value)
        elif self is XMLElementType.FLOAT:
            return float(value)
        elif self is XMLElementType.BOOLEAN:
            return value == "true"
        else:
            raise NotImplementedError(f"Etree element type not supported: {self.value}")


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

        return element_type.parse_element_value(element_value)

    @staticmethod
    def _parse_etree_to_json_type(node: _Element) -> JSONType:
        """
        Converts lxml.etree.ElementTree to a :type JSONType.
        :param node: etree node
        :return: JSONType
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
        Converts a :type JSONType to lxml.etree.ElementTree.
        :param data: JSONType data
        :return: lxml.etree.ElementTree
        """
        element_type = XMLElementType.from_value(data)
        element = etree.Element("ITEM", attrib={"type": element_type.value})
        element_value: Optional[str] = None

        # Set element children and value based on the type of the item
        # if the element is an object, then assign children to element keys recursively
        if element_type is XMLElementType.OBJECT:
            for key, value in data.items():  # type: ignore
                child = XMLParser._parse_json_data_to_etree(value)
                child.set("key", key)
                element.append(child)
        # if the element is a list, then append children to element
        elif element_type is XMLElementType.LIST:
            for value in data:  # type: ignore
                child = XMLParser._parse_json_data_to_etree(value)
                element.append(child)
        # if the element type is a string leaf, then set the value of the element
        elif element_type is XMLElementType.STRING:
            element_value = data  # type: ignore
        # if the element type is a leaf and not a string, then set the json-dumped value of the element
        elif element_type in [
            XMLElementType.INTEGER,
            XMLElementType.FLOAT,
            XMLElementType.BOOLEAN,
        ]:
            element_value = json.dumps(data)
        # if the element type is null, then do not set the value of the element
        elif element_type is XMLElementType.NULL:
            pass
        # if the element type is not one of above type, then raise an error
        else:
            raise NotImplementedError("Unsupported type for parsing")

        if element_value is not None:
            element.set("value", element_value)

        return element

    @staticmethod
    def parse_xml_from_file(file: Any) -> JSONType:
        """
        Parses XML file to JSONType object
        :param file:
        :return:
        """
        xml_parsed = parse(file)
        return XMLParser._parse_etree_to_json_type(node=xml_parsed.getroot())

    @staticmethod
    def parse_xml_from_json(data: JSONType) -> _Element:
        """
        Parses JSON string to JSONType object
        :param data: JSONType data
        :return: etree.Element
        """
        return XMLParser._parse_json_data_to_etree(data)
