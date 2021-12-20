from resources.advertisement import AdvertisementListCreate, ApplyAdvertisement, AdvertisementDelete, \
    AdvertisementUpdate, AdvertisementsPerCompany, AdvertisementsPerPreviousPosition, ApproveAdvertisement, \
    RejectAdvertisement
from resources.auth import RegisterApplicant, LoginApplicant, RegisterCompany, LoginCompany

routes = (
    (RegisterApplicant, '/registerApplicant'),
    (LoginApplicant, '/loginApplicant'),
    (RegisterCompany, '/registerCompany'),
    (LoginCompany, '/loginCompany'),
    (AdvertisementListCreate, '/advertisements'),
    (ApplyAdvertisement, '/advertisements/<int:_id>/apply'),
    (AdvertisementDelete, '/advertisements/<int:_id>/delete'),
    (AdvertisementUpdate, '/advertisements/<int:_id>/update'),
    (AdvertisementsPerCompany, '/advertisements/<string:company_name>'),
    (AdvertisementsPerPreviousPosition, '/advertisements/position'),
    (ApproveAdvertisement, '/advertisements/<int:ad_id>/<int:user_id>/approve'),
    (RejectAdvertisement, '/advertisements/<int:ad_id>/<int:user_id>/reject')
)
