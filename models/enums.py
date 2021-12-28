import enum


class RoleType(enum.Enum):
    applicant = "applicant"
    company = "company"
    admin = "admin"


class Status(enum.Enum):
    sent = "sent"
    approved = "approved"
    rejected = "rejected"


class Positions(enum.Enum):
    software_developer = "Software Developer"
    hr = "Human Resources"
    manager = "Manager"
    qa = "Quality Assurance"
    marketing_expert = "Marketing Expert"
    analyst = "IT Analyst"
    system_administrator = "System Administrator"
    devops = "DevOps"
    unemployed = "Unemployed"
    unknown = "Unknown"
