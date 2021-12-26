from flask import request
from flask_restful import Resource

from managers.auth import AuthManager, auth
from managers.user import UserManager
from models import RoleType
from schemas.requests.user import ApplicantRegisterRequestSchema, ApplicantLoginRequestSchema, \
    CompanyLoginRequestSchema, CompanyRegisterRequestSchema, AdminRegisterRequestSchema, AdminLoginRequestSchema
from utils.decorators import validate_schema, permission_required


class RegisterApplicant(Resource):
    @validate_schema(ApplicantRegisterRequestSchema)
    def post(self):
        user = UserManager.applicant_register(request.get_json(), 'Applicant')
        token = AuthManager.encode_token(user)

        return {'token': token}, 201


class LoginApplicant(Resource):
    @validate_schema(ApplicantLoginRequestSchema)
    def post(self):
        user = UserManager.login(request.get_json(), 'Applicant')
        token = AuthManager.encode_token(user)

        return {'token': token}, 200


class RegisterCompany(Resource):
    @validate_schema(CompanyRegisterRequestSchema)
    def post(self):
        user = UserManager.company_register(request.get_json(), 'Company')
        token = AuthManager.encode_token(user)

        return {'token': token}, 201


class LoginCompany(Resource):
    @validate_schema(CompanyLoginRequestSchema)
    def post(self):
        user = UserManager.login(request.get_json(), 'Company')
        token = AuthManager.encode_token(user)

        return {'token': token}, 200


class RegisterAdmin(Resource):
    @permission_required(RoleType.admin)
    @validate_schema(AdminRegisterRequestSchema)
    def post(self):
        admin = UserManager.admin_register(request.get_json(), 'Admin')
        token = AuthManager.encode_token(admin)

        return {'token': token}, 200


class LoginAdmin(Resource):
    @validate_schema(AdminLoginRequestSchema)
    def post(self):
        user = UserManager.login(request.get_json(), 'Admin')
        token = AuthManager.encode_token(user)

        return {'token': token}, 200
