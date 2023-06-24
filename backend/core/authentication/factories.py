import factory

from core.authentication.utils import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    phone = factory.Faker('phone_number', locale='th')
    address = factory.Faker('address')
    password = factory.PostGenerationMethodCall('set_password', '+KGtjFuS+kww&7c)')
