from flask_restful import Resource

from managers.auth import auth
from managers.user import UserManager
from models import RoleType
from utils.decorators import permission_required


class DeleteCompanyUser(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def delete(self, _id):
        _id = UserManager.delete_user(_id, "Company")
        return {"message": f"Company user with ID {_id} was successfully deleted."}


class DeleteApplicantUser(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def delete(self, _id):
        _id = UserManager.delete_user(_id, "Applicant")
        return {"message": f"Applicant user with ID {_id} was successfully deleted."}
