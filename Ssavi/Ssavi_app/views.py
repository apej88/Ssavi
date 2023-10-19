from django.shortcuts import render, redirect, get_object_or_404
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import Albums

client_credentials_manager = SpotifyClientCredentials(client_id='c0ef6b3167de4affb312e7fc7366abb4', client_secret='86babd771d3c4098b90fc70ed221cd60')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create your views here.
def index(request):
    return render(request, 'Ssavi_app/index.html')

# def detail(request, ab_id):
#     songs = sp.album_tracks(album_id=ab_id)['items']
#     for i in range(0, len(songs)):
#         url.append({'url' : songs[i]['img']})
#         name.append({'song_name' : songs[i]['name']})
#         artist.append({'song_artist' : songs[i]['artists'][0]['name']})
#         preview.append({'song_preview' : songs[i]['preview_url']})
#     album = [name, artist, preview] 
#     return render(request, 'Ssavi_app/detail.html', {'album' : album})

def detail(request, ab_id):
    album = get_object_or_404(Albums, pk=ab_id)
    songs = sp.album_tracks(album_id=ab_id)['items']
    songs_data = [] # 앨범 안의 노래들의 정보를 담을 리스트

    for s in range(0, len(songs)):
        song = {}  # 각 노래의 정보를 저장할 딕셔너리 생성
        song['song_id'] = songs[s]['id']
        song['song_name'] = songs[s]['name']
        song['song_artist'] = songs[s]['artists'][0]['name']
        song['song_preview_url'] = songs[s]['preview_url']
        songs_data.append(song)  # 노래 정보를 리스트에 추가

    context = {
        'album': album,
        'songs_data': songs_data,
    } # 앨범 데이터와 노래 데이터 반환

    return render(request, 'Ssavi_app/detail.html', context)


def recommend(request):
    return render(request, 'Ssavi_app/recommend.html')