from flask import request
from flask_restful import Resource

from managers.advertisement import AdvertisementManager
from managers.auth import auth
from models import RoleType
from schemas.requests.advertisement import AdvertisementCreateRequestSchema, \
    AdvertisementUpdateRequestSchema
from schemas.response.advertisement import AdvertisementResponseSchema
from schemas.response.user import ApplicantResponseSchema
from utils.decorators import validate_schema, permission_required


class AdvertisementListCreate(Resource):
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


class AdvertisementGet(Resource):
    def get(self, _id):
        return AdvertisementManager.get(_id)


class AdvertisementDelete(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    def delete(self, _id):
        current_user = auth.current_user()
        AdvertisementManager.delete(_id, current_user.id)

        return {'message': f'Advertisement with ID {_id} was successfully deleted.'}


class ApplyAdvertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.applicant)
    def post(self, _id):
        current_user = auth.current_user()
        applied_advertisement = AdvertisementManager.apply(current_user.id, _id)

        return {'message': f'You successfully applied your CV to this Ad! Status: {applied_advertisement.status.value}'}


class AdvertisementUpdate(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    @validate_schema(AdvertisementUpdateRequestSchema)
    def put(self, _id):
        current_user = auth.current_user()
        ad = AdvertisementManager.update(_id, current_user.id, request.get_json())

        return AdvertisementResponseSchema().dump(ad)


class AdvertisementsPerCompany(Resource):
    def get(self, company_name):
        ads = AdvertisementManager.get_all_advertisements_by_company_name(company_name)

        return AdvertisementResponseSchema().dump(ads, many=True)


class AdvertisementsPerUserPosition(Resource):
    @auth.login_required
    @permission_required(RoleType.applicant)
    def get(self):
        current_user = auth.current_user()
        ads = AdvertisementManager.get_all_advertisements_by_position(
            current_user.position)
        return AdvertisementResponseSchema().dump(ads, many=True)


class AdvertisementsPerPosition(Resource):
    def get(self, position):
        ads = AdvertisementManager.get_all_advertisements_by_position(position)
        return AdvertisementResponseSchema().dump(ads, many=True)


class ApproveAdvertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    def post(self, ad_id, user_id):
        current_user = auth.current_user()
        AdvertisementManager.approve(ad_id, user_id, current_user)

        return {'message': f'User with ID {user_id} was approved for the job!'}


class RejectAdvertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    def post(self, ad_id, user_id):
        current_user = auth.current_user()
        AdvertisementManager.reject(ad_id, user_id, current_user)

        return {'message': f'User with ID {user_id} was rejected!'}


class GetAllAppliersPerAdvertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    def get(self, _id):
        current_user = auth.current_user()
        appliers = AdvertisementManager.get_all_appliers_per_advertisement(current_user, _id)

        return ApplicantResponseSchema().dump(appliers, many=True)


class ExportAllAppliersPerAdvertisement(Resource):
    @auth.login_required
    @permission_required(RoleType.company)
    def get(self, _id):
        current_user = auth.current_user()
        appliers = AdvertisementManager.get_all_appliers_per_advertisement(current_user, _id)

        return AdvertisementManager.get_appliers_as_csv(ApplicantResponseSchema().dump(appliers, many=True))

