from werkzeug.exceptions import BadRequest

from db import db
from models import AdvertisementModel, AppliedAdvertisementModel


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
        db.session.commit()

        return applied_advertisement
