from sqlalchemy import Column, String, ForeignKey, JSON, Integer, Text
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

    members = relationship("UserOrganization", back_populates="organization")
    projects = relationship("Project", back_populates="organization")

class UserOrganization(Base):
  __tablename__ = "user_organizations"

  user_id = Column(String, ForeignKey("users.id"), primary_key=True)
  organization_id = Column(String, ForeignKey("organizations.id"), primary_key=True)
  role = Column(String, default="member")
  
  user = relationship("User", back_populates="organizations")
  organization = relationship("Organization", back_populates="members")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    organization_id = Column(
        String,
        ForeignKey("organizations.id"),
        nullable=False,
    )
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  

    organization = relationship("Organization", back_populates="projects")
    data_sources = relationship("DataSource", back_populates="project")
    files = relationship("File", back_populates="project")

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)

    type = Column(String, nullable=False)

    config = Column(JSON, nullable=True)

    project = relationship("Project", back_populates="data_sources")

class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(String, primary_key=True)
    data_source_id = Column(
        String,
        ForeignKey("data_sources.id"),
        nullable=False,
    )

    payload = Column(JSON, nullable=False)
    status = Column(String, default="received")
    # received | processed | failed

    data_source = relationship("DataSource")

class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True)
    project_id = Column(
        String,
        ForeignKey("projects.id"),
        nullable=False,
    )

    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size = Column(Integer)

    status = Column(String, default="uploaded")
    # uploaded | processing | processed | failed

    storage_path = Column(String, nullable=True)

    project = relationship("Project", back_populates="files")

class FileChunk(Base):
    __tablename__ = "file_chunks"

    id = Column(String, primary_key=True)
    file_id = Column(
        String,
        ForeignKey("files.id"),
        nullable=False,
    )

    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

    file = relationship("File")