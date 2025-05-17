from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
import time
from statistics import median

from app.db.session import get_db
from app.models.models import User, Session, Story, Vote, SessionUser
from app.schemas.schemas import (
    UserCreate, User, SessionCreate, Session, StoryCreate, Story,
    VoteCreate, Vote, Token
)
from app.core.security import create_access_token, verify_token
from app.core.websocket import manager, WebSocketMessage

api_router = APIRouter()

# Authentication endpoints
@api_router.post("/auth/token", response_model=Token)
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Create or get user
    result = await db.execute(
        select(User).where(User.name == user_data.name)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            id=str(uuid.uuid4()),
            name=user_data.name,
            is_active=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

# Session endpoints
@api_router.post("/sessions", response_model=Session)
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token)
):
    session = Session(
        id=str(uuid.uuid4()),
        name=session_data.name,
        created_at_ms=int(time.time() * 1000),
        host_id=current_user_id,
        timer_duration=session_data.timer_duration
    )
    db.add(session)
    
    # Add host as first user
    session_user = SessionUser(
        session_id=session.id,
        user_id=current_user_id
    )
    db.add(session_user)
    
    await db.commit()
    await db.refresh(session)
    return session

@api_router.get("/sessions/{session_id}", response_model=Session)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token)
):
    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

# Story endpoints
@api_router.post("/sessions/{session_id}/stories", response_model=Story)
async def create_story(
    session_id: str,
    story_data: StoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token)
):
    # Verify session exists and user is host
    session = await db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.host_id != current_user_id:
        raise HTTPException(status_code=403, detail="Only host can create stories")
    
    story = Story(
        id=str(uuid.uuid4()),
        title=story_data.title,
        description=story_data.description,
        session_id=session_id
    )
    db.add(story)
    await db.commit()
    await db.refresh(story)
    
    # Notify all users
    await manager.broadcast_to_session(
        session_id,
        WebSocketMessage(type="story_created", data=story.dict())
    )
    
    return story

@api_router.post("/sessions/{session_id}/stories/{story_id}/start-voting")
async def start_voting(
    session_id: str,
    story_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token)
):
    session = await db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.host_id != current_user_id:
        raise HTTPException(status_code=403, detail="Only host can start voting")
    
    story = await db.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    story.status = "voting"
    session.current_story_id = story_id
    session.are_votes_revealed = False
    
    if session.timer_duration:
        session.timer_end_time = int(time.time() * 1000) + (session.timer_duration * 1000)
    
    await db.commit()
    
    # Notify all users
    await manager.broadcast_to_session(
        session_id,
        WebSocketMessage(type="voting_started", data={"story_id": story_id})
    )
    
    return {"status": "success"}

@api_router.post("/sessions/{session_id}/stories/{story_id}/reveal-votes")
async def reveal_votes(
    session_id: str,
    story_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token)
):
    session = await db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.host_id != current_user_id:
        raise HTTPException(status_code=403, detail="Only host can reveal votes")
    
    story = await db.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Get all votes for the story
    result = await db.execute(
        select(Vote).where(Vote.story_id == story_id)
    )
    votes = result.scalars().all()
    
    # Calculate final estimate (median of numeric votes)
    numeric_votes = [int(v.value) for v in votes if v.value and v.value.isdigit()]
    if numeric_votes:
        story.final_estimate = int(median(numeric_votes))
    
    story.status = "completed"
    session.are_votes_revealed = True
    session.current_story_id = None
    session.timer_end_time = None
    
    await db.commit()
    
    # Notify all users
    await manager.broadcast_to_session(
        session_id,
        WebSocketMessage(
            type="votes_revealed",
            data={
                "story_id": story_id,
                "votes": [v.dict() for v in votes],
                "final_estimate": story.final_estimate
            }
        )
    )
    
    return {"status": "success"}

# Vote endpoints
@api_router.post("/sessions/{session_id}/stories/{story_id}/vote", response_model=Vote)
async def submit_vote(
    session_id: str,
    story_id: str,
    vote_data: VoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(verify_token)
):
    # Verify session and story exist
    session = await db.get(Session, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    story = await db.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    if story.status != "voting":
        raise HTTPException(status_code=400, detail="Story is not in voting state")
    
    # Create or update vote
    result = await db.execute(
        select(Vote).where(
            Vote.story_id == story_id,
            Vote.user_id == current_user_id
        )
    )
    existing_vote = result.scalar_one_or_none()
    
    if existing_vote:
        existing_vote.value = vote_data.value
        existing_vote.timestamp = int(time.time() * 1000)
        vote = existing_vote
    else:
        vote = Vote(
            id=str(uuid.uuid4()),
            user_id=current_user_id,
            story_id=story_id,
            value=vote_data.value,
            timestamp=int(time.time() * 1000)
        )
        db.add(vote)
    
    await db.commit()
    await db.refresh(vote)
    
    # Notify all users about the new vote
    await manager.broadcast_to_session(
        session_id,
        WebSocketMessage(
            type="vote_submitted",
            data={
                "story_id": story_id,
                "user_id": current_user_id,
                "has_voted": True
            }
        )
    )
    
    return vote 