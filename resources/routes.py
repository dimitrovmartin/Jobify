from resources.advertisement import AdvertisementListCreate, ApplyAdvertisement, AdvertisementDelete, \
    AdvertisementUpdate
from resources.auth import RegisterApplicant, LoginApplicant, RegisterCompany, LoginCompany

routes = (
    (RegisterApplicant, '/registerApplicant'),
    (LoginApplicant, '/loginApplicant'),
    (RegisterCompany, '/registerCompany'),
    (LoginCompany, '/loginCompany'),
    (AdvertisementListCreate, '/advertisements'),
    (ApplyAdvertisement, '/advertisements/<int:_id>/apply'),
    (AdvertisementDelete, '/advertisements/<int:_id>/delete'),
    (AdvertisementUpdate, '/advertisements/<int:_id>/update')
)
