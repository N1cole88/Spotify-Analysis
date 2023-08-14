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
    return token

def main():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    playlist_id = os.getenv("MY_PLAYLIST_ID")

    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-library-read user-library-modify user-read-private user-read-email playlist-read-private"
    }

    webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    code = "AQC8SUoBNkrkRM8Khj3wK8JfYAa5dhN5NOlBv8VtJnwVbViiL5kCyQvkv5CXcX3v1zkiRhRgZPnRTwB-S5IbuDyN8Nj9Nj8r1ASSHROD84LSL2d9H2XUm1LpYoelM4YjM9MVeBy63D15zbgeB3iMn6AKf_fGAPNL6c4u2C-f6X6mgqKiEXB1EE6A-ZHeped9oX3An2_Pv88IeH5Y5nzcO5uQVvE_MYzl462g5VPok63fROJ4HzZvq4uWVAMn45_QzpO4Nanwg3fBQdS_2genAG9GgB6RnqCJQ7SGerAW4CKpsaJfHQ"

    token = get_token(client_id, client_secret, code)
    spotifyInteract = Spotify(client_id, client_secret, token)
    result = spotifyInteract.search_for_artist("Justin")
    print("Found: ", result["name"])

    df = spotifyInteract.getDefaultDataframe()
    sq = Database("first_db", df)
    sq.insert()

    
main()