from db import db
from models import AdvertisementModel


class AdvertisementManager:
    @staticmethod
    def create(data, company_user_id):
        data['company_user_id'] = company_user_id

        advertisement = AdvertisementModel(**data)

        db.session.add(advertisement)
        db.session.commit()
        return advertisement
