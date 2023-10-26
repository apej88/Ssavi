from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q 
from mysqlsearcher import *
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

import spotipy
from mySpotipyID import cid, csecret
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=csecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Create your views here.
def index(request):
    return render(request, 'Ssavi_app/index.html')

def recommend(request):
    # 로그인하지 않은 채 그냥 들어간다면 장르는 except로 고정된다.
    # 유저의 인증정보를 조회하여 id값을 보낸다.
    recom_albums = Albums.objects.all()
    likealbum = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in recom_albums:
            if LikedAlbum.objects.filter(id=user_id, album_id=i.album_id).exists():
                likealbum.append(i.album_id)

    context = {
        'albums': recom_albums,
        'likealbum' : likealbum
    }

        # user_genre_list = DBsearch.selectUserGenre(str(user_id))
    if request.user.is_authenticated:
        user_id = request.user.id

        # user_id 정수를 받아오면 users_app_user에서 user_genre 검색
        try:
            current_login_user = UsersAppUser.objects.get(id=user_id)
            if current_login_user.user_genre is None:
                user_genre_list = []
            else:
                user_genre_list = current_login_user.user_genre.split(",")
        except UsersAppUser.DoesNotExist:
            user_genre_list = []

        return render(request, 'Ssavi_app/genre_music.html', {'recom_albums':recom_albums, 'user_genre_list':user_genre_list, 'context':context})

    else:
        user_genre_list = ['jazz', 'k-pop', 'J-pop', 'R&B']
    return render(request, 'Ssavi_app/genre_music.html', {'recom_albums':recom_albums, 'user_genre_list':user_genre_list, 'context':context})

def get_albuminfo():
    search_result = sp.new_releases(country='KR', limit=9)
    album_infos = []
    album_image_urls = []

    for re in search_result['albums']['items']:
        album_image_urls.append(re['name'])
        album_image_urls.append(re['artists'][0]['name'])
        album_image_urls.append(re['release_date'])
        for imagemedium in re['images']:
            if imagemedium.get('height') == 300:
                album_image_urls.append(imagemedium['url'])

    for i in range(0, len(album_image_urls), 4):
        album_info = {
            'albumname': album_image_urls[i],
            'artistname': album_image_urls[i+1],
            'releasedate': album_image_urls[i+2],
            'url': album_image_urls[i+3]
        }
        album_infos.append(album_info)

    return album_infos

def music_recommend(request):
    tracks = Tracks.objects.all()
    liketrack = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in tracks:
            if LikedTrack.objects.filter(id=user_id, track_id=i.track_id).exists():
                liketrack.append(i.track_id)

    context = {
        'tracks': tracks,
        'liketrack' : liketrack
    }

    return render(request, 'Ssavi_app/music_recommend.html', context)

def detail(request, ab_id):
    album = get_object_or_404(Albums, pk=ab_id)
    songs = sp.album_tracks(album_id=ab_id)['items']
    songs_data = [] # 앨범 안의 노래들의 정보를 담을 리스트
    tracks = Tracks.objects.all()
    liketrack = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in tracks:
            if LikedTrack.objects.filter(id=user_id, track_id=i.track_id).exists():
                liketrack.append(i.track_id)

    albums = Albums.objects.all()
    likealbum = []
    if request.user.is_authenticated:
            user_id = request.user.id
            for i in albums:
                if LikedAlbum.objects.filter(id=user_id, album_id=i.album_id).exists():
                    likealbum.append(i.album_id)

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
        'genres': genres,
        'likealbum' : likealbum,
        'tracks': tracks,
        'liketrack' : liketrack
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

    Album = get_object_or_404(Albums, pk=album_id)

    genre = Album.album_genre

    current_song = [album_image_url, song_name, artist_name, Track.track_preview, song_id]
    
    # 각 장르마다 평균 audio feature를 구하기 위해 모델 오브젝트 불러옴
    if genre=='k-pop':
        genre_audio_feature_all = Kpop.objects.all()
    elif genre == 'alternative':
        genre_audio_feature_all = Alternative.objects.all()
    elif genre == 'indie Pop':
        genre_audio_feature_all = Indiepop.objects.all()
    elif genre=='J-pop':
        genre_audio_feature_all = Jpop.objects.all()
    elif genre == 'rock':
        genre_audio_feature_all = Rock.objects.all()
    elif genre == 'R&B':
        genre_audio_feature_all = Rnb.objects.all()
    elif genre == 'jazz':
        genre_audio_feature_all = Jazz.objects.all()
    elif genre == 'latin':
        genre_audio_feature_all = Latin.objects.all()
    elif genre == 'hip hop':
        genre_audio_feature_all = Hiphop.objects.all()
    elif genre == 'electro':
        genre_audio_feature_all = Electro.objects.all()
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



    print(type(avg_acousticness))
    print(type(avg_danceability))

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
    recommendations = sp.recommendations(seed_tracks=[song_id], target_acousticness=audio_feature.acousticness, target_danceability=audio_feature.danceability,
                                    target_energy=audio_feature.energy, target_loudness=audio_feature.loudness,
                                    target_speechiness=audio_feature.speechiness, target_tempo=audio_feature.tempo,
                                    target_valence=audio_feature.valence, limit=7)

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
    
    tracks = Tracks.objects.all()
    liketrack = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in tracks:
            if LikedTrack.objects.filter(id=user_id, track_id=i.track_id).exists():
                liketrack.append(i.track_id)

    context = {
        'image' : image_data,
        'current_song' : current_song,
        'recommendation_album_images': recommendation_album_images,
        'recommendation_track_names': recommendation_track_names,
        'recommendation_track_artists' : recommendation_track_artists,
        'recommendation_tracks_preview_urls' : recommendation_tracks_preview_urls,
        'recommendations_images' : recommendations_images,
        'tracks': tracks,
        'liketrack' : liketrack
    }

    return render(request, 'Ssavi_app/analysis.html', context)

