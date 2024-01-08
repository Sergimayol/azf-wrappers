import json
import xml.etree.ElementTree as ET
from typing import Any, Optional, Dict


class ToJSON:
    def __init__(self, content: Optional[Dict[str, Any]] = None):
        self.content = content if self.content is not None else {}

    def parse_content(self) -> str: return json.dumps(self.content)


class ToXML:
    def __init__(self, content: Optional[Dict[str, Any]] = None):
        self.content = content if self.content is not None else {}

    def _parse_dict(self, parent_element: ET.Element, dictionary: Dict[str, Any]):
        for key, value in dictionary.items():
            child = ET.SubElement(parent_element, key)
            if isinstance(value, dict):
                self._parse_dict(child, value)
            else:
                child.text = str(value)

    def parse_content(self) -> str:
        root = ET.Element("response")
        self._parse_dict(root, self.content)
        return ET.tostring(root, encoding="utf-8").decode("utf-8")
