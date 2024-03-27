from typing import Any, Dict


class ToJSON:
    @staticmethod
    def parse_content(content: Dict[str, Any]) -> str:
        import json
        if content is None: return ""
        if not isinstance(content, dict): raise ValueError(f"Content must be a dictionary, not {type(content)}")
        return json.dumps(content)

class ToXML:
    @staticmethod
    def parse_content(content: Dict[str, Any]) -> str:
        import xmltodict
        if content is None: return ""
        if not isinstance(content, dict): raise ValueError(f"Content must be a dictionary, not {type(content)}")
        return xmltodict.unparse(content)
