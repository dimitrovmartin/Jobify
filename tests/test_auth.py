import json
import os
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import TEMP_FILE_FOLDER
from db import db
from models import ApplicantUserModel, RoleType, CompanyUserModel
from services.s3 import S3Service
from tests.helpers import object_as_dict, encoded_photo, mock_uuid


class TestAuth(TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfiguration")

    @patch("uuid.uuid4", mock_uuid)
    @patch.object(S3Service, "upload_photo", return_value="some.s3.url")
    def test_register_applicant(self, mocked_upload):
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
            "phone": "0879696799",
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
        data.pop("photo")
        extension = data.pop("photo_extension")
        applicant["position"] = applicant["position"].value

        assert applicant == {
            "id": applicant["id"],
            "role": RoleType.applicant,
            "photo_url": applicant["photo_url"],
            **data,
        }

        photo_name = f"{mock_uuid()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, photo_name)
        mocked_upload.assert_called_once_with(path, photo_name)

    @patch.object(S3Service, "upload_photo", return_value="some.s3.url")
    def test_applicant_already_exists_raises(self, mocked_upload):
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
            "phone": "0123456789",
        }

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201

        resp = self.client.post(
            url, data=json.dumps(data), headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 400
        assert resp.json == {"message": "Please login."}

    def test_register_company(self):
        url = "/registerCompany"

        data = {
            "company_name": "Test name",
            "address": "Test address",
            "employees_count": 20,
            "description": "Test description",
            "email": "Test@Test.com",
            "password": "123456",
            "phone": "0123456789",
        }

        companies = CompanyUserModel.query.all()

        assert len(companies) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201
        assert "token" in resp.json

        companies = CompanyUserModel.query.all()

        assert len(companies) == 1

        company = object_as_dict(companies[0])
        company.pop("password")
        data.pop("password")

        assert company == {
            "id": company["id"],
            "role": RoleType.company,
            **data,
        }

    def test_company_already_exists_raises(self):
        url = "/registerCompany"

        data = {
            "company_name": "Test name",
            "address": "Test address",
            "employees_count": 20,
            "description": "Test description",
            "email": "Test@Test.com",
            "password": "123456",
            "phone": "0123456789",
        }

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 201

        resp = self.client.post(
            url, data=json.dumps(data), headers={"Content-Type": "application/json"}
        )
        assert resp.status_code == 400
        assert resp.json == {"message": "Please login."}