# 태주님 index 페이지에서 기능할 함수
def album_list(request):
    page = int(request.GET.get('page', 1))
    albums_per_page = 15 # 페이지당 앨범 수
    albums = Albums.objects.all().order_by('-album_release_date')
    paginator = Paginator(albums, albums_per_page)
    page_albums = paginator.get_page(page)

    likealbum = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in albums:
            if LikedAlbum.objects.filter(id=user_id, album_id=i.album_id).exists():
                likealbum.append(i.album_id)

    context = {
        'albums': page_albums,
        'likealbum' : likealbum
    }

    return render(request, 'Ssavi_app/index.html', context)


def like_track(request):
    if request.method == 'POST':
        track_id = request.POST.get('track_id')
        id = request.POST.get('id')
      
        try:
            track_id = Tracks.objects.get(track_id=track_id)
            id = UsersAppUser.objects.get(id=id)

            liked_track, created = LikedTrack.objects.get_or_create(track=track_id, id=id)

            if created:
                message = "트랙 따봉"
            else:
                liked_track.delete()
                message = "트랙 따봉 해제"

            return JsonResponse({'message': message})
        except UsersAppUser.DoesNotExist:
            return JsonResponse({'error': '사용자가 존재하지 않습니다.'}, status=404)
        except Tracks.DoesNotExist:
            return JsonResponse({'error': '트랙이 존재하지 않습니다.'}, status=404)
        
def like_album(request):
    if request.method == 'POST':
        album_id = request.POST.get('album_id')
        id = request.POST.get('id')
      
        try:
            id = UsersAppUser.objects.get(id=id)
            album_id = Albums.objects.get(album_id=album_id)

            liked_album, created = LikedAlbum.objects.get_or_create(album=album_id, id=id)

            if created:
                message = "앨범 좋아요"
            else:
                liked_album.delete()
                message = "앨범 좋아요 해제"

            return JsonResponse({'message': message})
        except UsersAppUser.DoesNotExist:
            return JsonResponse({'error': '사용자가 존재하지 않습니다.'}, status=404)
        except Albums.DoesNotExist:
            return JsonResponse({'error': '트랙이 존재하지 않습니다.'}, status=404)
        

# 검색 쿼리 수행
def album_search(request):
    if request.method == "POST":
        search_condition = request.POST['search_condition']
        keyword = request.POST['keyword']
        request.session['keyword'] = keyword  # 세션에 키워드 저장
        request.session['search_condition'] = search_condition  # 세션에 검색 조건 저장
    else:
        keyword = request.session.get('keyword')  # 세션에서 키워드 가져오기
        search_condition = request.session.get('search_condition')  # 세션에서 검색 조건 가져오기

    if search_condition == "album_name":
        album_list = Albums.objects.filter(Q(album_name__contains=keyword)) 
    elif search_condition == "album_genre":
        album_list = Albums.objects.filter(Q(album_genre__contains=keyword)) 
    else:
        album_list = Albums.objects.filter(Q(album_artist__contains=keyword)) 

    page = int(request.GET.get('page', 1))
    albums_per_page = 15 # 페이지당 앨범 수
    paginator = Paginator(album_list, albums_per_page)
    page_albums = paginator.get_page(page)

    likealbum = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in album_list:
            if LikedAlbum.objects.filter(id=user_id, album_id=i.album_id).exists():
                likealbum.append(i.album_id)

    context = {
        'albums': page_albums,
        'likealbum' : likealbum
    }

    return render(request, 'ssavi_app/index_search.html', context)


# 마이페이지 함수
def playlist(request):
    playlists = PlayList.objects.all()
    return render(request, 'Ssavi_app/playlist.html', {"playlists":playlists})

def liked_album(request):
    albums = Albums.objects.all()
    likealbum = []
    liked_albums_info = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in albums:
            if LikedAlbum.objects.filter(id=user_id, album_id=i.album_id).exists():
                likealbum.append(i.album_id)

    if request.user.is_authenticated:
        user_id = request.user.id
        for album_id in likealbum:
            album = Albums.objects.get(album_id=album_id)
            album_image = album.album_image
            track_info = {
                'album_image' : album_image,
                'album_id' : album_id,
                'album_name': album.album_name,
                'album_artist': album.album_artist,
            }
            liked_albums_info.append(track_info)


    return render(request, 'Ssavi_app/liked_album.html', {'liked_albums_info' : liked_albums_info, 'likealbum' : likealbum})

def liked_track(request):
    tracks = Tracks.objects.all()
    liketrack = []
    liked_tracks_info = []

    if request.user.is_authenticated:
        user_id = request.user.id
        for i in tracks:
            if LikedTrack.objects.filter(id=user_id, track_id=i.track_id).exists():
                liketrack.append(i.track_id)


    if request.user.is_authenticated:
        user_id = request.user.id
        for track_id in liketrack:
            track = Tracks.objects.get(track_id=track_id)
            album_image = sp.album(track.album_id)['images'][0]['url']
            track_info = {
                'album_image' : album_image,
                'track_id' : track_id,
                'track_name': track.track_name,
                'track_preview': track.track_preview,
            }
            liked_tracks_info.append(track_info)
    


    return render(request, 'Ssavi_app/liked_track.html', {'liked_tracks_info' : liked_tracks_info, 'liketrack' : liketrack})

def delPlayList(request, pk):
    data = PlayList.objects.get(id=pk)
    data.delete()
    return redirect('playlist')

def mypage(request):
    return render(request, 'Ssavi_app/mypage.html')