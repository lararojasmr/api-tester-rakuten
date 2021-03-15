import json
import time

from specs.audio_qualities.AudioQualities import AudioQualities


class TAudioQualitiesPost(AudioQualities):

    def test_audio_qualities_add_new(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_quality = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "The Chum's AudioQuality " + str(round(time.time() * 1000)),
            "abbr": "TCAQ " + str(round(time.time() * 1000)),
        })
        assert new_quality.status_code == 201
        response = api_ops.get(TAudioQualitiesPost.path + '/' + str(json.loads(new_quality.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='get_by_id'
        ) == True
        assert json_schema_validator.validate(
            json_str=new_quality.content,
            endpoint='audio_qualities',
            method='get_by_id'
        ) == True

    # This test case try to verify if the default value is update after create a new default record.
    # Creating two records default the last-one should be default and the first one not.
    def test_audio_qualities_add_new_default(self, api_ops):
        # Precondition: We have and item add in the system with default
        quality_one = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "The Chum's Quality " + str(round(time.time() * 1000)),
            "abbr": "TCAQ " + str(round(time.time() * 1000)),
            "default": True
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPost.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200
        assert quality_one_obj['default'] == True

        # Create a new default records
        quality_two = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "The Chum's AudioQuality " + str(round(time.time() * 1000)),
            "abbr": "TCAQ " + str(round(time.time() * 1000)),
            "default": True
        })
        assert quality_two.status_code == 201
        quality_two_obj = json.loads(quality_one.content)
        quality_two = api_ops.get(TAudioQualitiesPost.path + '/' + str(quality_two_obj['id']))
        assert quality_two.status_code == 200
        assert quality_two_obj['default'] == True

        # Get the first record created and check the default property
        quality_one = api_ops.get(TAudioQualitiesPost.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200
        assert quality_one_obj['default'] == False

    def test_audio_qualities_add_new_name_empty(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_one = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "",
            "abbr": "TCAQ " + str(round(time.time() * 1000))
        })
        assert quality_one.status_code == 422
        assert json_schema_validator.validate(
            json_str=quality_one.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(quality_one.content)['message']).lower() == "validation failed: name can't be blank"

    def test_audio_qualities_add_new_without_name(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_one = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": None,
            "abbr": "TCAQ " + str(round(time.time() * 1000))
        })
        assert quality_one.status_code == 422
        assert json_schema_validator.validate(
            json_str=quality_one.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(quality_one.content)['message']).lower() == "validation failed: name can't be blank"

    def test_audio_qualities_add_new_abbr_empty(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_one = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "The Chum's AudioQuality " + str(round(time.time() * 1000)),
            "abbr": ""
        })
        assert quality_one.status_code == 422
        assert json_schema_validator.validate(
            json_str=quality_one.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(quality_one.content)['message']).lower() == "validation failed: abbr can't be blank"

    def test_audio_qualities_add_new_without_abbr(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_one = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "The Chum's AudioQuality " + str(round(time.time() * 1000)),
            "abbr": None
        })
        assert quality_one.status_code == 422
        assert json_schema_validator.validate(
            json_str=quality_one.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(quality_one.content)['message']).lower() == "validation failed: abbr can't be blank"

    def test_audio_qualities_add_new_unique_name(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_name = "The Chum's Quality " + str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": quality_name,
            "abbr": "TCQ " + str(round(time.time() * 1000))
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPost.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200

        # Test: Try to add a new one with the same name, the response should be different to 201
        # and the record shouldn't be saved
        quality_two = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": quality_name,
            "abbr": "TCQ " + str(round(time.time() * 1000))
        })
        assert quality_two.status_code != 201
        assert json_schema_validator.validate(
            json_str=quality_two.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(quality_two.content)['message']).lower() == "validation failed: name has already been taken"

    def test_audio_qualities_add_new_unique_abbr(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_abbr = "TCQ " + str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "The Chum's Quality " + str(round(time.time() * 1000)),
            "abbr": quality_abbr
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPost.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200

        # Test: Try to add a new one with the same name, the response should be different to 201
        # and the record shouldn't be saved
        quality_two = api_ops.post(url=TAudioQualitiesPost.path, json={
            "name": "The Chum's Quality " + str(round(time.time() * 1000)),
            "abbr": quality_abbr
        })
        assert quality_two.status_code != 201
        assert json_schema_validator.validate(
            json_str=quality_two.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(quality_two.content)['message']).lower() == "validation failed: abbr has already been taken"