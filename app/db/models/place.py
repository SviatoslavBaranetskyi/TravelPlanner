from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    visited = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="places")
