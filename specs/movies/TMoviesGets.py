import json
import time

from specs.movies.Movies import Movies


class TMoviesGets(Movies):

    # This test just verify that the isolate get response
    # endpoint: /movies
    def test_movies_get_isolate(self, api_ops, json_schema_validator):
        response = api_ops.get(TMoviesGets.path)
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get'
        ) == True

    # This test check that the pagination works
    # endpoint: /movies?page={number}
    def test_movies_get_pagination(self, api_ops, json_schema_validator):
        response = api_ops.get(TMoviesGets.path + '?page=2')
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get'
        ) == True
        assert json.loads(response.content)['meta']['page'] == 2

    # This test check that the pagination works
    # endpoint: /movies?page={negative_number}
    def test_movies_get_pagination_negative_page(self, api_ops):
        response = api_ops.get(TMoviesGets.path + '?page=-2')
        assert response.status_code == 200

    # This test check that the pagination works
    # endpoint: /movies?page={character}
    def test_movies_get_pagination_character_page(self, api_ops):
        response = api_ops.get(TMoviesGets.path + '?page=a')
        assert response.status_code == 200

    # This test check that the number of items in the collection can be change and works as expected
    # endpoint: /movies?per_page={number}
    def test_movies_get_pagination_per_page(self, api_ops, json_schema_validator):
        response = api_ops.get(TMoviesGets.path + '?per_page=10')
        json_content = json.loads(response.content)

        assert response.status_code == 200
        assert json_content['meta']['per_page'] == 10
        assert len(json_content['collection']) == 10

        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get'
        ) == True

    # This test check that the number of items in the collection can be change and works as expected
    # endpoint: /movies?per_page={negative_number}
    def test_movies_get_pagination_negative_per_page(self, api_ops):
        response = api_ops.get(TMoviesGets.path + '?per_page=-1')
        assert response.status_code == 200

    # This test check that the number of items in the collection can be change and works as expected
    # endpoint: /movies?per_page={character}
    def test_movies_get_pagination_character_per_page(self, api_ops):
        response = api_ops.get(TMoviesGets.path + '?per_page=a')
        assert response.status_code == 200

    # This test verify that the endpoint to get a movie by id works
    # endpoint: /movies/{id:number}
    def test_movies_get_item_by_id(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        movie = api_ops.post(url=TMoviesGets.path, json={
            "title": "the chum - testing movie" + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 2,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        # Test
        response = api_ops.get(TMoviesGets.path + '/' + str(json.loads(movie.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get_by_id'
        ) == True

    # This test verify that the endpoint to get a movie by wrong id was validated
    # endpoint: /movies/{id:number}
    def test_movies_get_item_by_wrong_id(self, api_ops, json_schema_validator):
        response = api_ops.get(TMoviesGets.path + '/fake_id')
        assert response.status_code == 404
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='error'
        ) == True
        assert str(json.loads(response.content)['message']).lower() == "couldn't find movie with 'id'=fake_id"
