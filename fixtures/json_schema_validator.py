import pytest
import argparse
from src.SchemaValidator import SchemaValidator


@pytest.fixture(scope="session", autouse=True)
def json_schema_validator():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apiversion')
    args = parser.parse_known_args()[0]
    return SchemaValidator(api_version=args.apiversion)
