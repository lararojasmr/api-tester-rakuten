from pytest_easy_api.client import ApiClient


class Connector:

    def __init__(self, base_url='https://protected-atoll-83840.herokuapp.com'):
        self.baseUrl = base_url

    def api_connection(self):
        print(self.baseUrl)
        return ApiClient(self.baseUrl)
