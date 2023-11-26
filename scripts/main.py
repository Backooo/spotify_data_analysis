from user_input import get_time_range
from spotify_api_access import *
from visualization import *


def main():
    sp = auth_spotify()
    time_range = get_time_range()

    print("Your Top Artists:\n")
    top_artists = get_top_artists(sp, time_range)[:5]
    for artist in top_artists:
        print(f"{artist['name']} - Follower count: {artist['followers']['total']}, Popularity: {artist['popularity']}")

    print("\n--------------------------------------------------- \n")
    print("Your Top Tracks:\n")
    top_tracks, tracks_ids = get_top_tracks(sp, time_range)
    plot_top_tracks(top_tracks)

    print("\n--------------------------------------------------- \n")
    print("Your Top Genres:\n")
    top_artists_for_genre = top_artist_info(sp, time_range)
    genre_dist = get_genre_distribution(top_artists_for_genre)
    for genre, count in sorted(genre_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"{count} artists in {genre}")
    plot_genre_distribution_pie(genre_dist)

    print("\n--------------------------------------------------- \n")
    print("Analysis of your Top Tracks Audio Features:\n")
    top_tracks, track_ids = get_top_tracks(sp, time_range)
    audio_features = sp.audio_features(track_ids)

    for track, features in zip(top_tracks, audio_features):
        print(f"Track: {track['name']} by {track['artists']}")
        print(
            f"Danceability: {features['danceability']}, Energy: {features['energy']}, Valence: {features['valence']}\n")

    plot_audio_features(top_tracks, audio_features)

    print("\n--------------------------------------------------- \n")
    print("Playlist Feature Analysis:\n")
    playlists = get_playlists(sp)[:3]
    playlist_names = [playlist['name'] for playlist in playlists]
    all_playlists_features = [get_playlist_tracks_features(sp, playlist['id']) for playlist in playlists]

    plot_playlist_features(all_playlists_features, playlist_names)

    playlists = get_playlists(sp)[:3]
    danceability_list, valence_list, energy_list = [], [], []
    for playlist in playlists:
        averages = calculate_playlist_averages(sp, playlist['id'])
        if averages:
            print(f"\n{playlist['name']} - {playlist['tracks']['total']} Tracks")
            print(f"Average Danceability: {averages['average_danceability']:.2f}")
            print(f"Average Valence: {averages['average_valence']:.2f}")
            print(f"Average Energy: {averages['average_energy']:.2f}")
            danceability_list.append(averages['average_danceability'])
            valence_list.append(averages['average_valence'])
            energy_list.append(averages['average_energy'])
        else:
            print(f"\n{playlist['name']} - No data available")
    plot_playlist_boxplots([danceability_list, valence_list, energy_list])

    print("\n--------------------------------------------------- \n")
    create_super_playlist_from_top_tracks(sp, time_range, max_tracks=100)


if __name__ == "__main__":
    main()
