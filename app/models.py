from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    invitations_sent = db.relationship('Invitation',
        foreign_keys='Invitation.sender_id', backref='sender', lazy='dynamic')
    invitations_received = db.relationship('Invitation', 
        foreign_keys='Invitation.recipient_id', backref='recipient', lazy='dynamic')
    last_invitation_read_time = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def new_invitations(self):
        last_read_time = self.last_invitation_read_time or datetime(1900, 1, 1)
        return Invitation.query.filter_by(recipent=self).filter(
            Invitation.timestamp > last_read_time).count()
        

    def __repr__(self):
        return f'<User {self.username}>'

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    invitation_header = db.Column(db.String(140))
    invitation_body = db.Column(db.String(140))
    invitation_footer = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    accepted = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Invitation {self.invitation_body}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))