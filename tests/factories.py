from random import randint

import factory

from db import db
from models import ApplicantUserModel, RoleType, Positions, CompanyUserModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class ApplicantFactory(BaseFactory):
    class Meta:
        model = ApplicantUserModel

    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    education = 'some educ'
    role = RoleType.applicant
    photo_url = 'photo.url'
    position = Positions.software_developer


class CompanyFactory(BaseFactory):
    class Meta:
        model = CompanyUserModel

    id = factory.Sequence(lambda n: n)
    company_name = factory.Faker("first_name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    role = RoleType.company
    address = factory.Faker('address')
    description = 'some desc'
    employees_count = str(randint(10, 1000))
