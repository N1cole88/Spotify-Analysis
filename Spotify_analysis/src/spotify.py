from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser
from urllib.parse import urlencode
import pandas as pd
from pandas import json_normalize
import database

class Spotify:
    def __init__(self, client_id, client_secret, token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.df = None

    def get_auth_header(self):
        return {"Authorization" : "Bearer " + self.token}


    def search_for_artist(self, artist_name):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header()
        query = f"?q={artist_name}&type=artist&limit=1"
        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)["artists"]["items"] 
        #print(json_result)
        if len(json_result) == 0:
            print("No artist with this name....")
            return None
        
        return json_result[0]


    def get_songs_by_artist(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["tracks"]
        return json_result

    def get_my_profile(self):
        url = f"https://api.spotify.com/v1/me"
        data = {"grant_type": "client_credentials"}
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)

        df = json_normalize(json_result)
        print(df)

        return json_result

    def getPlaylist(self):
        url = f"https://api.spotify.com/v1/me/playlists?limit=20&offset=0"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result

    def getPlaylistItems(self, limit, offset):
        url = f"https://api.spotify.com/v1/playlists/5Dww7ikBY4JDVUe5Csdpm8/tracks?limit={limit}&offset={offset}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["items"]
        return json_result

    def getNthPlaylistNumTotal(self, n):        
        total = self.getPlaylist()[n]["tracks"]["total"]
        return total

    def getArtistGenres(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["genres"]
        return json_result

    def getAudioFeatures(self, track_id):
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        headers = self.get_auth_header()
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        return json_result
    
    def getDefaultDataframe(self):
        total_num_of_songs = self.getNthPlaylistNumTotal(2)
        data_dict = {"track_id" : [], "track_name" : [], "album_name" : [],  "album_popularity" : [], "release_date": [], "artist_name" : [], "artist_genres" : [], "acousticness" : [], "danceability" : [], "energy": [], "instrumentalness" : [], "liveness" : [], "loudness" : [], "mode" : [], "speechiness" : [], "tempo" : [], "valence" : []}
        for n in range(total_num_of_songs // 100):
            tracks = self.getPlaylistItems(100, n * 100)
            for item in tracks:
                data_dict["track_id"].append(item["track"]["id"])
                data_dict["track_name"].append(item["track"]["name"])
                data_dict["album_name"].append(item["track"]["album"]["name"])
                data_dict["album_popularity"].append(item["track"]["popularity"])
                data_dict["release_date"].append(item["track"]["album"]["release_date"])
                data_dict["artist_name"].append(item["track"]["album"]["artists"][0]["name"])
                artist_genres = self.getArtistGenres(item["track"]["album"]["artists"][0]["id"])
                if len(artist_genres) == 0:
                    genres = "NaN"
                else:
                    genres = ",".join(artist_genres)
                data_dict["artist_genres"].append(genres)
                audio_features = self.getAudioFeatures(item["track"]["id"])
                data_dict["acousticness"].append(audio_features["acousticness"])
                data_dict["danceability"].append(audio_features["danceability"])
                data_dict["energy"].append(audio_features["energy"])
                data_dict["instrumentalness"].append(audio_features["instrumentalness"])
                data_dict["liveness"].append(audio_features["liveness"])
                data_dict["loudness"].append(audio_features["loudness"])
                data_dict["mode"].append(audio_features["mode"])
                data_dict["speechiness"].append(audio_features["speechiness"])
                data_dict["tempo"].append(audio_features["tempo"])
                data_dict["valence"].append(audio_features["valence"])
                

        offset = total_num_of_songs // 100 * 100
        limit = total_num_of_songs - offset
        tracks = self.getPlaylistItems(limit, offset)
        for item in tracks:
                data_dict["track_id"].append(item["track"]["id"])
                data_dict["track_name"].append(item["track"]["name"])
                data_dict["album_name"].append(item["track"]["album"]["name"])
                data_dict["album_popularity"].append(item["track"]["popularity"])
                data_dict["release_date"].append(item["track"]["album"]["release_date"])
                data_dict["artist_name"].append(item["track"]["album"]["artists"][0]["name"])
                artist_genres = self.getArtistGenres(item["track"]["album"]["artists"][0]["id"])
                if len(artist_genres) == 0:
                    genres = "NaN"
                else:
                    genres = ",".join(artist_genres)
                data_dict["artist_genres"].append(genres)
                audio_features = self.getAudioFeatures(item["track"]["id"])
                data_dict["acousticness"].append(audio_features["acousticness"])
                data_dict["danceability"].append(audio_features["danceability"])
                data_dict["energy"].append(audio_features["energy"])
                data_dict["instrumentalness"].append(audio_features["instrumentalness"])
                data_dict["liveness"].append(audio_features["liveness"])
                data_dict["loudness"].append(audio_features["loudness"])
                data_dict["mode"].append(audio_features["mode"])
                data_dict["speechiness"].append(audio_features["speechiness"])
                data_dict["tempo"].append(audio_features["tempo"])
                data_dict["valence"].append(audio_features["valence"])
        
        self.df = pd.DataFrame(data_dict)
        return self.df
        """
        for t in data_dict:
            print(t, data_dict[t])
        """