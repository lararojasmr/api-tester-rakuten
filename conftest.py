
def pytest_addoption(parser):
    parser.addoption(
        "--baseurl", help="Specify the API base URL"
    )
    parser.addoption(
        "--apiversion", help="Specify the API Version including 'v'. Example: v1"
    )

from fixtures.connector import api_ops
from fixtures.json_schema_validator import json_schema_validator