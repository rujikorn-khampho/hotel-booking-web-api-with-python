from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.authentication.views import UserViewSet
from core.management.views import HotelViewSet, RoomTypeViewSet, EquipmentViewSet, BookingViewSet

router = routers.DefaultRouter()
router.register('bookings', BookingViewSet)
router.register('equipments', EquipmentViewSet)
router.register('hotels', HotelViewSet)
router.register('room-types', RoomTypeViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
