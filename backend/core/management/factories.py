import factory

from core.management.constants import ROOM_TYPE_ELEMENTS, EQUIPMENT_ELEMENTS, HOTEL_ELEMENTS, ROOM_NAME_ELEMENTS
from core.management.models import RoomType, Equipment, Hotel, Amenity, Room


class RoomTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoomType

    name = factory.Faker('random_element', elements=ROOM_TYPE_ELEMENTS)
    description = factory.Faker('sentence')


class EquipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Equipment

    name = factory.Faker('random_element', elements=EQUIPMENT_ELEMENTS)
    description = factory.Faker('sentence')


class HotelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hotel

    name = factory.Faker('random_element', elements=HOTEL_ELEMENTS)
    description = factory.Faker('sentence')
    address = factory.Faker('sentence')

    @factory.post_generation
    def rooms(self, create, extracted):
        if not create:
            return

        if extracted:
            for room in extracted:
                self.rooms.add(room)


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    hotel = factory.SubFactory(HotelFactory)
    type = factory.SubFactory(RoomTypeFactory)
    name = factory.Faker('random_element', elements=ROOM_NAME_ELEMENTS)
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    is_available = factory.Faker('boolean')

    @factory.post_generation
    def equipments(self, create, extracted):
        if not create:
            return

        if extracted:
            for equipment in extracted:
                self.equipments.add(equipment)

    @factory.post_generation
    def guests(self, create, extracted):
        if not create:
            return

        if extracted:
            for guest in extracted:
                self.guests.add(guest)


class AmenityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Amenity

    room = factory.SubFactory(RoomFactory)
    equipment = factory.SubFactory(EquipmentFactory)
    quantity = factory.Faker('random_int', min=1, max=5)
