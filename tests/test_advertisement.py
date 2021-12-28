import json
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from models import AdvertisementModel, AppliedAdvertisementModel, Status
from tests.factories import (
    CompanyFactory,
    ApplicantFactory,
    AdvertisementFactory,
    AppliedAdFactory,
)
from tests.helpers import generate_token, object_as_dict, mock_smtp


class TestAdvertisement(TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        self.headers = {"Content-Type": "application/json"}
        return create_app("config.TestApplicationConfiguration")

    def test_create_ad_invalid_input_fields_raises(self):
        url = "/advertisements"
        data = {"title": "Searching for Test Testov", "description": "biva rabotata"}

        company = CompanyFactory()
        token = generate_token(company)
        self.headers.update({"Authorization": f"Bearer {token}"})
        ads = AdvertisementModel.query.all()
        assert len(ads) == 0

        for key in data:
            copy_data = data.copy()
            copy_data.pop(key)
            resp = self.client.post(
                url, data=json.dumps(copy_data), headers=self.headers
            )
            assert resp.status_code == 400
            assert resp.json == {"message": {key: ["Missing data for required field."]}}

        ads = AdvertisementModel.query.all()
        assert len(ads) == 0

    def test_invalid_fields_length_raises(self):
        long_text = "a" * 200
        url = "/advertisements"
        data = {"title": f"{long_text}", "description": f"{long_text}"}

        company = CompanyFactory()
        token = generate_token(company)
        self.headers.update({"Authorization": f"Bearer {token}"})
        ads = AdvertisementModel.query.all()
        assert len(ads) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        assert resp.status_code == 400
        assert resp.json == {
            "message": {
                "description": ["Length must be between 5 and 100."],
                "title": ["Length must be between 5 and 100."],
            }
        }

        ads = AdvertisementModel.query.all()
        assert len(ads) == 0

    def test_create_ad(self):
        url = "/advertisements"

        data = {
            "title": "Searching for Software Developer",
            "position": "Software Developer",
            "description": "biva rabotata",
            "salary": 650,
        }

        company = CompanyFactory()
        token = generate_token(company)
        self.headers.update({"Authorization": f"Bearer {token}"})
        ads = AdvertisementModel.query.all()
        assert len(ads) == 0

        resp = self.client.post(url, data=json.dumps(data), headers=self.headers)

        ads = AdvertisementModel.query.all()
        assert len(ads) == 1

        ad = object_as_dict(ads[0])
        ad.pop("company_user_id")
        ad["position"] = ad["position"].value

        assert ad == {"id": ad["id"], **data}

    def test_apply_advertisement(self):
        url = "/advertisements/0/apply"

        company = CompanyFactory()
        ad = AdvertisementFactory()
        applicant = ApplicantFactory()
        token = generate_token(applicant)
        self.headers.update({"Authorization": f"Bearer {token}"})

        resp = self.client.post(url, headers=self.headers)

        assert resp.json == {
            "message": "You successfully applied your CV to this Ad! Status: sent"
        }

        applied_ad = AppliedAdvertisementModel.query.filter_by(
            applicant_user_id=applicant.id, advertisement_id=0
        ).first()

        assert applied_ad is not None

    @patch("services.email_service.send_mail", mock_smtp)
    def test_approve_ad(self):
        url = "/advertisements/0/0/approve"

        company = CompanyFactory()
        ad = AdvertisementFactory()
        applicant = ApplicantFactory()
        applied_ad = AppliedAdFactory()

        token = generate_token(company)
        self.headers.update({"Authorization": f"Bearer {token}"})

        resp = self.client.post(url, headers=self.headers)

        assert resp.json == {"message": "User with ID 0 was approved for the job!"}

        applied_ad = AppliedAdvertisementModel.query.filter_by(
            applicant_user_id=applicant.id, advertisement_id=0
        ).first()

        assert applied_ad.status == Status.approved

    @patch("services.email_service.send_mail", mock_smtp)
    def test_reject_ad(self):
        url = "/advertisements/0/0/reject"

        company = CompanyFactory()
        ad = AdvertisementFactory()
        applicant = ApplicantFactory()
        applied_ad = AppliedAdFactory()

        token = generate_token(company)
        self.headers.update({"Authorization": f"Bearer {token}"})

        resp = self.client.post(url, headers=self.headers)

        assert resp.json == {"message": "User with ID 0 was rejected!"}

        applied_ad = AppliedAdvertisementModel.query.filter_by(
            applicant_user_id=applicant.id, advertisement_id=0
        ).first()

        assert applied_ad.status == Status.rejected
