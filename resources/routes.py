from resources.advertisement import Advertisement
from resources.auth import RegisterApplicant, LoginApplicant, RegisterCompany, LoginCompany

routes = (
    (RegisterApplicant, '/registerApplicant'),
    (LoginApplicant, '/loginApplicant'),
    (RegisterCompany, '/registerCompany'),
    (LoginCompany, '/loginCompany'),
    (Advertisement, '/advertisements')
)
