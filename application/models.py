from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """Model for user accounts."""

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True)
    username = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False)
    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False)
    password = db.Column(
        db.String(128),
        index=False,
        unique=False,
        nullable=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
