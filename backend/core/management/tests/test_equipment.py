from core.management.factories import EquipmentFactory
from core.management.models import Equipment
from core.management.tests.test_room_type import RoomTypeTests


class EquipmentTests(RoomTypeTests):
    model = Equipment
    factory = EquipmentFactory
