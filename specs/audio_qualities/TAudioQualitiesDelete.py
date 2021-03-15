import json
import time

from specs.audio_qualities.AudioQualities import AudioQualities


##
# This class could contains more test cases that make a relation
# between the genres and movies. ex. you shouldn't delete a genre
# if exist any movie with that genre in "genres" list. But
# there is a test that indicate that you can add a genre, video_qualities,
# and audio_qualities to a movie, then, right now this test-case is not
# useful.
#
# Put off this implementation to a next iteration.
##

class TAudioQualitiesDelete(AudioQualities):

    def test_audio_qualities_delete_existing_genres(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        time_first = str(round(time.time() * 1000))
        quality_one = api_ops.post(url=TAudioQualitiesDelete.path, json={
            "name": "chum_quality_name_" + time_first,
            "abbr": "chum_abbr_" + time_first,
            "position": 99,
            "default": False
        })
        assert quality_one.status_code == 201
        response = api_ops.get(TAudioQualitiesDelete.path + '/' + str(json.loads(quality_one.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='get_by_id'
        ) == True

        id = str(json.loads(response.content)['id'])
        # Delete this genre
        response = api_ops.delete(TAudioQualitiesDelete.path + '/' + id)
        assert response.status_code == 204

        response = api_ops.get(TAudioQualitiesDelete.path + '/' + id)
        assert response.status_code == 404

        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='audio_qualities',
            method='error'
        ) == True
        assert str(json.loads(response.content)['message']).lower() == "couldn't find audioquality with 'id'=" + id
