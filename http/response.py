import json
import xml.etree.ElementTree as ET
from typing import Any, Optional, Dict
from azure.functions import HttpResponse


class ToJSON:
    def __init__(self, content: Optional[Dict[str, Any]] = None):
        self.content = content

    def __call__(self):
        self.content = self.content if self.content is not None else {}

    def parse_content(self) -> str:
        return json.dumps(self.content)


class ToXML:
    def __init__(self, content: Optional[Dict[str, Any]] = None):
        self.content = content

    def __call__(self):
        self.content = self.content if self.content is not None else {}

    def _parse_dict(self, parent_element: ET.Element, dictionary: Dict[str, Any]):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                child = ET.SubElement(parent_element, key)
                self._parse_dict(child, value)
            else:
                child = ET.SubElement(parent_element, key)
                child.text = str(value)

    def parse_content(self) -> str:
        root = ET.Element("response")
        self._parse_dict(root, self.content)
        return ET.tostring(root, encoding="utf-8").decode("utf-8")


class JSONResponse:
    def __new__(cls, data: Optional[Any] = None, status_code: int = 200, *args, **kargs) -> HttpResponse:
        instance = super(JSONResponse, cls).__new__(cls)
        instance.data = data
        instance.status_code = status_code
        return instance.to_http_response(*args, **kargs)

    def to_json(self) -> str:
        return ToJSON(self.data).parse_content()

    def to_http_response(self, *args, **kargs) -> HttpResponse:
        return HttpResponse(body=self.to_json(), status_code=self.status_code, mimetype="application/json", *args, **kargs)


class XMLResponse:
    def __new__(cls, data: Optional[Any] = None, status_code: int = 200, *args, **kargs) -> HttpResponse:
        instance = super(XMLResponse, cls).__new__(cls)
        instance.data = data
        instance.status_code = status_code
        return instance.to_http_response(*args, **kargs)

    def to_xml(self) -> str:
        return ToXML(self.data).parse_content()

    def to_http_response(self, *args, **kargs) -> HttpResponse:
        return HttpResponse(body=self.to_xml(), status_code=self.status_code, mimetype="application/xml", *args, **kargs)
