from sqlalchemy.orm import backref, relationship

from db import db
from models import CompanyUserModel, SkillModel


class UserSkillModel(db.Model):
    __tablename__ = 'users_skills'

    applicant_user_id = db.Column(db.Integer, db.ForeignKey('applicant_users.id'), primary_key=True, nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True, nullable=False)

    applicant_user = relationship(CompanyUserModel, backref=backref("users_skills", cascade="all, delete-orphan"))
    skill = relationship(SkillModel, backref=backref("users_skills", cascade="all, delete-orphan"))
