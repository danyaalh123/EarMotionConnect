# -*- encoding: utf-8 -*-
"""
Original source from AppSeed.us - adapted and modified for educational purposes.
"""

# Flask modules import: Used for web app functionalities
from apps import app
from flask import Flask, request, render_template, jsonify
# Jinja2 module import: Template engine for Python
from jinja2 import TemplateNotFound

# Spotify modules import: To interact with Spotify's API
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Spotify setup: Configuring Spotify API credentials and scopes
client_id = app.config['CLIENT_ID']
client_secret = app.config['CLIENT_SECRET'] 
redirect_uri = app.config['SPOTIFY_REDIRECT_URL']
scope = "user-read-private user-read-playback-state user-modify-playback-state"

# Creating Spotify client instance with OAuth for user authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Data store initialization for received data and current song
threshold = 10
received_data = ""
chart_data = [threshold] * 9
playlists = {
    'highAlpha': ['Sleep', 'Meditation', 'Relaxed'],
    'highBeta': ['Upbeat', 'Energetic', 'Active']
}
current_genre = ""
current_playlist = ""

# Function to search and play a specific Spotify playlist
def search_and_play_playlist(playlist_name):
    result = sp.search(playlist_name, type='playlist', limit=1)
    if result['playlists']['items']:
        playlist_id = result['playlists']['items'][0]['id']
        playlist_uri = result['playlists']['items'][0]['uri']
        sp.start_playback(context_uri=playlist_uri)
        print(f"Playing playlist: {playlist_name}")
    else:
        print("Playlist not found.")

# Function to get the currently playing song on Spotify
def get_current_song():
    global current_playlist
    current_playback = sp.current_playback()
    if current_playback and current_playback['is_playing']:
        current_song = current_playback['item']['name']
        artist_name = current_playback['item']['artists'][0]['name']
        album_cover_url = current_playback['item']['album']['images'][0]['url']
        playlist_name = ""
        if current_playback['context'] and current_playback['context']['type'] == 'playlist':
            playlist_id = current_playback['context']['uri'].split(':')[-1]
            playlist_name = current_playlist

        return current_song, artist_name, album_cover_url, playlist_name
    return "", "", "", ""

# Main route of the Flask application
@app.route('/')
def index():
    current_song, artist_name, album_cover_url, playlist_name = get_current_song()
    return render_template('home/index.html', 
                           received_data=received_data, 
                           current_song=current_song, 
                           artist_name=artist_name, 
                           album_cover_url=album_cover_url, 
                           playlist_name=playlist_name, 
                           current_genre=current_genre, 
                           threshold=threshold,
                           segment='index')

# Route for handling EEG data received via POST request
@app.route('/eeg-data', methods=['POST'])
def eeg_data():
    global chart_data, current_genre, current_playlist, threshold
    if request.form:
        data_received = request.form.get('data')
    else:
        data_received = request.data.decode('utf-8')
    
    print(f"Received data: {data_received}")
    chart_data.pop(0)
    chart_data.append(int(data_received))
    required_playlist = 'highBeta' if all(x < int(threshold) for x in chart_data) else 'highAlpha' if all(x > int(threshold) for x in chart_data) else current_genre 

    if required_playlist != current_genre:
        current_genre = required_playlist
        current_playlist = random.choice(playlists[current_genre])
        search_and_play_playlist(current_playlist)

    return "EEG Data received"

# Route for handling generic data received via POST request
@app.route('/data', methods=['POST'])
def data():
    global received_data
    if request.form:
        data_received = request.form.get('data')
    else:
        data_received = request.data.decode('utf-8')
    print(f"Received data: {data_received}")
    search_and_play_playlist(data_received)
    received_data = data_received
    return "Data received"

# Route for updating data on the client side
@app.route('/update-data')
def update_data():
    global received_data
    global chart_data
    global threshold
    current_song, artist_name, album_cover_url, playlist_name = get_current_song()
    return jsonify(
        received_data=received_data, 
        current_song=current_song, 
        artist_name=artist_name, 
        playlist_name=playlist_name, 
        album_cover_url=album_cover_url,
        current_genre=current_genre, 
        threshold=threshold,
        chartData=chart_data
    )

# Route for updating playlist information based on user interaction
@app.route('/update-playlist', methods=['POST'])
def update_playlist():
    global playlists
    data = request.json
    playlist_type = data['type']
    playlist_name = data['name']

    if playlist_name in playlists[playlist_type]:
        playlists[playlist_type].remove(playlist_name)
    else:
        playlists[playlist_type].append(playlist_name)

    return jsonify({"message": "Playlist updated"})

# Route for retrieving playlist data in JSON format
@app.route('/get-playlist-data')
def get_playlist_data():
    global playlists
    return jsonify(playlists)

# Route for updating threshold based on user interaction
@app.route('/update-threshold', methods=['POST'])
def update_threshold():
    global threshold
    data = request.json
    threshold = data['threshold']
    return jsonify({"message": "Threshold updated"})

# Route for retrieving threshold data in JSON format
@app.route('/get-threshold')
def get_threshold():
    global threshold
    return jsonify(threshold=threshold)

# Catch-all route for any undefined URLs
@app.route('/<path:path>')
def catch_all(path):
    try:
        segment = get_segment(request)
        return render_template('home/' + path, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

# Helper function to get the current URL segment
def get_segment(request): 
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment    
    except:
        return None
