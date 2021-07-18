import requests
import os
KAKAO_API_KEY = os.environ.get("KAKAO_API_KEY", None)

def getLatLng(addr):
    searchAddr = addr
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={}'.format(searchAddr)
    headers = {
        "Authorization": "KakaoAK {}".format(KAKAO_API_KEY)
    }
    latitude = requests.get(url, headers=headers).json()['documents'][0]['address']['x']
    longitude = requests.get(url, headers=headers).json()['documents'][0]['address']['y']
    print(latitude, longitude)
    return (latitude, longitude)
