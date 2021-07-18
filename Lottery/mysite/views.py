from django.shortcuts import render
from crawler.models import LotteryList
from django.contrib import messages
from .getlocation import getLatLng
from haversine import haversine

# Create your views here.
def index(request):
    context = {
        "lottery_stores": LotteryList.objects.order_by('-lottery_count')
    }
    return render(request, 'index.html', context=context)


def search(request):
    searchAddr = request.POST['user_address']
    # 사용자가 입력한 주소의 위도, 경도 받아오기

    lat, lng = getLatLng(searchAddr)
    userLocation = (float(lat), float(lng))

    # 위도, 경도 tuple 담긴 리스트
    locations = []


    # 기존 복권 판매소와의 거리 계산
    LotteryList.objects.all().order_by('id')

    for item in LotteryList.objects.all():
        locations.append((float(item.latitude), float(item.longitude)))

    distance = []

    for i in range(len(locations)):
        distance.append((i + 1, haversine(userLocation, locations[i])))

    distance.sort(key=lambda element:element[1])

    lottery_stores = []

    for i in range(len(distance)):
        lottery_stores.append(LotteryList.objects.get(id=distance[i][0]))

    context = {
        "lottery_stores": lottery_stores
    }
    # distance 기준으로 정렬한 리스트 html로 넘기기

    return render(request, 'search.html', context=context)
