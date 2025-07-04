import factory
from faker import Faker


from app.users.user_profile.models import UserProfile

faker = Faker()


EXISTS_GOOGLE_USER_ID = 20
EXISTS_GOOGLE_USER_EMAIL = "vd-boy400@yandex.ru"


class UserProfileFactory(factory.Factory):
    class Meta:
        model = UserProfile

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.name())
    email = factory.LazyFunction(lambda: faker.email())
    name = factory.LazyFunction(lambda: faker.name())
    yandex_access_token = factory.LazyFunction(lambda: faker.sha256())
    google_access_token = factory.LazyFunction(lambda: faker.sha256())