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
    top_tracks = sp.current_user_top_tracks(time_range=time_range)['items']
    track_info = []
    track_ids = []
    for track in top_tracks[:5]:
        track_data = {
            'name': track['name'],
            'popularity': track['popularity'],
            'artists': ", ".join([artist['name'] for artist in track['artists']])
        }
        track_info.append(track_data)
        track_ids.append(track['id'])
    return track_info, track_ids


def get_top_artists(sp, time_range):
    return sp.current_user_top_artists(time_range=time_range)['items']


def get_artist_info(sp, artist_id):
    return sp.artist(artist_id)


def top_artist_info(sp, time_range):
    return sp.current_user_top_artists(time_range=time_range)['items']


def get_playlists(sp):
    return sp.current_user_playlists()['items']


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


def get_genre_distribution(top_artists):
    genre_count = {}
    for artist in top_artists:
        for genre in artist['genres']:
            genre_count[genre] = genre_count.get(genre, 0) + 1

    final_genres = {}
    for genre, count in genre_count.items():
        if count == 1:
            final_genres['Other'] = final_genres.get('Other', 0) + 1
        else:
            final_genres[genre] = final_genres.get(genre, 0) + count

    return final_genres


def get_playlist_tracks_features(sp, playlist_id):
    playlist_tracks = get_tracks_from_playlists(sp, playlist_id)
    track_ids = [track['track']['id'] for track in playlist_tracks]
    features = sp.audio_features(track_ids)
    return features


def calculate_playlist_averages(sp, playlist_id):
    tracks = get_tracks_from_playlists(sp, playlist_id)
    track_ids = [track['track']['id'] for track in tracks]

    features = sp.audio_features(track_ids)
    if not features:
        return None

    total_danceability = total_valence = total_energy = 0
    valid_features_count = 0

    for feature in features:
        if feature:
            total_danceability += feature['danceability']
            total_valence += feature['valence']
            total_energy += feature['energy']
            valid_features_count += 1

    if valid_features_count > 0:
        return {
            'average_danceability': total_danceability / valid_features_count,
            'average_valence': total_valence / valid_features_count,
            'average_energy': total_energy / valid_features_count
        }
    else:
        return None
