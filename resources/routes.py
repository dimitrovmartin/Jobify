from resources.advertisement import AdvertisementListCreate, ApplyAdvertisement, AdvertisementDelete, \
    AdvertisementUpdate, AdvertisementsPerCompany, AdvertisementsPerUserPosition, ApproveAdvertisement, \
    RejectAdvertisement, AdvertisementsPerPosition, AdvertisementGet
from resources.auth import RegisterApplicant, LoginApplicant, RegisterCompany, LoginCompany

routes = (
    (RegisterApplicant, '/registerApplicant'),
    (LoginApplicant, '/loginApplicant'),
    (RegisterCompany, '/registerCompany'),
    (LoginCompany, '/loginCompany'),
    (AdvertisementListCreate, '/advertisements'),
    (AdvertisementGet, '/advertisements/<int:_id>'),
    (ApplyAdvertisement, '/advertisements/<int:_id>/apply'),
    (AdvertisementDelete, '/advertisements/<int:_id>/delete'),
    (AdvertisementUpdate, '/advertisements/<int:_id>/update'),
    (AdvertisementsPerCompany, '/advertisements/<string:company_name>'),
    (AdvertisementsPerUserPosition, '/advertisements/userPosition'),
    (AdvertisementsPerPosition, '/advertisements/position/<string:position>'),
    (ApproveAdvertisement, '/advertisements/<int:ad_id>/<int:user_id>/approve'),
    (RejectAdvertisement, '/advertisements/<int:ad_id>/<int:user_id>/reject')
)
