import json

from flask_testing import TestCase

from config import create_app
from db import db
from managers.auth import AuthManager
from tests.factories import ApplicantFactory


class TestApplication(TestCase):
    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_app(self):
        return create_app("config.TestApplicationConfiguration")

    def test_authentication_missing_auth_header_raises(self):
        # Arrange
        url_methods = [
            ('/registerAdmin', "POST"),
            ('/advertisements', "POST"),
            ('/advertisements/1/appliers', "GET"),
            ('/advertisements/1/appliers/export', "GET"),
            ('/advertisements/1/apply', "POST"),
            ('/advertisements/1/delete', "DELETE"),
            ('/advertisements/1/update', "PUT"),
            ('/advertisements/userPosition', "GET"),
            ('/advertisements/1/1/approve', "POST"),
            ('/advertisements/1/1/reject', "POST"),
            ('/companyUsers/1/delete', "DELETE"),
            ('/applicantUsers/1/delete', "DELETE"),

        ]

        # Act
        for url, method in url_methods:
            if method == "GET":
                resp = self.client.get(url)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}))
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}))
            else:
                resp = self.client.delete(url)

            # Assert
            assert resp.status_code == 400
            assert resp.json == {'message': 'Invalid token!'}

    def test_protected_company_endpoints_require_company_rights(self):
        url_methods = [
            ('/advertisements', "POST"),
            ('/advertisements/1/appliers', "GET"),
            ('/advertisements/1/appliers/export', "GET"),
            ('/advertisements/1/delete', "DELETE"),
            ('/advertisements/1/update', "PUT"),
            ('/advertisements/1/1/approve', "POST"),
            ('/advertisements/1/1/reject', "POST"),
        ]

        applier = ApplicantFactory()
        token = AuthManager.encode_token(applier)
        headers = {"Authorization": f"Bearer {token}"}

        for url, method in url_methods:

            if method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}), headers=headers)
            else:
                resp = self.client.delete(url, headers=headers)

            assert resp.status_code == 403
            assert resp.json == {'message': 'You don`t have access to this resource!'}

    def test_protected_admin_endpoints_require_admin_rights(self):
        url_methods = [
            ('/registerAdmin', "POST"),
            ('/companyUsers/1/delete', "DELETE"),
            ('/applicantUsers/1/delete', "DELETE"),
        ]

        applier = ApplicantFactory()
        token = AuthManager.encode_token(applier)
        headers = {"Authorization": f"Bearer {token}"}

        for url, method in url_methods:

            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)

            assert resp.status_code == 403
            assert resp.json == {'message': 'You don`t have access to this resource!'}
