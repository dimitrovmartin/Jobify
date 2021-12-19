from flask import request
from flask_restful import Resource

from managers.advertisement import AdvertisementManager
from managers.auth import auth
from models import RoleType
from schemas.requests.advertisement import AdvertisementCreateRequestSchema
from utils.decorators import validate_schema, permission_required


class Advertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    @validate_schema(AdvertisementCreateRequestSchema)
    def post(self):
        current_user = auth.current_user()
        ad = AdvertisementManager.create(request.get_json(), current_user.id)
        return {'ad_id': ad.id}
