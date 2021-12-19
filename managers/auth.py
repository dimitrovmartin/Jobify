from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import BadRequest

from models import ApplicantUserModel, CompanyUserModel, AdminUserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            'sub': user.id,
            'exp': datetime.utcnow() + timedelta(days=100),
            'role': user.role.value
        }

        return jwt.encode(payload, key=config('JWT_KEY'), algorithm='HS256')

    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(token, key=config('JWT_KEY'), algorithms=['HS256'])
            return data['sub'], data['role']
        except jwt.ExpiredSignatureError:
            raise BadRequest('Token expired!')
        except jwt.InvalidTokenError:
            raise BadRequest('Invalid token!')


auth = HTTPTokenAuth(scheme='Bearer')


@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)

    user = eval(f'{role.title()}UserModel.query.filter_by(id=user_id).first()')

    return user
