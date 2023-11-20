import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_top_tracks(top_tracks_data):
    for track in top_tracks_data:
        print(f"{track['name']} from {track['artists']} - Popularity: {track['popularity']}")
    plt.style.use('ggplot')
    track_names = [track['name'] for track in top_tracks_data]
    popularity = [track['popularity'] for track in top_tracks_data]
    colors = plt.cm.viridis([0.2, 0.4, 0.6, 0.8, 1.0])
    plt.figure(figsize=(12, 15))
    bars = plt.bar(track_names, popularity, color=colors)

    for bar in bars:
        yVal = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yVal + 1, round(yVal, 1), ha='center', va='bottom')

    plt.xlabel('Tracks')
    plt.ylabel('Popularity')
    plt.title('Top 5 Tracks Popularity')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
    plt.show()


def plot_audio_features(top_tracks_data, audio_features):
    danceability = [feature['danceability'] for feature in audio_features]
    energy = [feature['energy'] for feature in audio_features]
    valence = [feature['valence'] for feature in audio_features]
    track_names = [track['name'] for track in top_tracks_data]
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.bar(track_names, danceability, color='blue')
    plt.title('Danceability')
    plt.xticks(rotation=45)

    plt.subplot(1, 3, 2)
    plt.bar(track_names, energy, color='green')
    plt.title('Energy')
    plt.xticks(rotation=45)

    plt.subplot(1, 3, 3)
    plt.bar(track_names, valence, color='red')
    plt.title('Valence')
    plt.xticks(rotation=45)

    plt.suptitle('Audio Features of Top Tracks')
    plt.tight_layout()
    plt.show()


def plot_genre_distribution_pie(genre_dist):
    genres = list(genre_dist.keys())
    counts = list(genre_dist.values())

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=genres, autopct='%1.1f%%', startangle=60)
    plt.title('Genre-Distribution of your Top Artists')
    plt.show()


def plot_playlist_features(playlists_features):
    plt.figure(figsize=(10, 6))

    for features in playlists_features:
        energy = [feature['energy'] for feature in features]
        danceability = [feature['danceability'] for feature in features]
        plt.scatter(energy, danceability)

    plt.xlabel('Energy')
    plt.ylabel('Danceability')
    plt.title('Energy vs Danceability in Playlists')
    plt.legend([f'Playlist {i + 1}' for i in range(len(playlists_features))])
    plt.show()
