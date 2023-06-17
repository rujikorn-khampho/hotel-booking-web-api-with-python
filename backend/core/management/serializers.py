from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from core.authentication.serializers import GuestReadSerializer
from core.management.models import Hotel, RoomType, Equipment, Room, Amenity, Booking


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
            'guests',
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


class BookingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['guest']

    @staticmethod
    def validate_room(value):
        if not value.is_available:
            raise serializers.ValidationError('This room is not available')
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['guest'] = request.user
        self.change_room_status(validated_data.get('room'))
        return super().create(validated_data)

    @staticmethod
    def change_room_status(room):
        room.is_available = False
        room.save()


class BookingReadSerializer(serializers.ModelSerializer):
    room = RoomReadSerializer()
    guest = GuestReadSerializer()

    class Meta:
        model = Booking
        fields = '__all__'
