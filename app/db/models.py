from sqlalchemy import Column, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"

  id = Column(String, primary_key=True)
  email = Column(String, unique=True, nullable=False)
  organizations = relationship("UserOrganization", back_populates="user", lazy="selectin")

class Organization(Base):
  __tablename__ = "organizations"

  id = Column(String, primary_key=True)
  name = Column(String, nullable=False)
  members = relationship("UserOrganization", back_populates="organization", lazy="selectin")

class UserOrganization(Base):
  __tablename__ = "user_organizations"

  user_id = Column(String, ForeignKey("users.id"), primary_key=True)
  organization_id = Column(String, ForeignKey("organizations.id"), primary_key=True)
  role = Column(String, default="member")
  
  user = relationship("User", back_populates="organizations")
  organization = relationship("Organization", back_populates="members")