from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail
from .models import PoliceStation
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat/2) ** 2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_sos(request):

    user = request.user  # 🔥 logged in user

    user_lat = float(request.data.get("latitude"))
    user_lon = float(request.data.get("longitude"))

    stations = PoliceStation.objects.all()

    if not stations:
        return Response({"error": "No police stations found"}, status=400)

    nearest_station = None
    min_distance = float("inf")

    for station in stations:
        distance = calculate_distance(
            user_lat, user_lon,
            station.latitude, station.longitude
        )

        if distance < min_distance:
            min_distance = distance
            nearest_station = station

    # 🔥 Get correct user fields
    name = user.full_name
    mobile = user.mobile
    blood_group = user.blood_group
    emergency1 = user.emergency_contact1
    emergency2 = user.emergency_contact2
    medical = user.medical_condition

    subject = "🚨 SOS ALERT - TourMate Emergency"

    message = f"""
🚨 SOS ALERT 🚨

👤 Name: {name}
📞 Mobile: {mobile}
🩸 Blood Group: {blood_group}
⚕ Medical Condition: {medical if medical else "None"}

📱 Emergency Contact 1: {emergency1}
📱 Emergency Contact 2: {emergency2 if emergency2 else "Not Provided"}

📍 Location:
https://maps.google.com/?q={user_lat},{user_lon}

Immediate assistance required.
"""

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [nearest_station.email],
        fail_silently=False,
    )

    return Response({
        "success": True,
        "sent_to": nearest_station.name,
        "email": nearest_station.email
    })