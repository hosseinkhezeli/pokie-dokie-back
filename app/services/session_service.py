
from .. import db
from datetime import datetime

from ..models.session_model import Session


def create_session(current_user, data):
    name = data.get('name')
    description = data.get('description', '')
    max_users = data.get('max_users')

    if not name:
        return {'error': 'Session name is required'}, 400

    session = Session(
        name=name,
        description=description,
        active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        max_users=max_users
    )
    session.users.append(current_user)  # Add creator to session

    db.session.add(session)
    db.session.commit()

    return {'id': session.id, 'name': session.name, 'active': session.active}, 201


def get_sessions_for_user(user):
    sessions = user.sessions.all()  # Assuming backref 'sessions' on User model
    return [{'id': s.id, 'name': s.name, 'active': s.active} for s in sessions]
