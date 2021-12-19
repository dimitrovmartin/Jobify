from db import db


class AdvertisementModel(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=False)
    company_user_id = db.Column(db.Integer, db.ForeignKey('company_users.id'))
    company = db.relationship('CompanyUserModel')
