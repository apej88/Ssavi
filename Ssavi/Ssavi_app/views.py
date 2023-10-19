from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import Albums, AudioFeatures

client_credentials_manager = SpotifyClientCredentials(client_id='c0ef6b3167de4affb312e7fc7366abb4', client_secret='86babd771d3c4098b90fc70ed221cd60')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create your views here.
def index(request):
    return render(request, 'Ssavi_app/index.html')

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

import matplotlib
matplotlib.use('Agg')  # Matplotlib이 인터페이스를 생성하지 않도록 설정

import matplotlib.pyplot as plt
import io
import mpld3
import base64

def analysis(request, song_id):
    # 곡의 audio feature 불러오기
    audio_feature = get_object_or_404(AudioFeatures, pk=song_id)
    feat_cols = ['acousticness', 'danceability', 'energy', 'loudness', 'speechiness', 'tempo', 'valence']
    
    audio_feature_data = {
        "acousticness": audio_feature.acousticness,
        "danceability": audio_feature.danceability,
        "energy": audio_feature.energy,
        "loudness": 10**(audio_feature.loudness/10),
        "speechiness": audio_feature.speechiness,
        "tempo": audio_feature.tempo/100,
        "valence": audio_feature.valence
    }

    r_values = [audio_feature_data[col] for col in feat_cols]

    # 그래프를 생성하고 데이터 표시
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='polar')
    ax.fill(feat_cols + feat_cols[:1], r_values + r_values[:1], 'b', alpha=0.1)
    ax.set_xticks(range(len(feat_cols)))
    ax.set_xticklabels(feat_cols)

    # 그래프를 이미지로 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 이미지 데이터를 Base64로 인코딩하여 클라이언트에게 반환
    image_data = base64.b64encode(buffer.read()).decode('utf-8')
    return render(request, 'Ssavi_app/analysis.html', {'image': image_data})


def recommend(request):
    return render(request, 'Ssavi_app/recommend.html')