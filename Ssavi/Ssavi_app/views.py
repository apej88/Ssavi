from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from .models import Albums, Tracks, AudioFeatures, Kpop, Jpop, Jazz, Latin, Alternative, Hiphop, Rnb, Rock, Indiepop

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

def analysis(request, song_id):
    # 곡의 audio feature 불러오기
    audio_feature = get_object_or_404(AudioFeatures, pk=song_id)
    Track = get_object_or_404(Tracks, pk=song_id)
    feat_cols = ['acousticness', 'danceability', 'energy', 'loudness', 'speechiness', 'tempo', 'valence']
    
    # song_id를 가지고 장르 뽑기
    track_info = sp.track(song_id)
    album_id = track_info['album']['id']
    album_info = sp.album(album_id)
    album_images = album_info['images']
    album_image_url = album_images[0]['url']
    song_name = track_info['name']
    artist_id = track_info["artists"][0]["id"]
    artists_info = sp.artist(artist_id)
    artist_name = artists_info['name']
    genre = artists_info["genres"][0]
    
    current_song = [album_image_url, song_name, artist_name, Track.track_preview]
    
    # 각 장르마다 평균 audio feature를 구하기 위해 모델 오브젝트 불러옴
    if genre=='k-pop':
        genre_audio_feature_all = Kpop.objects.all()
    elif genre=='pop':
        genre_audio_feature_all = Jpop.objects.all()
    elif genre=='rock':
        genre_audio_feature_all = Rock.objects.all()
    elif genre=='r&b':
        genre_audio_feature_all = Rnb.objects.all()
    elif genre=='jazz':
        genre_audio_feature_all = Jazz.objects.all()
    elif genre=='latin':
        genre_audio_feature_all = Latin.objects.all()
    elif genre=='hip hop':
        genre_audio_feature_all = Hiphop.objects.all()
    elif genre=='indie pop':
        genre_audio_feature_all = Indiepop.objects.all()
    elif genre=='alternative':
        genre_audio_feature_all = Alternative.objects.all()
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
    ax.fill(feat_cols + feat_cols[:1], r_values + r_values[:1], 'blue', alpha=0.1, label=song_name)
    
    # 장르 평균값 그래프 추가
    ax.fill(feat_cols + feat_cols[:1], genre_r_values + genre_r_values[:1], 'r', alpha=0.1, label=(genre+' 100'))

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
    image_data = base64.b64encode(buffer.read()).decode('utf-8')
    
    plt.close(fig)
    ####################################################################################################################################
    # 같은 장르의 다른 곡들 추천
    recommendations = sp.recommendations(seed_tracks=[song_id], limit=7)

    # 추천 곡과 앨범 이미지, 곡 제목, 가수, 그래프 이미지 저장
    recommendation_album_images = []
    recommendation_album_id = []
    recommendation_tracks = []
    recommendation_track_names = []
    recommendation_track_artists = []
    recommendation_tracks_preview_urls = []
    recommendations_images = []

    for track in recommendations['tracks']:
        if track['id'] != song_id and track['id'] not in recommendation_tracks and track['name'] not in recommendation_track_names:
            recommendation_album_id.append(track['album']['id'])
            recommendation_album_images.append(track['album']['images'][0]['url'])
            recommendation_tracks.append(track['id'])
            recommendation_track_names.append(track['name'])
            artists = [artist['name'] for artist in track['artists']]
            artists_str = ', '.join(artists)
            recommendation_track_artists.append(artists_str)
            recommendation_tracks_preview_urls.append(track['preview_url'])
    
    # # 데이터베이스에 곡이 없으면 저장
    # for track_id, track_name, track_preview, album_id in zip(recommendation_tracks, recommendation_track_names, recommendation_tracks_preview_urls, recommendation_album_id):
    #     existing_track = Track.objects.filter(track_id=track_id).first()

    #     if not existing_track:
    #         new_track = Track(
    #             track_id=track_id,
    #             track_name=track_name,
    #             track_preview=track_preview,
    #             album=album_id
    #         )
    #         new_track.save()

    
    for i in range(0, 5):
        audio_features = sp.audio_features(recommendation_tracks[i])

        audio_feature_data = {
            "acousticness": audio_features[0]['acousticness'],
            "danceability": audio_features[0]['danceability'],
            "energy": audio_features[0]['energy'],
            "loudness": 10**(audio_features[0]['loudness']/10),
            "speechiness": audio_features[0]['speechiness'],
            "tempo": audio_features[0]['tempo']/100,
            "valence": audio_features[0]['valence']
        }

        r_values = [audio_feature_data[col] for col in feat_cols]

        # 그래프를 생성하고 데이터 표시
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='polar')

        # 라벨의 값 변경 후 그래프 그리기
        labels = recommendation_track_names[i] + ' - ' + recommendation_track_artists[i]
        ax.fill(feat_cols + feat_cols[:1], r_values + r_values[:1], 'b', alpha=0.1, label=labels)
        
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
        recommendations_images.append(image_data1)
        plt.close(fig)
        
    context = {
        'image' : image_data,
        'current_song' : current_song,
        'recommendation_album_images': recommendation_album_images,
        'recommendation_track_names': recommendation_track_names,
        'recommendation_track_artists' : recommendation_track_artists,
        'recommendation_tracks_preview_urls' : recommendation_tracks_preview_urls,
        'recommendations_images' : recommendations_images
    }

    return render(request, 'Ssavi_app/analysis.html', context)


def recommend(request):
    return render(request, 'Ssavi_app/recommend.html')