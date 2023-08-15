from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import webbrowser
from urllib.parse import urlencode
import pandas as pd
from pandas import json_normalize
from database import Database
from spotify import Spotify


def get_token(client_id, client_secret, code):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code" : code,
        "redirect_uri": "http://localhost:7777/callback"
    }
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    refresh_token = json_result["refresh_token"]
    return token, refresh_token

def main():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    #playlist_id = os.getenv("MY_PLAYLIST_ID")
    playlist_id = "5Dww7ikBY4JDVUe5Csdpm8"

    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read user-library-modify user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-top-read user-read-recently-played user-read-currently-playing user-modify-playback-state user-modify-playback-state"
    }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    code = input("Please insert the authentication code: \n")

    token, refresh_token = get_token(client_id, client_secret, code)
    spotifyInteract = Spotify(client_id, client_secret, token, refresh_token)
    result = spotifyInteract.search_for_artist("Justin")
    print("Found: ", result["name"])
    track_searched = spotifyInteract.search_for_track("Ghost", 2)
    print("Found track:", track_searched[1]["name"], "By", track_searched[1]["artists"][0]["name"], "URI:", track_searched[1]["uri"] )
    print("User's 15 top tracks: ")
    tt = spotifyInteract.get_user_top_tracks(3, 0)
    t = spotifyInteract.getRecentTracks(15)
    for idx, item in enumerate(tt):
        print(idx + 1, ".", item["name"])
    
    #spotifyInteract.add_items_to_playlist_by_name(playlist_id, ["Baby", "LADY"])

    #df = spotifyInteract.getDefaultDataframe()
    #sq = Database("second_db", df)
    #sq.insert()
    t = spotifyInteract.getRecentTracks(15)
    for idx, item in enumerate(t):
        print(idx + 1, ".", item["track"]["name"])
    r = spotifyInteract.get_current_playing_track()
    print(r["name"])

    spotifyInteract.skip_to_prev()
    
main()