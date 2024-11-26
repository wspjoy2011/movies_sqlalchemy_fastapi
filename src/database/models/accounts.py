from datetime import datetime

import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from apps.accounts.validators import validate_username, validate_password_strength, validate_name, validate_email
from database.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    is_active = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    _hashed_password = Column("hashed_password", String(255))

    profile = relationship("Profile", back_populates="user", uselist=False)
    activation_token = relationship("ActivationToken", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<CustomUser(username={self.username}, email={self.email})>"

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self._hashed_password = hashed_password.decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self._hashed_password.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, username):
        validate_username(username)
        return username

    @validates("first_name", "last_name")
    def validate_name(self, key, name):
        if name:
            validate_name(name)
        return name

    @validates("password")
    def validate_password(self, key, password):
        validate_password_strength(password)
        return password

    @validates("email")
    def validate_email(self, key, email):
        validate_email(email)
        return email


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    avatar = Column(String)
    gender = Column(String(6))
    date_of_birth = Column(Date)
    info = Column(String(255))

    user = relationship("User", back_populates="profile", uselist=False)

    def __repr__(self):
        return f"<Profile(user_id={self.user_id}, gender={self.gender})>"


class ActivationToken(Base):
    __tablename__ = "activation_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    token = Column(String(32), unique=True)
    created = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="activation_token", uselist=False)

    def __repr__(self):
        return f"<ActivationToken(user_id={self.user_id}, token={self.token})>"


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<BlacklistedToken(token={self.token}, expires_at={self.expires_at})>"

    def is_expired(self):
        return datetime.now() > self.expires_at
