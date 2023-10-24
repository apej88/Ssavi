import spotipy
from mySpotipyID import cid, csecret
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=csecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 300px 이미지 url만 가지고 오는 함수
def get_image300():
    search_result = sp.new_releases(country='KR', limit=9)
    imageurls = []
    album_image_urls = []

    for re in search_result['albums']['items']:
        for imagemedium in re['images']:
            if imagemedium.get('height') == 300:
                imageurls.append(imagemedium)
    
    for url in imageurls:
        album_image_urls.append(url['url'])


    for re in search_result['albums']['items']:
        album_image_urls.append(re['name'])

    return album_image_urls