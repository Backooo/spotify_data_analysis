import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth


def auth_spotify():
    load_dotenv()

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    scope = "user-top-read playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private"

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


def get_playlists(sp):
    response = sp.current_user_playlists()
    if response:
        return response['items']
    else:
        print("Fehler beim Abrufen der Playlists.")
        return []


def get_tracks_from_playlists(sp, playlist_id):
    playlist_tracks = []
    response = sp.playlist_tracks(playlist_id, limit=100)

    while response:
        playlist_tracks.extend(response['items'])
        if response['next']:
            response = sp.next(response)
        else:
            break
    return playlist_tracks


def get_genres_of_track(sp, track_id):
    track_info = sp.track(track_id)
    artist_ids = [artist['id'] for artist in track_info['artists']]

    genres = set()
    for artist_id in artist_ids:
        artist_info = sp.artist(artist_id)
        genres.update(artist_info['genres'])

    return list(genres)


def analyze_playlist_artists_genres(sp, playlist_id):
    playlist_tracks = get_tracks_from_playlists(sp, playlist_id)
    genre_count_playlist = {}

    for item in playlist_tracks:
        track = item['track']
        artists = track['artists']
        for artist in artists:
            artist_info = get_artist_info(sp, artist['id'])
            for genre in artist_info['genres']:
                genre_count_playlist[genre] = genre_count_playlist.get(genre, 0) + 1

    return genre_count_playlist


def create_super_playlist_from_top_tracks(sp, time_range, playlist_name="My Top 50 Tracks", max_tracks=100):
    choice = input("Create a Super-Playlist of your Top Tracks from chosen time range? (y/n): ")

    if choice != "y":
        return

    top_tracks = []
    response = sp.current_user_top_tracks(limit=50, time_range=time_range)
    while response and len(top_tracks) < max_tracks:
        top_tracks.extend(response['items'])
        if response['next'] and len(top_tracks) < max_tracks:
            response = sp.next(response)
        else:
            break

    track_ids = [track['id'] for track in top_tracks[:max_tracks]]
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name)
    sp.playlist_add_items(playlist['id'], track_ids)
    print(f"Playlist '{playlist_name}' created with {len(track_ids)} tracks.")
