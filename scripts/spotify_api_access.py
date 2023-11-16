import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth


def auth_spotify():
    load_dotenv()

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    scope = "user-top-read playlist-read-private playlist-read-collaborative"

    sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Authorize at this URL: {auth_url}")

        redirected_url = input("Please enter the URL you were redirected to: ")
        code = sp_oauth.parse_response_code(redirected_url)
        token_info = sp_oauth.get_access_token(code)
    else:
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])

    return spotipy.Spotify(auth=token_info['access_token'])


def get_top_tracks(sp, time_range):
    return sp.current_user_top_tracks(time_range=time_range)


def get_top_artists(sp, time_range):
    return sp.current_user_top_artists(time_range=time_range)


def get_artist_info(sp, artist_id):
    return sp.artist(artist_id)


def get_audio_features_per_track(sp, time_range):
    tracks = get_top_tracks(sp, time_range=time_range)
    track_ids = [track['id'] for track in tracks['items']]
    return sp.audio_features(track_ids)


def get_playlists(sp):
    playlists = []
    response = sp.current_user_playlists(limit=50)

    while response:
        playlists.extend(response['items'])
        if response['next']:
            response = sp.next(response)
        else:
            break
    return playlists
