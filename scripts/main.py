from user_input import get_time_range
from spotify_api_access import auth_spotify, get_top_tracks


def main():
    sp = auth_spotify()
    time_range = get_time_range()

    top_tracks = get_top_tracks(sp, time_range)
    for track in top_tracks['items']:
        print(track['name'], '-', track['artists'][0]['name'])


if __name__ == "__main__":
    main()
