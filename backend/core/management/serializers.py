from rest_framework import serializers

from core.management.models import Hotel, RoomType, Amenity, Room


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class RoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    type = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = '__all__'
