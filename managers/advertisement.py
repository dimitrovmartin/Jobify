from sqlalchemy import update
from werkzeug.exceptions import BadRequest

from db import db
from models import AdvertisementModel, AppliedAdvertisementModel, CompanyUserModel


class AdvertisementManager:
    @staticmethod
    def create(data, company_user_id):
        data['company_user_id'] = company_user_id
        advertisement = AdvertisementModel(**data)

        db.session.add(advertisement)
        db.session.commit()
        return advertisement

    @staticmethod
    def apply(user_id, advertisement_id):
        if AppliedAdvertisementModel.query.filter_by(applicant_user_id=user_id,
                                                     advertisement_id=advertisement_id).first():
            raise BadRequest('You\'ve already apply your CV to this Ad!')

        applied_advertisement = AppliedAdvertisementModel(applicant_user_id=user_id, advertisement_id=advertisement_id)

        db.session.add(applied_advertisement)
        try:
            db.session.commit()
        except Exception:
            raise BadRequest('Invalid ad')
        return applied_advertisement

    @staticmethod
    def delete(_id, current_user_id):
        ad = AdvertisementModel.query.filter_by(id=_id, company_user_id=current_user_id).first()

        if not ad:
            raise BadRequest('Invalid ID!')

        db.session.delete(ad)
        db.session.commit()

    @staticmethod
    def get_all_advertisements():
        return AdvertisementModel.query.all()

    @staticmethod
    def update(_id, current_user_id, data):
        num_rows_updated = AdvertisementModel.query.filter_by(id=_id, company_user_id=current_user_id).update(data)

        if not num_rows_updated:
            raise BadRequest('Invalid ID!')

        ad = AdvertisementModel.query.filter_by(id=_id, company_user_id=current_user_id).first()

        db.session.commit()

        return ad

    @staticmethod
    def get_all_advertisements_by_company_name(company_name):
        company = CompanyUserModel.query.filter_by(company_name=company_name).first()

        if not company:
            raise BadRequest('Invalid company!')

        return company.advertisements

