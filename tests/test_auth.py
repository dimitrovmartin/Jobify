import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import ApplicantUserModel, RoleType
from tests.helpers import object_as_dict, encoded_photo


class TestAuth(TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfiguration")

    def test_register_applicant(self):
        url = "/registerApplicant"

        data = {
            "first_name": "Marto",
            "last_name": "Dimitrov",
            "position": "Human Resources",
            "education": "Bachelor degree",
            "photo": encoded_photo,
            "photo_extension": "jpg",
            "email": "vipernapier751@gmail.com",
            "password": "123456",
            "phone": "0879696799"

        }

        applicants = ApplicantUserModel.query.all()
        assert len(applicants) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201
        assert "token" in resp.json

        applicants = ApplicantUserModel.query.all()

        assert len(applicants) == 1

        applicant = object_as_dict(applicants[0])
        applicant.pop("password")

        data.pop("password")
        data.pop('photo')
        data.pop('photo_extension')
        applicant['position'] = applicant['position'].value

        assert applicant == {
            "id": applicant["id"],
            "role": RoleType.applicant,
            "photo_url": applicant['photo_url'],
            **data,
        }

    def test_user_already_exists_raises(self):
        url = "/registerApplicant"

        data = {
            "first_name": "Marto",
            "last_name": "Dimitrov",
            "position": "Human Resources",
            "education": "Bachelor degree",
            "photo": encoded_photo,
            "photo_extension": "jpg",
            "email": "vipernapier751@gmail.com",
            "password": "123456",
            "phone": "0879696799"

        }

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201

        resp = self.client.post(
            url, data=json.dumps(data), headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 400
        assert resp.json == {"message": "Please login."}
