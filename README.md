# spotify_data_analysis
Your very own **Spotify Wrapped** for any time of the year

## Overview

This project aims at analyzing data from the Spotify API to visualize your own custom Spotify Wrapped that can be accessed any time of the year.

## Key Features
- Visualization of top artists, songs, and genres over chosen time period
- Playlist analysis of audio features
- Creation of playlist of your 50 top tracks from chosen time period

## Dependencies
- spotipy (To interact with the Spotify Web API)
- matplotlib (For static visualizations)
- dotenv (Handle Spotify API credentials without hardcoding)

## Getting Your Spotify API Credentials
To use this project, you need to register your application with Spotify and obtain the necessary credentials. Follow these steps:
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Log in with your Spotify account (or create one if you don't have it yet).
3. Click on 'Create an App'. Fill in the form with your app details.
4. Once your app is created, you will see your Client ID and Secret. Add these to your `.env` file as described in the Installation section.

## Installation
1. Clone the repository: `git clone [repository URL]`
2. Install the required Python packages: `pip install spotipy matplotlib python-dotenv`
3. Set up your Spotify API credentials: 
   - Create a `.env` file in the root of the project.
   - Add your Spotify Client ID and Client Secret to the `.env` file as follows:
     ```
     SPOTIFY_CLIENT_ID='your_client_id'
     SPOTIFY_CLIENT_SECRET='your_client_secret'
     ```
## Usage
To run the script:
1. Navigate to the project directory.
2. Run `python main.py` and follow the prompts to select your time range for analysis.
