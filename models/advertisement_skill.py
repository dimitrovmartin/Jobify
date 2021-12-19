from sqlalchemy.orm import backref, relationship

from db import db
from models import SkillModel, AdvertisementModel


class AdvertisementSkillModel(db.Model):
    __tablename__ = 'advertisements_skills'

    advertisement_id = db.Column(db.Integer, db.ForeignKey('advertisements.id'), primary_key=True, nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True, nullable=False)

    advertisement = relationship(AdvertisementModel, backref=backref("advertisements_skills", cascade="all, delete-orphan"))
    skill = relationship(SkillModel, backref=backref("advertisements_skills", cascade="all, delete-orphan"))
