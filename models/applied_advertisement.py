from db import db
from models.enums import Status


class AppliedAdvertisementModel(db.Model):
    __tablename__ = "applied_advertisements"

    applicant_user_id = db.Column(
        db.Integer,
        db.ForeignKey("applicant_users.id"),
        primary_key=True,
        nullable=False,
    )
    advertisement_id = db.Column(
        db.Integer, db.ForeignKey("advertisements.id"), primary_key=True, nullable=False
    )
    status = db.Column(db.Enum(Status), default=Status.sent, nullable=False)
