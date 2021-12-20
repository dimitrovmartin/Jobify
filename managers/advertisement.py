from werkzeug.exceptions import BadRequest

from db import db
from models import AdvertisementModel, AppliedAdvertisementModel, CompanyUserModel, Positions, Status


class AdvertisementManager:
    @staticmethod
    def create(data, company_user_id):
        data['company_user_id'] = company_user_id
        position = data['position']
        position_key = [i.name for i in Positions if i.value == position][0]

        data['position'] = eval(f'Positions.{position_key}')
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

    @staticmethod
    def get_all_advertisements_by_position(position):
        ads = AdvertisementModel.query.filter_by(position=position).all()

        return ads

    @staticmethod
    def approve(ad_id, user_id, current_user):
        ad = AppliedAdvertisementModel.query.filter_by(applicant_user_id=user_id, advertisement_id=ad_id).first()
        if not ad:
            raise BadRequest('Invalid ID!')

        AdvertisementModel.__validate_ad(ad, current_user.advertisements)

        ad.status = Status.approved
        db.session.commit()

    @staticmethod
    def reject(ad_id, user_id, current_user):
        ad = AppliedAdvertisementModel.query.filter_by(applicant_user_id=user_id, advertisement_id=ad_id).first()
        if not ad:
            raise BadRequest('Invalid ID!')

        AdvertisementModel.__validate_ad(ad, current_user.advertisements)

        ad.status = Status.rejected
        db.session.commit()

    @staticmethod
    def __validate_ad(ad, advertisements):
        if ad.advertisement_id not in [a.id for a in advertisements]:
            raise BadRequest('Invalid Advertisement!')

        if ad.status == Status.approved:
            raise BadRequest('This advertisement was already approved!')

        if ad.status == Status.rejected:
            raise BadRequest('This advertisement was already rejected!')
