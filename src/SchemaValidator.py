import json
import jsonschema
from jsonschema import validate


class SchemaValidator:

    def __init__(self, api_version):
        self.api_version = api_version

    def validate(self, json_str, endpoint, method):
        try:
            json_source = json.loads(json_str)
            schema_file_name = str(endpoint).lower() + '_' + str(method) + '.json'
            with open("schemas/" + self.api_version + '/' + schema_file_name, "r") as schema_file:
                schema_obj = json.load(schema_file)
                try:
                    validate(instance=json_source, schema=schema_obj)
                except jsonschema.exceptions.ValidationError as err:
                    return 'The JSON is not compatible with the schema. Error: ' + str(err)
        except ValueError as err:
            return 'The JSON returned by API is not valid. Error: ' + str(err)
        return True
