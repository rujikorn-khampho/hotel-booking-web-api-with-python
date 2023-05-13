from rest_framework import serializers

from core.authentication.utils import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']
