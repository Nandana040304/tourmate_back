from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Place
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@api_view(['POST'])
def nearby_places(request):
    user_lat = float(request.data.get('latitude'))
    user_lon = float(request.data.get('longitude'))

    places = Place.objects.all()
    result = []

    for place in places:
        distance = haversine(
            user_lat,
            user_lon,
            place.latitude,
            place.longitude
        )

        if distance <= 20:
            result.append({
                "name": place.name,
                "category": place.category,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "description": place.description,
                "image": request.build_absolute_uri(place.image.url),
                "distance": round(distance, 2)
            })

    return Response(result)