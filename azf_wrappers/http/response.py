from typing import Any, Optional
from azure.functions import HttpResponse

from .parser import ToJSON, ToXML


class JSONResponse:
    def __init__(self, data: Optional[Any] = None, status_code: int = 200):
        self.data, self.status_code = data, status_code

    def __new__(cls, data: Optional[Any] = None, status_code: int = 200, *args, **kargs) -> HttpResponse:
        instance = super(JSONResponse, cls).__new__(cls)
        instance.data = data
        instance.status_code = status_code
        return instance.to_http_response(*args, **kargs)

    def to_json(self) -> str: return ToJSON(self.data).parse_content()

    def to_http_response(self, *args, **kargs) -> HttpResponse:
        return HttpResponse(body=self.to_json(), status_code=self.status_code, mimetype="application/json", *args, **kargs)


class XMLResponse:
    def __init__(self, data: Optional[Any] = None, status_code: int = 200):
        self.data, self.status_code = data, status_code

    def __new__(cls, data: Optional[Any] = None, status_code: int = 200, *args, **kargs) -> HttpResponse:
        instance = super(XMLResponse, cls).__new__(cls)
        instance.data = data
        instance.status_code = status_code
        return instance.to_http_response(*args, **kargs)

    def to_xml(self) -> str: return ToXML(self.data).parse_content()

    def to_http_response(self, *args, **kargs) -> HttpResponse:
        return HttpResponse(body=self.to_xml(), status_code=self.status_code, mimetype="application/xml", *args, **kargs)


class BoolResponse:
    def __init__(self, data: bool = True, status_code: int = 200):
        self.data, self.status_code = data, status_code

    def __new__(cls, data: bool = True, status_code: int = 200, *args, **kargs) -> HttpResponse:
        instance = super(BoolResponse, cls).__new__(cls)
        instance.data = data
        instance.status_code = status_code
        return instance.to_http_response(*args, **kargs)

    def to_bool(self): return str(self.data)

    def to_http_response(self, *args, **kargs) -> HttpResponse:
        return HttpResponse(body=self.to_bool(), status_code=self.status_code, *args, **kargs)
