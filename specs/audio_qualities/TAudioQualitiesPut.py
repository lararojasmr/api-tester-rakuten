import json
import time

from specs.audio_qualities.AudioQualities import AudioQualities


class TAudioQualitiesPut(AudioQualities):

    def test_audio_qualities_not_change_with_existing_name(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_name = "The Chum's Quality " + str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesPut.path, json={
            "name": quality_name,
            "abbr": "TCQ " + str(round(time.time() * 1000))
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200

        quality_two_abbr = "TCQ " + str(round(time.time() * 1000))
        quality_two = api_ops.post(url=TAudioQualitiesPut.path, json={
            "name": quality_name + 'new',
            "abbr": quality_two_abbr
        })
        assert quality_two.status_code == 201
        quality_two_obj = json.loads(quality_one.content)
        quality_two = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_two_obj['id']))
        assert quality_two.status_code == 200

        # Try to update with and existing test case
        quality_two_edited = api_ops.put(url=TAudioQualitiesPut.path, json={
            "name": quality_name,
            "abbr": quality_two_abbr
        })

        assert json_schema_validator.validate(
            json_str=quality_two_edited.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(
            json.loads(quality_two_edited.content)['message']
        ).lower() == "validation failed: name has already been taken"

    def test_audio_qualities_not_change_with_existing_abbr(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_abbr = "TCQ " + str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesPut.path, json={
            "name": "The Chum's Quality " + str(round(time.time() * 1000)),
            "abbr": quality_abbr
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200

        quality_two_name = "The Chum's Quality " + str(round(time.time() * 1000))
        quality_two = api_ops.post(url=TAudioQualitiesPut.path, json={
            "name": quality_two_name,
            "abbr": quality_abbr + "new"
        })
        assert quality_two.status_code == 201
        quality_two_obj = json.loads(quality_one.content)
        quality_two = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_two_obj['id']))
        assert quality_two.status_code == 200

        # Try to update with and existing test case
        quality_two_edited = api_ops.put(url=TAudioQualitiesPut.path, json={
            "name": quality_two_name,
            "abbr": quality_abbr
        })

        assert json_schema_validator.validate(
            json_str=quality_two_edited.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(
            json.loads(quality_two_edited.content)['message']
        ).lower() == "validation failed: abbr has already been taken"

    def test_audio_qualities_not_change_without_name(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_abbr = "TCQ " + str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesPut.path, json={
            "name": "The Chum's Quality " + str(round(time.time() * 1000)),
            "abbr": quality_abbr
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200

        # Try to update with a non name
        quality_one_edited = api_ops.put(url=TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']), json={
            "name": None,
            "abbr": quality_abbr
        })

        assert json_schema_validator.validate(
            json_str=quality_one_edited.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(
            json.loads(quality_one_edited.content)['message']
        ).lower() == "validation failed: name can't be blank"

    def test_audio_qualities_not_change_without_abbr(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        quality_name = "The Chum's Quality " + str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesPut.path, json={
            "name": quality_name,
            "abbr": "TCQ " + str(round(time.time() * 1000))
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200

        # Try to update with a non name
        quality_one_edited = api_ops.put(url=TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']), json={
            "name": quality_name,
            "abbr": None
        })

        assert json_schema_validator.validate(
            json_str=quality_one_edited.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(
            json.loads(quality_one_edited.content)['message']
        ).lower() == "validation failed: abbr can't be blank"

    def test_audio_qualities_change_record_parameters(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system with default
        time_first = str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesPut.path, json={
            "name": "chum_quality_name_" + time_first,
            "abbr": "chum_abbr_" + time_first,
            "position": 99,
            "default": False
        })
        assert quality_one.status_code == 201
        quality_one_obj = json.loads(quality_one.content)
        quality_one = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']))
        assert quality_one.status_code == 200
        quality_one_obj = json.loads(quality_one.content)

        # Try to update with a non name
        quality_one_edited = api_ops.put(url=TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']), json={
            "name": "edited_chum_quality_name_" + time_first,
            "abbr": "edited_chum_abbr_" + time_first,
            "position": None,
            "default": True
        })
        assert quality_one_edited.status_code == 204

        quality_one_edited = api_ops.get(TAudioQualitiesPut.path + '/' + str(quality_one_obj['id']))
        assert quality_one_edited.status_code == 200
        quality_one_edited_obj = json.loads(quality_one_edited.content)

        assert quality_one_edited_obj['name'] == "edited_chum_quality_name_" + time_first
        assert quality_one_edited_obj['abbr'] == "edited_chum_abbr_" + time_first
        assert quality_one_edited_obj['position'] is None
        assert quality_one_edited_obj['default'] is True

        assert json_schema_validator.validate(
            json_str=quality_one_edited.content,
            endpoint='audio_qualities',
            method='get_by_id'
        ) == True
