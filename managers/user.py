from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.user import ApplicantUserModel, CompanyUserModel

GLOBALS = {'ApplicantUserModel': ApplicantUserModel,
           'CompanyUserModel': CompanyUserModel}


class UserManager:
    @staticmethod
    def register(user_data, user_model):
        GLOBALS['user_data'] = user_data
        user_data['password'] = generate_password_hash(user_data['password'])
        user = eval(f'{user_model}UserModel(**user_data)', GLOBALS)

        db.session.add(user)

        try:
            db.session.commit()
        except Exception as ex:
            if ex.orig.pgcode == UNIQUE_VIOLATION:
                raise BadRequest('Please login.')
            else:
                raise InternalServerError('Server is unavailable. Please try again later.')
        return user

    @staticmethod
    def login(user_data, user_model):
        GLOBALS['user_data'] = user_data

        user = eval(f'{user_model}UserModel.query.filter_by(email=user_data[\'email\']).first()', GLOBALS)

        if not user or not check_password_hash(user.password, user_data['password']):
            raise BadRequest('Wrong username or password!')

        return user
