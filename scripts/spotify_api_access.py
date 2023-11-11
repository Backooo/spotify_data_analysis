import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret= os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

scope = "user-top-read"

sp_Oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope)

auth_url = sp_Oauth.get_authorize_url()
print(f"Authorize at this URL: {auth_url}")

redirected_url = input("Please enter the URL you were redirected to: ")
code = sp_Oauth.parse_response_code(redirected_url)

token_info = sp_Oauth.get_cached_token()
if not token_info:
    token_info = sp_Oauth.refresh_access_token()

sp = spotipy.Spotify(auth=token_info['access_token'])


urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'
try:
    artist = sp.artist(urn)
    print(artist['name'])
except spotipy.exceptions.SpotifyException as e:
    print(f"Error : {e}")

