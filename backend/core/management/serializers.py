from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from core.management.models import Hotel, RoomType, Equipment, Room, Amenity


class AmenityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        exclude = ['room']


class RoomWriteSerializer(WritableNestedModelSerializer):
    amenities = AmenityWriteSerializer(many=True)

    class Meta:
        model = Room
        exclude = [
            'hotel',
            'equipments',
        ]


class HotelWriteSerializer(WritableNestedModelSerializer):
    rooms = RoomWriteSerializer(many=True)

    class Meta:
        model = Hotel
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class AmenityReadSerializer(AmenityWriteSerializer):
    equipment = EquipmentSerializer()


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'


class RoomReadSerializer(RoomWriteSerializer):
    amenities = AmenityReadSerializer(many=True)
    type = RoomTypeSerializer()


class HotelRetrieveSerializer(HotelWriteSerializer):
    rooms = RoomReadSerializer(many=True)


class HotelListSerializer(HotelRetrieveSerializer):
    rooms = None
