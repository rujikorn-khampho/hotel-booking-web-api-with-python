import factory

from core.management.constants import ROOM_TYPE_ELEMENTS, EQUIPMENT_ELEMENTS
from core.management.models import RoomType, Equipment


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
