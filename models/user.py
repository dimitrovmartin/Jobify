from db import db
from models.enums import RoleType, Positions


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class ApplicantUserModel(BaseUserModel):
    __tablename__ = 'applicant_users'

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleType),
                     default=RoleType.applicant,
                     nullable=False)
    position = db.Column(db.Enum(Positions),
                         default=Positions.unemployed,
                         nullable=True)
    education = db.Column(db.String(255), nullable=False)
    photo_url = db.Column(db.String, nullable=False)
    advertisements = db.relationship("AdvertisementModel", secondary="applied_advertisements",
                                     back_populates='appliers', cascade="all, delete-orphan")


class CompanyUserModel(BaseUserModel):
    __tablename__ = 'company_users'

    company_name = db.Column(db.String(255), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    employees_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleType),
                     default=RoleType.company,
                     nullable=False)
    advertisements = db.relationship("AdvertisementModel", back_populates='company', lazy='dynamic')


class AdminUserModel(BaseUserModel):
    __tablename__ = 'admin_users'

    role = db.Column(db.Enum(RoleType),
                     default=RoleType.admin,
                     nullable=False)
