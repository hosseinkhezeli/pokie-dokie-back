from .. import db
from datetime import datetime, timezone

session_users = db.Table('session_users',
                         db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id'),primary_key=True))


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc),
                           nullable=False)
    status = db.Column(db.String(50), default='waiting', nullable=False)
    votes_visible = db.Column(db.Boolean, default=False, nullable=False)
    users = db.relationship('User', secondary=session_users, backref=db.backref('sessions', lazy='dynamic'))
    # current_story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=True)
    # current_story = db.relationship('Story', uselist=False)

    def __repr__(self):
        return f'<Session {self.name} (Active: {self.active})>'
