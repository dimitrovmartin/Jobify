from db import db
from models import Positions


class AdvertisementModel(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Enum(Positions), default=Positions.unknown, nullable=True)
    salary = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=False)
    company_user_id = db.Column(db.Integer, db.ForeignKey('company_users.id'))
    company = db.relationship('CompanyUserModel', cascade="all, delete-orphan")
    appliers = db.relationship('ApplicantUserModel', secondary="applied_advertisements",
                               back_populates='advertisements', cascade="all, delete-orphan")
