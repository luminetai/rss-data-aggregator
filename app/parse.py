import xml.etree.ElementTree as ET
from typing import List, Dict

class ParserError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class Parser:
    @staticmethod
    def execute (xml_data: str, field_to_tags_mapping: Dict[str, List[str]]) -> List[Dict[str, List[str]]]:
        try:
            root = ET.fromstring(xml_data)
            items = root.findall(".//item")
            
            parsed_data = []
            for item in items:
                parsed_item = {}
                for field_name, tags in field_to_tags_mapping.items():
                    values = []
                    for tag in tags:
                        elements = item.findall(tag)
                        values.extend(el.text for el in elements if el.text)
                    parsed_item[field_name] = values
                
                parsed_data.append(parsed_item)
            
            return parsed_data
        except ET.ParseError as e:
            raise ParseError(f"Failed to parse XML data: {e}")
        except Exception as e:
            raise ParseError(f"Unexpected error occurred while parsing XML data: {e}")