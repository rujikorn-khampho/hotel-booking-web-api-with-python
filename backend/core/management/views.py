from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from core.management.models import Hotel, RoomType, Equipment, Booking
from core.management.serializers import (
    BookingReadSerializer,
    BookingWriteSerializer,
    EquipmentSerializer,
    HotelListSerializer,
    HotelRetrieveSerializer,
    HotelWriteSerializer,
    RoomTypeSerializer,
)


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.prefetch_related(
        'rooms__amenities__equipment',
        'rooms__type',
    ).order_by(
        'pk',
    )
    write_serializer_class = HotelWriteSerializer
    list_serializer_class = HotelListSerializer
    retrieve_serializer_class = HotelRetrieveSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        serializer_action_mapping = {
            'create': self.write_serializer_class,
            'retrieve': self.retrieve_serializer_class,
            'update': self.write_serializer_class,
            'partial_update': self.write_serializer_class,
        }

        return serializer_action_mapping.get(
            self.action,
            self.list_serializer_class,
        )


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.order_by('pk')
    serializer_class = RoomTypeSerializer
    permission_classes = [IsAdminUser]


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.order_by('pk')
    serializer_class = EquipmentSerializer
    permission_classes = [IsAdminUser]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.prefetch_related(
        'room__amenities__equipment',
    ).select_related(
        'room__type',
        'guest',
    ).order_by(
        'pk',
    )
    write_serializer_class = BookingWriteSerializer
    read_serializer_class = BookingReadSerializer

    def get_queryset(self):
        if self.request.user.is_superuser is False:
            return super().get_queryset().filter(
                guest=self.request.user,
            )
        return super().get_queryset()

    def get_serializer_class(self):
        serializer_action_mapping = {
            'create': self.write_serializer_class,
            'update': self.write_serializer_class,
            'partial_update': self.write_serializer_class,
        }

        return serializer_action_mapping.get(
            self.action,
            self.read_serializer_class,
        )
