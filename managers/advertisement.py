import pandas as pd
from flask import make_response
from werkzeug.exceptions import BadRequest

from db import db
from models import AdvertisementModel, AppliedAdvertisementModel, CompanyUserModel, Positions, Status, \
    ApplicantUserModel
from schemas.response.advertisement import AdvertisementResponseSchema
from services.email_service import send_mail


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
    def get(_id):
        ad = AdvertisementModel.query.filter_by(id=_id).first()

        if ad:
            return AdvertisementManager.attach_company_to_advertisements(ad)

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
        if not data:
            raise BadRequest('Invalid JSON!')

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
        if isinstance(position, str):
            try:
                position = eval(f'Positions.{position.lower()}', {'Positions': Positions})
            except Exception:
                return []

        ads = AdvertisementModel.query.filter_by(position=position).all()

        return ads

    @staticmethod
    def approve(ad_id, user_id, current_user):
        AdvertisementManager.change_status(ad_id, user_id, current_user, Status.approved)

    @staticmethod
    def reject(ad_id, user_id, current_user):
        AdvertisementManager.change_status(ad_id, user_id, current_user, Status.rejected)

    @staticmethod
    def __validate_ad(ad, advertisements):
        for a in advertisements:
            if a.id == ad.advertisement_id:
                if ad.status == Status.approved:
                    raise BadRequest('This advertisement was already approved!')

                if ad.status == Status.rejected:
                    raise BadRequest('This advertisement was already rejected!')

                return a

        raise BadRequest('Invalid Advertisement!')

    @staticmethod
    def change_status(ad_id, user_id, current_user, status):
        applied_ad = AppliedAdvertisementModel.query.filter_by(applicant_user_id=user_id,
                                                               advertisement_id=ad_id).first()
        if not applied_ad:
            raise BadRequest('Invalid ID!')

        ad = AdvertisementManager.__validate_ad(applied_ad, current_user.advertisements)
        applicant = ApplicantUserModel.query.filter_by(id=user_id).first()

        applied_ad.status = status

        send_mail(applicant.email, applied_ad.status.value, ad.title)

        db.session.commit()

    @staticmethod
    def attach_company_to_advertisements(ad):
        company = ad.company

        ad = AdvertisementResponseSchema().dump(ad)

        ad['company'] = {}
        ad['company']['company_name'] = company.company_name
        ad['company']['address'] = company.address
        ad['company']['email'] = company.email
        ad['company']['phone'] = company.phone
        ad['company']['description'] = company.description
        ad['company']['employees_count'] = company.employees_count

        return ad

    @staticmethod
    def get_all_appliers_per_advertisement(current_user, ad_id):
        if ad_id not in [ad.id for ad in current_user.advertisements]:
            raise BadRequest('Invalid ID!')

        appliers_ids = db.session.query(AppliedAdvertisementModel.applicant_user_id).filter(
            AppliedAdvertisementModel.advertisement_id == ad_id).all()

        appliers = db.session.query(ApplicantUserModel).filter(ApplicantUserModel.id.in_(appliers_ids[0]))

        return appliers

    @staticmethod
    def get_appliers_as_csv(appliers):
        data = {}

        for r in appliers:
            for key, value in r.items():
                if key not in data.keys():
                    data[key] = []

                data[key].append(value)

        df = pd.DataFrame(data, columns=data.keys())

        resp = make_response(df.to_csv(index=False))
        resp.headers["Content-Disposition"] = f"attachment; filename=Appliers.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
