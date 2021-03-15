import json
import time

from specs.audio_qualities.AudioQualities import AudioQualities
from specs.genres.Genres import Genres
from specs.movies.Movies import Movies
from specs.video_qualities.VideoQualities import VideoQualities


class TMoviesPut(Movies):

    def test_movie_update_fields_to_valid(self, api_ops, json_schema_validator):
        movie_name = "The Chum's Movie " + str(round(time.time() * 1000))
        new_movie = api_ops.post(url=TMoviesPut.path, json={
            "title": movie_name,
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 201
        movie_id = str(json.loads(new_movie.content)['id'])
        response = api_ops.get(TMoviesPut.path + '/' + movie_id)
        assert response.status_code == 200

        # Edit Title
        movie_obj = json.loads(new_movie.content)
        current = movie_obj['title']
        edited = current + '_edited'
        movie_obj['title'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 204
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['title'] == edited

        # Edit Year
        current = movie_obj['year']
        edited = current + 20
        movie_obj['year'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 204
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['year'] == edited

        # Edit Plot
        current = movie_obj['plot']
        edited = current + '_edited'
        movie_obj['plot'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 204
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['plot'] == edited

        # Edit Duration
        current = movie_obj['duration']
        edited = current + 20
        movie_obj['duration'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 204
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['duration'] == edited

        # Edit Audio Qualities
        audio_qualities = []
        audios_to_create = 2
        for i in range(audios_to_create):
            audio_qualities.append(
                json.loads(api_ops.post(AudioQualities.path, json={
                    "name": "audio_chum_name " + str(i) + '_' + str(round(time.time() * 1000)),
                    "abbr": "audio_chum_" + str(i) + '_' + str(round(time.time() * 1000))
                }).content)['id']
            )
        current = movie_obj['audio_qualities']
        edited = current + audio_qualities
        movie_obj['audio_qualities'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 204
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['audio_qualities'] == edited

        # Edit Video Qualities
        video_qualities = []
        videos_to_create = 2
        for i in range(videos_to_create):
            video_qualities.append(
                json.loads(api_ops.post(VideoQualities.path, json={
                    "name": "audio_chum_name " + str(i) + '_' + str(round(time.time() * 1000)),
                    "abbr": "audio_chum_" + str(i) + '_' + str(round(time.time() * 1000))
                }).content)['id']
            )
        current = movie_obj['video_qualities']
        edited = current + video_qualities
        movie_obj['video_qualities'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 204
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['video_qualities'] == edited

        # Edit Genres
        genres_ids = []
        genres_to_create = 2
        for i in range(genres_to_create):
            genres_ids.append(
                json.loads(api_ops.post(Genres.path, json={
                    "name": "genres_chum_name " + str(i) + '_' + str(round(time.time() * 1000)),
                }).content)['id']
            )

        current = movie_obj['genres']
        edited = current + genres_ids
        movie_obj['genres'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 204
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['genres'] == edited

        # This test verify that a movie can be created and the duration is not a number

    def test_movie_update_duration_is_not_a_number(self, api_ops, json_schema_validator):
        movie_name = "The Chum's Movie " + str(round(time.time() * 1000))
        new_movie = api_ops.post(url=TMoviesPut.path, json={
            "title": movie_name,
            "year": 2021,
            "plot": 'plot_message_to_test_api',
            "duration": 90,
            "audio_qualities": [],
            "video_qualities": [],
            "genres": []
        })
        assert new_movie.status_code == 201
        movie_id = str(json.loads(new_movie.content)['id'])
        response = api_ops.get(TMoviesPut.path + '/' + movie_id)
        assert response.status_code == 200

        # Edit Year
        movie_obj = json.loads(new_movie.content)
        current = movie_obj['year']
        edited = 'not a number'
        movie_obj['year'] = edited
        edited_movie = api_ops.put(url=TMoviesPut.path + '/' + movie_id, json=movie_obj)
        assert edited_movie.status_code == 422
        movie_obj = json.loads(api_ops.get(TMoviesPut.path + '/' + movie_id).content)
        assert movie_obj['year'] == current
