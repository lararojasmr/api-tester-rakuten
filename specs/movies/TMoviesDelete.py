import json
import time

from specs.movies.Movies import Movies


class TMoviesDelete(Movies):

    def test_movies_delete_correctly(self, api_ops, json_schema_validator):
        # Precondition: We have and movie add in the system
        new_movie = api_ops.post(url=TMoviesDelete.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 1542955,
            "duration": 130,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 201
        new_movie_id = str(json.loads(new_movie.content)['id'])

        response = api_ops.get(TMoviesDelete.path + '/' + new_movie_id)
        assert response.status_code == 200
        response = api_ops.delete(TMoviesDelete.path + '/' + new_movie_id)
        assert response.status_code == 204
        response = api_ops.get(TMoviesDelete.path + '/' + new_movie_id)
        assert response.status_code == 404
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='error'
        ) == True
        assert str(json.loads(response.content)['message']).lower() == "couldn't find movie with 'id'=" + new_movie_id
