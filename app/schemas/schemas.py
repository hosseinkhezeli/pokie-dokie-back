from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime
from app.models.models import StoryStatus

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    is_active: bool
    is_host: Optional[bool] = False

    class Config:
        from_attributes = True

class VoteBase(BaseModel):
    value: Optional[Union[int, str]] = None

class VoteCreate(VoteBase):
    story_id: str

class Vote(VoteBase):
    id: str
    user_id: str
    story_id: str
    timestamp: int

    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    title: str
    description: Optional[str] = None

class StoryCreate(StoryBase):
    pass

class Story(StoryBase):
    id: str
    status: StoryStatus
    final_estimate: Optional[int] = None
    session_id: str
    votes: List[Vote] = []

    class Config:
        from_attributes = True

class SessionBase(BaseModel):
    name: str
    timer_duration: Optional[int] = None

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: str
    created_at_ms: int
    host_id: str
    current_story_id: Optional[str] = None
    timer_end_time: Optional[int] = None
    are_votes_revealed: bool
    users: List[User] = []
    stories: List[Story] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class WebSocketMessage(BaseModel):
    type: str
    data: dict 