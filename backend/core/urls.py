from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.authentication.views import UserViewSet
from core.management.views import HotelViewSet, RoomTypeViewSet, AmenityViewSet, RoomViewSet

router = routers.DefaultRouter()
router.register('amenities', AmenityViewSet)
router.register('hotels', HotelViewSet)
router.register('room-types', RoomTypeViewSet)
router.register('rooms', RoomViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
