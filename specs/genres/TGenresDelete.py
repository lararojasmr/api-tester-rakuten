import json
import time

from specs.genres.Genres import Genres


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

class TGenresDelete(Genres):

    def test_genres_delete_existing_genres(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_genre = api_ops.post(url=TGenresDelete.path, json={
            "name": "The Chum's Genre " + str(round(time.time() * 1000)),
        })
        assert new_genre.status_code == 201
        response = api_ops.get(TGenresDelete.path + '/' + str(json.loads(new_genre.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='genres',
            method='get_by_id'
        ) == True

        genre_id = str(json.loads(response.content)['id'])
        # Delete this genre
        response = api_ops.delete(TGenresDelete.path + '/' + genre_id)
        assert response.status_code == 204

        response = api_ops.get(TGenresDelete.path + '/' + genre_id)
        assert response.status_code == 404

        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(response.content)['message']).lower() == "couldn't find genre with 'id'=" + genre_id
