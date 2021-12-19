from sqlalchemy.orm import relationship

from db import db


class SkillModel(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(255), nullable=False)
    users = relationship("ApplicantUserModel", secondary="users_skills")
    advertisements = relationship("AdvertisementModel", secondary="advertisements_skills")
