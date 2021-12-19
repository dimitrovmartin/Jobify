from sqlalchemy.orm import backref, relationship

from db import db
from models import CompanyUserModel, SkillModel


class SkillUserModel(db.Model):
    __tablename__ = 'skills_users'

    applicant_user_id = db.Column(db.Integer, db.ForeignKey('applicant_users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)

    applicant_user = relationship(CompanyUserModel, backref=backref("skills_users", cascade="all, delete-orphan"))
    skill = relationship(SkillModel, backref=backref("skills_users", cascade="all, delete-orphan"))
