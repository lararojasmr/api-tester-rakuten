import json
import time

from specs.genres.Genres import Genres


class TGenresGet(Genres):

    # This test just verify that the isolate get response
    # endpoint: /genres
    def test_genres_get_isolate(self, api_ops, json_schema_validator):
        response = api_ops.get(TGenresGet.path)
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='genres',
            method='get'
        ) == True

    # This test check that the pagination works
    # endpoint: /movies?page={number}
    def test_genres_get_pagination(self, api_ops, json_schema_validator):
        response = api_ops.get(TGenresGet.path + '?page=2')
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='genres',
            method='get'
        ) == True
        assert json.loads(response.content)['meta']['page'] == 2

    # This test check that the pagination works
    # endpoint: /movies?page={negative_number}
    def test_genres_get_pagination_negative_page(self, api_ops):
        response = api_ops.get(TGenresGet.path + '?page=-2')
        assert response.status_code == 200

    # This test check that the pagination works
    # endpoint: /movies?page={character}
    def test_genres_get_pagination_character_page(self, api_ops):
        response = api_ops.get(TGenresGet.path + '?page=a')
        assert response.status_code == 200

    # This test check that the number of items in the collection can be change and works as expected
    # endpoint: /movies?per_page={number}
    def test_genres_get_pagination_per_page(self, api_ops, json_schema_validator):
        response = api_ops.get(TGenresGet.path + '?per_page=10')
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
    def test_genres_get_pagination_negative_per_page(self, api_ops):
        response = api_ops.get(TGenresGet.path + '?per_page=-1')
        assert response.status_code == 200

    # This test check that the number of items in the collection can be change and works as expected
    # endpoint: /movies?per_page={character}
    def test_genres_get_pagination_character_per_page(self, api_ops):
        response = api_ops.get(TGenresGet.path + '?per_page=a')
        assert response.status_code == 200

    # This test verify that the endpoint to get a movie by id works
    # endpoint: /movies/{id:number}
    def test_genres_get_item_by_id(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        genre = api_ops.post(url=TGenresGet.path, json={
            "name": "The chum genres " + str(round(time.time() * 1000))
        })
        # Test
        response = api_ops.get(TGenresGet.path + '/' + str(json.loads(genre.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='genres',
            method='get_by_id'
        ) == True

    # This test verify that the endpoint to get a movie by wrong id was validated
    # endpoint: /movies/{id:number}
    def test_genres_get_item_by_wrong_id(self, api_ops, json_schema_validator):
        response = api_ops.get(TGenresGet.path + '/fake_id')
        assert response.status_code == 404
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='genres',
            method='error'
        ) == True
        assert str(json.loads(response.content)['message']).lower() == "couldn't find genre with 'id'=fake_id"
