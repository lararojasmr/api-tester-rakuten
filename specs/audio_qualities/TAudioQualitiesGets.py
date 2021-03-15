import json
import time

from specs.audio_qualities.AudioQualities import AudioQualities


class TAudioQualities(AudioQualities):

    def test_audio_qualities_get_isolate(self, api_ops, json_schema_validator):
        response = api_ops.get(TAudioQualities.path)
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='get'
        ) == True

    def test_audio_qualities_get_pagination(self, api_ops, json_schema_validator):
        response = api_ops.get(TAudioQualities.path + '?page=2')
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='get'
        ) == True
        assert json.loads(response.content)['meta']['page'] == 2

    def test_audio_qualities_get_pagination_negative_page(self, api_ops):
        response = api_ops.get(TAudioQualities.path + '?page=-2')
        assert response.status_code == 200

    def test_audio_qualities_get_pagination_character_page(self, api_ops):
        response = api_ops.get(TAudioQualities.path + '?page=a')
        assert response.status_code == 200

    def test_audio_qualities_get_pagination_per_page(self, api_ops, json_schema_validator):
        response = api_ops.get(TAudioQualities.path + '?per_page=10')
        json_content = json.loads(response.content)

        assert response.status_code == 200
        assert json_content['meta']['per_page'] == 10
        assert len(json_content['collection']) == 10

        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='get'
        ) == True

    def test_audio_qualities_get_pagination_negative_per_page(self, api_ops):
        response = api_ops.get(TAudioQualities.path + '?per_page=-1')
        assert response.status_code == 200

    def test_audio_qualities_get_pagination_character_per_page(self, api_ops):
        response = api_ops.get(TAudioQualities.path + '?per_page=a')
        assert response.status_code == 200

    def test_audio_qualities_get_item_by_id(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        quality = api_ops.post(url=TAudioQualities.path, json={
            "name": "The chum quality " + str(round(time.time() * 1000)),
            "abbr": "The chum quality abbr " + str(round(time.time() * 1000))
        })
        # Test
        response = api_ops.get(TAudioQualities.path + '/' + str(json.loads(quality.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='get_by_id'
        ) == True

    def test_audio_qualities_get_item_by_wrong_id(self, api_ops, json_schema_validator):
        response = api_ops.get(TAudioQualities.path + '/fake_id')
        assert response.status_code == 404
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(response.content)['message']).lower() == "couldn't find audioquality with 'id'=fake_id"
