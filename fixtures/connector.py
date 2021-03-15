import pytest
import argparse
from src.Connector import Connector


@pytest.fixture(scope="session", autouse=True)
def api_ops():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl')
    args = parser.parse_known_args()[0]
    return Connector(base_url=args.baseurl).api_connection()
