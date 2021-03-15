import json
import time

from specs.genres.Genres import Genres


class TGenresPost(Genres):

    def test_genres_add_new(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_genre = api_ops.post(url=TGenresPost.path, json={
            "name": "The Chum's Genre " + str(round(time.time() * 1000)),
        })
        assert new_genre.status_code == 201
        response = api_ops.get(TGenresPost.path + '/' + str(json.loads(new_genre.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='genres',
            method='get_by_id'
        ) == True
        assert json_schema_validator.validate(
            json_str=new_genre.content,
            endpoint='genres',
            method='get_by_id'
        ) == True

    def test_genres_add_new_with_existing_name(self, api_ops, json_schema_validator):
        # Precondition: Having a genre with a specific name
        genre_name = "The Chum's Genre " + str(round(time.time() * 1000))
        new_genre = api_ops.post(url=TGenresPost.path, json={
            "name": genre_name,
        })
        assert new_genre.status_code == 201
        response = api_ops.get(TGenresPost.path + '/' + str(json.loads(new_genre.content)['id']))
        assert response.status_code == 200

        # Test: We couldn't create a new one with the same name
        fail_genre = api_ops.post(url=TGenresPost.path, json={
            "name": genre_name,
        })
        assert json_schema_validator.validate(
            json_str=fail_genre.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(fail_genre.content)['message']).lower() == "validation failed: name has already been taken"

    def test_genres_add_new_empty_name(self, api_ops, json_schema_validator):
        # Test: We couldn't create a new one with a blank name
        fail_genre = api_ops.post(url=TGenresPost.path, json={
            "name": "",
        })
        assert json_schema_validator.validate(
            json_str=fail_genre.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(fail_genre.content)['message']).lower() == "validation failed: name can't be blank"

    def test_genres_add_new_without_name(self, api_ops, json_schema_validator):
        # Test: We couldn't create a new one with a blank name
        fail_genre = api_ops.post(url=TGenresPost.path, json={
            "name": None,
        })
        assert json_schema_validator.validate(
            json_str=fail_genre.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(fail_genre.content)['message']).lower() == "validation failed: name can't be blank"