from resources.admin import DeleteCompanyUser, DeleteApplicantUser
from resources.advertisement import AdvertisementListCreate, ApplyAdvertisement, AdvertisementDelete, \
    AdvertisementUpdate, AdvertisementsPerCompany, AdvertisementsPerUserPosition, ApproveAdvertisement, \
    RejectAdvertisement, AdvertisementsPerPosition, AdvertisementGet, GetAllAppliersPerAdvertisement, \
    ExportAllAppliersPerAdvertisement
from resources.auth import RegisterApplicant, LoginApplicant, RegisterCompany, LoginCompany, LoginAdmin, RegisterAdmin

routes = (
    (RegisterApplicant, '/registerApplicant'),
    (LoginApplicant, '/loginApplicant'),
    (RegisterCompany, '/registerCompany'),
    (LoginCompany, '/loginCompany'),
    (RegisterAdmin, '/registerAdmin'),
    (LoginAdmin, '/loginAdmin'),
    (AdvertisementListCreate, '/advertisements'),
    (AdvertisementGet, '/advertisements/<int:_id>'),
    (GetAllAppliersPerAdvertisement, '/advertisements/<int:_id>/appliers'),
    (ExportAllAppliersPerAdvertisement, '/advertisements/<int:_id>/appliers/export'),
    (ApplyAdvertisement, '/advertisements/<int:_id>/apply'),
    (AdvertisementDelete, '/advertisements/<int:_id>/delete'),
    (AdvertisementUpdate, '/advertisements/<int:_id>/update'),
    (AdvertisementsPerCompany, '/advertisements/<string:company_name>'),
    (AdvertisementsPerUserPosition, '/advertisements/userPosition'),
    (AdvertisementsPerPosition, '/advertisements/position/<string:position>'),
    (ApproveAdvertisement, '/advertisements/<int:ad_id>/<int:user_id>/approve'),
    (RejectAdvertisement, '/advertisements/<int:ad_id>/<int:user_id>/reject'),
    (DeleteCompanyUser, '/companyUsers/<int:_id>/delete'),
    (DeleteApplicantUser, '/applicantUsers/<int:_id>/delete'),
)
