# azf-wrappers

Wrapper functions for expanding Python Azure functions SDK.

## Install

```shell
pip install -e .
```

## Usage

```python
import logging
import azure.functions as func
from azf_wrappers.http.response import JSONResponse, XMLResponse

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="example")
def example(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")
    res = req.params.get("res")
    if not res:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            res = req_body.get("res")
    if res:
        content = {"response_type": "XML", "level1": {"level2": {"level3": "hello"}}}
        return XMLResponse(content)
    else:
        content = {"response_type": "JSON", "level1": {"level2": {"level3": "hello"}}}
        return JSONResponse(content)
```
