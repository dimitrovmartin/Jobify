from flask import request
from flask_restful import Resource

from managers.advertisement import AdvertisementManager
from managers.auth import auth
from models import RoleType
from schemas.requests.advertisement import AdvertisementCreateRequestSchema, ApplyAdvertisementRequestSchema
from utils.decorators import validate_schema, permission_required


class Advertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    @validate_schema(AdvertisementCreateRequestSchema)
    def post(self):
        current_user = auth.current_user()
        ad = AdvertisementManager.create(request.get_json(), current_user.id)
        return {'ad_id': ad.id}


class ApplyAdvertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    @validate_schema(ApplyAdvertisementRequestSchema)
    def post(self):
        current_user = auth.current_user()
        applied_advertisement = AdvertisementManager.apply(current_user.id, request.get_json()['id'])

        return {'message': f'You successfully applied your CV to this Ad! Status: {applied_advertisement.status.value}'}
