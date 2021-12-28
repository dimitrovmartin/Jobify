import os
import uuid

from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError
from werkzeug.security import generate_password_hash, check_password_hash

from constants import TEMP_FILE_FOLDER
from db import db
from models import Positions, AdvertisementModel
from models.user import ApplicantUserModel, CompanyUserModel, AdminUserModel
from services.s3 import S3Service
from utils.helpers import decode_photo

s3 = S3Service()


class UserManager:
    @staticmethod
    def applicant_register(user_data, user_model):
        photo_name = f'{str(uuid.uuid4())}.{user_data["photo_extension"]}'
        path = os.path.join(TEMP_FILE_FOLDER, photo_name)

        user_data.pop("photo_extension")

        try:
            decode_photo(user_data.pop("photo"), path)
            photo_url = s3.upload_photo(path, photo_name)
        except Exception as ex:
            raise ex
        finally:
            os.remove(path)

        user_data["photo_url"] = photo_url
        user_data["password"] = generate_password_hash(user_data["password"])
        position = user_data["position"]
        position_key = [i.name for i in Positions if i.value == position][0]

        user_data["position"] = eval(f"Positions.{position_key}")

        return UserManager.create_user(user_data, user_model)

    @staticmethod
    def company_register(user_data, user_model):
        user_data["password"] = generate_password_hash(user_data["password"])
        return UserManager.create_user(user_data, user_model)

    @staticmethod
    def admin_register(user_data, user_model):
        user_data["password"] = generate_password_hash(user_data["password"])
        return UserManager.create_user(user_data, user_model)

    @staticmethod
    def create_user(user_data, user_model):
        user = eval(
            f"{user_model}UserModel(**user_data)",
            {
                "ApplicantUserModel": ApplicantUserModel,
                "CompanyUserModel": CompanyUserModel,
                "AdminUserModel": AdminUserModel,
                "user_data": user_data,
            },
        )
        try:
            db.session.add(user)
            db.session.flush()
        except Exception as ex:
            db.session.rollback()

            if ex.orig.pgcode == UNIQUE_VIOLATION:
                raise BadRequest("Please login.")
            else:
                raise InternalServerError(
                    "Server is unavailable. Please try again later."
                )
        return user

    @staticmethod
    def login(user_data, user_model):
        user = eval(
            f"{user_model}UserModel.query.filter_by(email=user_data['email']).first()",
            {
                "ApplicantUserModel": ApplicantUserModel,
                "CompanyUserModel": CompanyUserModel,
                "AdminUserModel": AdminUserModel,
                "user_data": user_data,
            },
        )

        if not user or not check_password_hash(user.password, user_data["password"]):
            raise BadRequest("Wrong username or password!")

        return user

    @staticmethod
    def delete_user(_id, user_model):
        user = eval(
            f"{user_model}UserModel.query.filter_by(id=_id).first()",
            {
                "ApplicantUserModel": ApplicantUserModel,
                "CompanyUserModel": CompanyUserModel,
                "AdminUserModel": AdminUserModel,
                "_id": _id,
            },
        )

        if not user:
            raise BadRequest(f"{user_model} user with ID {_id} does not exist!")

        # Delete all advertisements that was created from this company because i have
        # problem with cascade delete on one-to-many tables

        AdvertisementModel.query.filter_by(company_user_id=_id).delete()

        db.session.delete(user)
        db.session.flush()

        return user.id
