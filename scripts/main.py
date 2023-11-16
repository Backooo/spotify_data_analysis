from user_input import get_time_range
from spotify_api_access import auth_spotify, get_top_tracks, get_top_artists, get_artist_info, get_audio_features_per_track, get_playlists


def main():
    sp = auth_spotify()
    time_range = get_time_range()

    print("Your Top Artists:\n")
    genre_count = {}
    top_artists = get_top_artists(sp, time_range)
    for artist in top_artists['items']:
        artist_info = get_artist_info(sp, artist['id'])
        print(f"{artist_info['name']} - Follower count: {artist_info['followers']['total']}, Popularity: {artist_info['popularity']}")
        for genre in artist_info['genres']:
            genre_count[genre] = genre_count.get(genre, 0) + 1
    sort_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
    print("\n--------------------------------------------------- \n")
    print("Your Top tracks:\n")
    top_tracks = get_top_tracks(sp, time_range)
    for track in top_tracks['items']:
        artists = ", ".join([artist['name'] for artist in track['artists']])
        print(f"{track['name']} from {artists} - Popularity: {track['popularity']}")
        print(track['name'], '-', track['artists'][0]['name'])
    print("\n--------------------------------------------------- \n")
    print("Your top genres:\n")
    for genre, count in sort_genres:
        print(f"{count} artists in {genre}")
    print("\n--------------------------------------------------- \n")
    print("Analysis of your Top Tracks Audio Features:\n")
    audio_features = get_audio_features_per_track(sp, time_range)
    for track, feature in zip(top_tracks['items'], audio_features):
        if feature:
            print(f"Track: {track['name']} by {' '.join([artist['name'] for artist in track['artists']])}")
            print(f"Danceability: {feature['danceability']}, Energy: {feature['energy']}, Valence: {feature['valence']}")
    print("\n--------------------------------------------------- \n")
    print("Your Playlists:\n")
    playlists = get_playlists(sp)
    for playlist in playlists:
        print(f"{playlist['name']} - {playlist['tracks']['total']} Tracks")


if __name__ == "__main__":
    main()
