from django.db import models


class AbstractNameDescription(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Hotel(AbstractNameDescription):
    address = models.TextField()


class RoomType(AbstractNameDescription):
    pass


class Amenity(AbstractNameDescription):
    pass


class Room(models.Model):
    hotel = models.ForeignKey(
        'management.Hotel',
        on_delete=models.CASCADE,
        related_name='rooms',
    )
    type = models.ForeignKey(
        'management.RoomType',
        on_delete=models.CASCADE,
        related_name='rooms',
    )
    number = models.CharField(max_length=20)
    amenities = models.ManyToManyField(
        'management.Amenity',
        related_name='rooms',
        through='management.RoomAmenity',
        blank=True,
    )

    objects = models.Manager()


class RoomAmenity(models.Model):
    room = models.ForeignKey(
        'management.Room',
        on_delete=models.CASCADE,
        related_name='room_amenities',
    )
    amenity = models.ForeignKey(
        'management.Amenity',
        on_delete=models.CASCADE,
        related_name='room_amenities',
    )
    amenity_count = models.PositiveSmallIntegerField()

    objects = models.Manager()
