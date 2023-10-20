from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .models import Albums, AudioFeatures, Kpop, Jpop

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

    # 장르가 문자열로 되어있기 때문에 문자 제외한 부분 제거하고 리스트로 저장.
    genres = album.album_genre.strip('[]').replace("'", "").split(', ')

    # 앨범 데이터와 노래 데이터, 장르 반환
    context = {
        'album': album,
        'songs_data': songs_data,
        'genres' : genres
    }

    return render(request, 'Ssavi_app/detail.html', context)


import matplotlib
matplotlib.use('Agg')  # Matplotlib이 인터페이스를 생성하지 않도록 설정
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

def analysis(request, song_id):
    # 곡의 audio feature 불러오기
    audio_feature = get_object_or_404(AudioFeatures, pk=song_id)
    feat_cols = ['acousticness', 'danceability', 'energy', 'loudness', 'speechiness', 'tempo', 'valence']
    
    # song_id를 가지고 장르 뽑기
    track_info = sp.track(song_id)
    artist_id = track_info["artists"][0]["id"]
    artists_info = sp.artist(artist_id)
    genre = artists_info["genres"][0]
    
    # 각 장르마다 평균 audio feature를 구하기 위해 모델 오브젝트 불러옴
    if genre=='k-pop':
        genre_audio_feature_all = Kpop.objects.all()
    elif genre=='pop':
        genre_audio_feature_all = Jpop.objects.all()
    else:
        print("오류")

    # 장르의 audio feature의 평균값 구하기
    avg_acousticness = genre_audio_feature_all.aggregate(avg_acousticness=Avg('acousticness'))['avg_acousticness']
    avg_danceability = genre_audio_feature_all.aggregate(avg_danceability=Avg('danceability'))['avg_danceability']
    avg_energy = genre_audio_feature_all.aggregate(avg_energy=Avg('energy'))['avg_energy']
    avg_loudness = 10**(genre_audio_feature_all.aggregate(avg_loudness=Avg('loudness'))['avg_loudness'] / 10)
    avg_speechiness = genre_audio_feature_all.aggregate(avg_speechiness=Avg('speechiness'))['avg_speechiness']
    avg_tempo = genre_audio_feature_all.aggregate(avg_tempo=Avg('tempo'))['avg_tempo'] / 100
    avg_valence = genre_audio_feature_all.aggregate(avg_valence=Avg('valence'))['avg_valence']

    # 장르의 평균 audio feature
    genre_audio_feature_data = {
        "acousticness": avg_acousticness,
        "danceability": avg_danceability,
        "energy": avg_energy,
        "loudness": avg_loudness,
        "speechiness": avg_speechiness,
        "tempo": avg_tempo,
        "valence": avg_valence
    }

    # 내가 선택한 곡의 audio feature
    audio_feature_data = {
        "acousticness": audio_feature.acousticness,
        "danceability": audio_feature.danceability,
        "energy": audio_feature.energy,
        "loudness": 10**(audio_feature.loudness/10),
        "speechiness": audio_feature.speechiness,
        "tempo": audio_feature.tempo/100,
        "valence": audio_feature.valence
    }

    # 그래프 그리기
    genre_r_values = [genre_audio_feature_data[col] for col in feat_cols]
    r_values = [audio_feature_data[col] for col in feat_cols]
    

    # 그래프를 생성하고 데이터 표시
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='polar')

    # 내가 선택한 곡 그래프 추가
    # 그래프 영역 채우기 ('b' : 파란색)
    ax.fill(feat_cols + feat_cols[:1], r_values + r_values[:1], 'blue', alpha=0.1, label='current song audio feature')
    
    # 장르 평균값 그래프 추가
    ax.fill(feat_cols + feat_cols[:1], genre_r_values + genre_r_values[:1], 'r', alpha=0.1, label='genre average audio feature')

    # 기존 그래프 설정 (축 레이블 등)
    ax.set_xticks(range(len(feat_cols)))
    ax.set_xticklabels(feat_cols)
    # 범례 표시 (위치 조정 가능)
    ax.legend(loc='upper right', bbox_to_anchor=(1, 1.1))

    # 그래프를 이미지로 저장
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 이미지 데이터를 Base64로 인코딩하여 클라이언트에게 반환
    image_data1 = base64.b64encode(buffer.read()).decode('utf-8')

    audio_feature_data = {
        "acousticness": audio_feature.acousticness+1,
        "danceability": audio_feature.danceability+1,
        "energy": audio_feature.energy+1,
        "loudness": 10**(audio_feature.loudness/10)+1,
        "speechiness": audio_feature.speechiness+1,
        "tempo": audio_feature.tempo/100+1,
        "valence": audio_feature.valence+1
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
    image_data2 = base64.b64encode(buffer.read()).decode('utf-8')
    return render(request, 'Ssavi_app/analysis.html', {'image1': image_data1, 'image2' : image_data2})


def recommend(request):
    return render(request, 'Ssavi_app/recommend.html')