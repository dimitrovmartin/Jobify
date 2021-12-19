import enum


class RoleType(enum.Enum):
    applicant = 'applicant'
    company = 'company'
    admin = 'admin'


class Status(enum.Enum):
    sent = 'sent'
    approved = 'approved'
    rejected = 'rejected'
