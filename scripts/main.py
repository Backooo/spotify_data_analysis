from user_input import get_time_range
from spotify_api_access import *


def get_top_artists(sp, time_range):
    top_artists = sp.current_user_top_artists(time_range=time_range)['items']
    genre_count = {}
    for artist in top_artists[:5]:
        artist_info = get_artist_info(sp, artist['id'])
        print(f"{artist_info['name']} - Follower count: {artist_info['followers']['total']}, Popularity: {artist_info['popularity']}")
        for genre in artist_info['genres']:
            genre_count[genre] = genre_count.get(genre, 0) + 1
    return genre_count


def get_top_tracks(sp, time_range):
    top_tracks = sp.current_user_top_tracks(time_range=time_range)['items']  # API-Aufruf
    for track in top_tracks[:5]:
        artists = ", ".join([artist['name'] for artist in track['artists']])
        print(f"{track['name']} from {artists} - Popularity: {track['popularity']}")


def get_audio_features(sp, time_range):
    top_tracks = sp.current_user_top_tracks(time_range=time_range)['items']  # API-Aufruf
    audio_features = sp.audio_features([track['id'] for track in top_tracks])  # API-Aufruf
    for track, feature in zip(top_tracks[:5], audio_features):
        if feature:
            print(f"Track: {track['name']} by {' '.join([artist['name'] for artist in track['artists']])}")
            print(f"Danceability: {feature['danceability']}, Energy: {feature['energy']}, Valence: {feature['valence']}")


def get_playlists(sp):
    playlists = sp.current_user_playlists()['items']  # API-Aufruf
    for playlist in playlists[:3]:  # Begrenzung auf die ersten 3 Playlists
        print(f"\n{playlist['name']} - {playlist['tracks']['total']} Tracks\n")
        genre_count_playlist = analyze_playlist_artists_genres(sp, playlist['id'])
        sorted_genres_playlist = sorted(genre_count_playlist.items(), key=lambda x: x[1], reverse=True)
        for genre, count in sorted_genres_playlist:
            print(f"{count} Tracks in {genre}")


def get_playlist_content(sp, playlist_id):
    playlist_tracks = get_tracks_from_playlists(sp, playlist_id)
    genre_count_playlist = {}
    popularity_sum = 0
    max_popularity = 0
    min_popularity = 100

    for item in playlist_tracks:
        track = item['track']
        track_genres = get_genres_of_track(sp, track['id'])
        for genre in track_genres:
            genre_count_playlist[genre] = genre_count_playlist.get(genre, 0) + 1
        popularity = track['popularity']
        popularity_sum += popularity
        max_popularity = max(max_popularity, popularity)
        min_popularity = min(min_popularity, popularity)

    sorted_genres_playlist = sorted(genre_count_playlist.items(), key=lambda x: x[1], reverse=True)
    for genre, count in sorted_genres_playlist:
        print(f"{count} Tracks in {genre}")

    average_popularity = popularity_sum / len(playlist_tracks) if playlist_tracks else 0
    print(f"\nAverage Popularity: {average_popularity}")
    print(f"Max Popularity: {max_popularity}")
    print(f"Min Popularity: {min_popularity}")


def main():
    sp = auth_spotify()
    time_range = get_time_range()

    print("Your Top Artists:\n")
    genre_count = get_top_artists(sp, time_range)

    print("\n--------------------------------------------------- \n")
    print("Your Top Tracks:\n")
    get_top_tracks(sp, time_range)

    print("\n--------------------------------------------------- \n")
    print("Your Top Genres:\n")
    for genre, count in sorted(genre_count.items(), key=lambda x: x[1], reverse=True):
        print(f"{count} artists in {genre}")

    print("\n--------------------------------------------------- \n")
    print("Analysis of your Top Tracks Audio Features:\n")
    get_audio_features(sp, time_range)

    print("\n--------------------------------------------------- \n")
    print("Your Newest 3 Playlists:\n")
    playlists = get_playlists(sp)
    if playlists:
        for playlist in playlists[:3]:
            print(f"{playlist['name']} - {playlist['tracks']['total']} Tracks\n")
            analyze_playlist_artists_genres(sp, playlist['id'])

    create_super_playlist_from_top_tracks(sp, time_range, max_tracks=100)


if __name__ == "__main__":
    main()
