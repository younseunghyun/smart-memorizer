# -*- coding: utf-8 -*-
"""word models."""
import datetime as dt

from flask_login import UserMixin

from smartmemorizer.database import Column, Model, SurrogatePK, db, reference_col, relationship
from smartmemorizer.extensions import bcrypt

from sqlalchemy import func

class Word(SurrogatePK, Model):
    """A word of the app."""

    __tablename__ = 'words'

    username = Column(db.String(80), db.ForeignKey('users.username'), unique=False)
    group = Column(db.String(80), unique=False, nullable=False)
    word = Column(db.String(80), unique=False, nullable=False)
    mean = Column(db.String(80), unique=False, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    call_count = Column(db.Integer, nullable=True)
    error_count = Column(db.Integer, nullable=True)

    def __init__(self, username, group, word, mean):
        """Create instance."""
        if db.session.query(func.count('*')).\
                select_from(Word_book).\
                filter(Word_book.group == group,
                       Word_book.username == username).\
                distinct().scalar() == 0:
            Word_book.create(username=username, group=group, description='')

        db.Model.__init__(self, username=username, group=group, word=word, mean=mean)

    def increase_error_count(self):
        if self.error_count is None:
            self.error_count = 0
        self.error_count += 1
        self.save()

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class Word_book(SurrogatePK, Model):
    """A word book of the app"""

    __tablename__ = 'word_books'

    username = Column(db.String(80), db.ForeignKey('users.username'), unique=False)
    group = Column(db.String(80), unique=False, nullable=False)
    description = Column(db.String(200), unique=False, nullable=True)

    def __init__(self, username, group, description, **kwargs):
        db.Model.__init__(self, username=username, group=group, description=description, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Word_book({username!r, group!r})>'.format(username=self.username, group=self.group)

    def modify_description(self, description):
        self.description = description
        self.save()

