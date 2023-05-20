from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core.authentication.views import UserViewSet, RegisterViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('register', RegisterViewSet, basename='register')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
