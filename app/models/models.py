from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from typing import List
import enum

from app.models.base import Base

class StoryStatus(str, enum.Enum):
    PENDING = "pending"
    VOTING = "voting"
    COMPLETED = "completed"

class User(Base):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_host = Column(Boolean, default=False)
    
    # Relationships
    votes = relationship("Vote", back_populates="user")
    sessions = relationship("SessionUser", back_populates="user")

class Vote(Base):
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    story_id = Column(String, ForeignKey("story.id"), nullable=False)
    value = Column(String, nullable=True)  # Can be number, null, or '?'
    timestamp = Column(Integer, nullable=False)  # epoch milliseconds
    
    # Relationships
    user = relationship("User", back_populates="votes")
    story = relationship("Story", back_populates="votes")

class Story(Base):
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(StoryStatus), default=StoryStatus.PENDING)
    final_estimate = Column(Integer, nullable=True)
    session_id = Column(String, ForeignKey("session.id"), nullable=False)
    
    # Relationships
    votes = relationship("Vote", back_populates="story")
    session = relationship("Session", back_populates="stories")

class Session(Base):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at_ms = Column(Integer, nullable=False)  # epoch milliseconds
    host_id = Column(String, ForeignKey("user.id"), nullable=False)
    current_story_id = Column(String, ForeignKey("story.id"), nullable=True)
    timer_duration = Column(Integer, nullable=True)  # seconds
    timer_end_time = Column(Integer, nullable=True)  # epoch milliseconds
    are_votes_revealed = Column(Boolean, default=False)
    
    # Relationships
    users = relationship("SessionUser", back_populates="session")
    stories = relationship("Story", back_populates="session")
    host = relationship("User", foreign_keys=[host_id])

class SessionUser(Base):
    session_id = Column(String, ForeignKey("session.id"), primary_key=True)
    user_id = Column(String, ForeignKey("user.id"), primary_key=True)
    
    # Relationships
    session = relationship("Session", back_populates="users")
    user = relationship("User", back_populates="sessions") 