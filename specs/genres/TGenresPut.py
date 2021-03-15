import json
import time

from specs.genres.Genres import Genres


class TGenresPut(Genres):

    def test_genres_change_without_name(self, api_ops, json_schema_validator):
        # Precondition: Having a genre with a specific name
        genre_name = "The Chum's Genre " + str(round(time.time() * 1000))
        new_genre = api_ops.post(url=TGenresPut.path, json={
            "name": genre_name,
        })
        assert new_genre.status_code == 201
        genre_id = str(json.loads(new_genre.content)['id'])
        response = api_ops.get(TGenresPut.path + '/' + genre_id)
        assert response.status_code == 200

        # Test: We couldn't create a new one with the same name
        edited_genre = api_ops.put(url=TGenresPut.path + '/' + genre_id, json={
            "name": None,
        })
        assert json_schema_validator.validate(
            json_str=edited_genre.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(edited_genre.content)['message']).lower() == "validation failed: name can't be blank"

    def test_genres_change_name_to_empty(self, api_ops, json_schema_validator):
        # Precondition: Having a genre with a specific name
        genre_name = "The Chum's Genre " + str(round(time.time() * 1000))
        new_genre = api_ops.post(url=TGenresPut.path, json={
            "name": genre_name,
        })
        assert new_genre.status_code == 201
        genre_id = str(json.loads(new_genre.content)['id'])
        response = api_ops.get(TGenresPut.path + '/' + genre_id)
        assert response.status_code == 200

        # Test: We couldn't create a new one with the same name

        edited_genre = api_ops.put(url=TGenresPut.path + '/' + genre_id, json={
            "name": "",
        })
        assert json_schema_validator.validate(
            json_str=edited_genre.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(edited_genre.content)['message']).lower() == "validation failed: name can't be blank"

    def test_genres_change_name_with_existing(self, api_ops, json_schema_validator):
        # Precondition: Having a genre with a specific name
        genre_name = "The Chum's Genre "
        new_genre = api_ops.post(url=TGenresPut.path, json={
            "name": genre_name + str(round(time.time() * 1000)),
        })
        assert new_genre.status_code == 201
        genre_id = str(json.loads(new_genre.content)['id'])
        response = api_ops.get(TGenresPut.path + '/' + genre_id)
        assert response.status_code == 200

        # Test:
        # Create a new genre to ensure that we have one used name
        genre_name = "The Chum's Genre " + str(round(time.time() * 1000))
        new_genre = api_ops.post(url=TGenresPut.path, json={
            "name": genre_name,
        })
        # Try to update the name with and existing one
        edited_genre = api_ops.put(url=TGenresPut.path + '/' + genre_id, json={
            "name": genre_name,
        })
        assert json_schema_validator.validate(
            json_str=edited_genre.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(edited_genre.content)['message']).lower() == "validation failed: name has already been taken"
