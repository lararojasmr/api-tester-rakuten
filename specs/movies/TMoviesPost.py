import json
import time

from specs.audio_qualities.AudioQualities import AudioQualities
from specs.genres.Genres import Genres
from specs.movies.Movies import Movies
from specs.movies.TMoviesGets import TMoviesGets
from specs.video_qualities.VideoQualities import VideoQualities


class TMoviesPost(Movies):

    # This test verify that a movie can be created using default values (all right)
    # endpoint: /movies
    def test_movies_create_movie_happy_path(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 201
        response = api_ops.get(TMoviesPost.path + '/' + str(json.loads(new_movie.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='get_by_id'
        ) == True

    # This test verify that a movie can be created without title
    # endpoint: /movies
    def test_movies_create_movie_without_name(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": None,
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 422
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='error'
        ) == True
        assert str(json.loads(new_movie.content)['message']).lower() == "validation failed: title can't be blank"

    # This test verify that a movie can be created empty title
    # endpoint: /movies
    def test_movies_create_movie_empty_name(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "",
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 422
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='error'
        ) == True
        assert str(json.loads(new_movie.content)['message']).lower() == "validation failed: title can't be blank"

    # This test verify that a movie can be created without year}
    # endpoint: /movies
    def test_movies_create_movie_without_year(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie" + str(round(time.time() * 1000)),
            "year": None,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 422
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='error'
        ) == True
        assert str(json.loads(new_movie.content)['message']).lower() == "validation failed: year can't be blank"

    # This test verify that a movie can be created and the plot always is cast to string
    # endpoint: /movies
    def test_movies_create_movie_cast_plot(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 1542955,
            "duration": 90,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 201
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        assert type(json.loads(new_movie.content)['plot']) == str

    # This test verify that a movie can be created and the duration is not a number
    # endpoint: /movies
    def test_movies_create_movie_duration_is_not_a_number(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 1542955,
            "duration": 'It is not a number',
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 422
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='error'
        ) == True
        assert str(json.loads(new_movie.content)['message']).lower() == "validation failed: duration must be blank"

    # The test verify if after saved a movie with video qualities it are saved
    def test_movies_create_movie_with_some_video_qualities(self, api_ops, json_schema_validator):
        # Precondition: We have a several video_qualities registered
        video_qualities = []
        videos_to_create = 2
        for i in range(videos_to_create):
            video_qualities.append(
                json.loads(api_ops.post(VideoQualities.path, json={
                    "name": "video_chum_name " + str(i) + '_' + str(round(time.time() * 1000)),
                    "abbr": "video_chum_" + str(i) + '_' + str(round(time.time() * 1000))
                }).content)['id']
            )

        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 1542955,
            "duration": 'It is not a number',
            "audio_qualities": [],
            "video_qualities": video_qualities,
            "genres": []
        })

        print(TMoviesGets.path + '/' + str(json.loads(new_movie.content)['id']))
        movie_saved = api_ops.get(TMoviesGets.path + '/' + str(json.loads(new_movie.content)['id']))
        video_qualities_from_record = json.loads(movie_saved.content)['video_qualities']

        # Assertions
        assert json_schema_validator.validate(
            json_str=movie_saved.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        # Verifying the Type
        assert type(video_qualities_from_record) == list
        # Verifying Length
        assert len(video_qualities_from_record) == len(video_qualities)
        # Verify the IDs registered
        for video_quality in video_qualities_from_record:
            assert video_quality['id'] in video_qualities

    # The test verify if after saved a movie with audio qualities it are saved
    def test_movies_create_movie_with_some_audio_qualities(self, api_ops, json_schema_validator):
        # Precondition: We have a several audio_qualities registered
        audio_qualities = []
        audios_to_create = 2
        for i in range(audios_to_create):
            audio_qualities.append(
                json.loads(api_ops.post(AudioQualities.path, json={
                    "name": "audio_chum_name " + str(i) + '_' + str(round(time.time() * 1000)),
                    "abbr": "audio_chum_" + str(i) + '_' + str(round(time.time() * 1000))
                }).content)['id']
            )

        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 1542955,
            "duration": 'It is not a number',
            "audio_qualities": audio_qualities,
            "video_qualities": [],
            "genres": []
        })

        print(TMoviesGets.path + '/' + str(json.loads(new_movie.content)['id']))
        movie_saved = api_ops.get(TMoviesGets.path + '/' + str(json.loads(new_movie.content)['id']))
        audio_qualities_from_record = json.loads(movie_saved.content)['audio_qualities']

        # Assertions
        assert json_schema_validator.validate(
            json_str=movie_saved.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        # Verifying the Type
        assert type(audio_qualities_from_record) == list
        # Verifying Length
        assert len(audio_qualities_from_record) == len(audio_qualities)
        # Verify the IDs registered
        for audio_quality in audio_qualities_from_record:
            assert audio_quality['id'] in audio_qualities

    # The test verify if after saved a movie with genres it are saved
    def test_movies_create_movie_with_some_genres(self, api_ops, json_schema_validator):
        # Precondition: We have a several genres registered
        genres_ids = []
        genres_to_create = 2
        for i in range(genres_to_create):
            genres_ids.append(
                json.loads(api_ops.post(Genres.path, json={
                    "name": "genres_chum_name " + str(i) + '_' + str(round(time.time() * 1000)),
                }).content)['id']
            )

        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 1542955,
            "duration": 12,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": genres_ids
        })

        print(TMoviesGets.path + '/' + str(json.loads(new_movie.content)['id']))
        movie_saved = api_ops.get(TMoviesGets.path + '/' + str(json.loads(new_movie.content)['id']))
        genres_from_record = json.loads(movie_saved.content)['genres']

        # Assertions
        assert json_schema_validator.validate(
            json_str=movie_saved.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        # Verifying the Type
        assert type(genres_from_record) == list
        # Verifying Length
        assert len(genres_from_record) == len(genres_ids)
        # Verify the IDs registered
        for genre in genres_from_record:
            assert genre['id'] in genres_ids

    # The test verify if one movie can be registered using just the required fields
    def test_movies_create_movie_with_minimun_fields(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021
        })
        assert new_movie.status_code == 201
        response = api_ops.get(TMoviesPost.path + '/' + str(json.loads(new_movie.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='get_by_id'
        ) == True

        # Genres
        response_json = json.loads(response.content)
        # Verifying the Type
        assert type(response_json['genres']) == list
        # Verifying Length
        assert len(response_json['genres']) == 0

        # Audio Qualities
        response_json = json.loads(response.content)
        # Verifying the Type
        assert type(response_json['audio_qualities']) == list
        # Verifying Length
        assert len(response_json['audio_qualities']) == 0

        # Video Qualities
        response_json = json.loads(response.content)
        # Verifying the Type
        assert type(response_json['video_qualities']) == list
        # Verifying Length
        assert len(response_json['video_qualities']) == 0

    # The test verify if two movies can be registered using the same name
    def test_movies_create_two_movie_with_same_name(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        name = "The Chum's Movie " + str(round(time.time() * 1000));
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": name,
            "year": 2021
        })
        assert new_movie.status_code == 201
        response = api_ops.get(TMoviesPost.path + '/' + str(json.loads(new_movie.content)['id']))
        assert response.status_code == 200

        new_movie_same_name = api_ops.post(url=TMoviesPost.path, json={
            "title": name,
            "year": 2021
        })
        assert new_movie.status_code == 422
        assert json_schema_validator.validate(
            json_str=new_movie_same_name.content,
            endpoint='movies',
            method='error'
        ) == True
        error_message = str(json.loads(new_movie.content)['message']).lower()
        assert error_message == "validation failed: title has already been taken"

    # This test verify that a movie can be created using wrongs ids to genres, audio and video
    # endpoint: /movies
    def test_movies_create_movie_wrong_genres_video_audio_id(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": ['not_valid_id'],
            "video_qualities": ['not_valid_id'],
            "genres": ['not_valid_id']
        })
        assert new_movie.status_code == 201
        response = api_ops.get(TMoviesPost.path + '/' + str(json.loads(new_movie.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='get_by_id'
        ) == True

    # This test verify that a movie can be created using type of values to audio, video y genres
    # The fields should be ignored or will be validated (it's depending on the schema and PM)
    # endpoint: /movies
    def test_movies_create_movie_wrong_type_of_fields(self, api_ops, json_schema_validator):
        # Precondition: We have and item add in the system
        new_movie = api_ops.post(url=TMoviesPost.path, json={
            "title": "The Chum's Movie " + str(round(time.time() * 1000)),
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": 1542,
            "video_qualities": 2542,
            "genres": 'i am the string'
        })
        assert new_movie.status_code == 201
        response = api_ops.get(TMoviesPost.path + '/' + str(json.loads(new_movie.content)['id']))
        assert response.status_code == 200
        assert json_schema_validator.validate(
            json_str=response.content,
            endpoint='movies',
            method='get_by_id'
        ) == True
        assert json_schema_validator.validate(
            json_str=new_movie.content,
            endpoint='movies',
            method='get_by_id'
        ) == True