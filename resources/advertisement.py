from flask import request
from flask_restful import Resource

from managers.advertisement import AdvertisementManager
from managers.auth import auth
from models import RoleType
from schemas.requests.advertisement import AdvertisementCreateRequestSchema, ApplyAdvertisementRequestSchema
from schemas.response.advertisement import AdvertisementResponseSchema
from utils.decorators import validate_schema, permission_required


class AdvertisementListCreate(Resource):
    @auth.login_required
    def get(self):
        ads = AdvertisementManager.get_all_advertisements()
        return AdvertisementResponseSchema().dump(ads, many=True)

    @auth.login_required
    @permission_required(RoleType.company)
    @validate_schema(AdvertisementCreateRequestSchema)
    def post(self):
        current_user = auth.current_user()
        ad = AdvertisementManager.create(request.get_json(), current_user.id)
        return {'ad_id': ad.id}


class AdvertisementDelete(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    def delete(self, _id):
        current_user = auth.current_user()
        AdvertisementManager.delete(_id, current_user.id)
        return {'message': f'Advertisement with ID {_id} was successfully deleted.'}


class ApplyAdvertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    def post(self, _id):
        current_user = auth.current_user()
        applied_advertisement = AdvertisementManager.apply(current_user.id, _id)

        return {'message': f'You successfully applied your CV to this Ad! Status: {applied_advertisement.status.value}'}
