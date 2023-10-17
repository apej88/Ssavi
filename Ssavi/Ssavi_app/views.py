from django.shortcuts import render, redirect, get_object_or_404
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id='c0ef6b3167de4affb312e7fc7366abb4', client_secret='86babd771d3c4098b90fc70ed221cd60')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create your views here.
def index(request):
    return render(request, 'Ssavi_app/index.html')

def detail(request):
    album_id = '01dPJcwyht77brL4JQiR8R'
    songs = sp.album_tracks(album_id=album_id)['items']
    song_name = []; song_artist = []; song_preview = []
    for j in range(0, len(songs)):
        song_name.append({'song_name' : songs[j]['name']})
        song_artist.append({'song_artist' : songs[j]['artists'][0]['name']})
        song_preview.append({'song_preview' : songs[j]['preview_url']})
    album = [song_name, song_artist, song_preview]
    print(album)
    return render(request, 'Ssavi_app/detail.html', {'album' : album})

def recommend(request):
    return render(request, 'Ssavi_app/recommend.html')