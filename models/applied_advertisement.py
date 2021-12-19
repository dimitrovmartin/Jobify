from sqlalchemy.orm import relationship, backref

from db import db
from models import CompanyUserModel, AdvertisementModel
from models.enums import Status


class AppliedAdvertisement(db.Model):
    __tablename__ = 'applied_advertisements'

    applicant_user_id = db.Column(db.Integer, db.ForeignKey('applicant_users.id'), primary_key=True, nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('advertisements.id'), primary_key=True, nullable=False)
    status = db.Column(db.Enum(Status), default=Status.sent, nullable=False)

    applicant_user = relationship(CompanyUserModel, backref=backref("applied_advertisements", cascade="all, delete-orphan"))
    skill = relationship(AdvertisementModel, backref=backref("applied_advertisements", cascade="all, delete-orphan"))
