# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, session, request
from flask_login import login_required, current_user
from smartmemorizer.extensions import login_manager, db
from smartmemorizer.user.models import User
from smartmemorizer.word.models import Word
from sqlalchemy import func
import json


blueprint = Blueprint('word', __name__, url_prefix='/word', static_folder='../static')


@blueprint.route('/')
@login_required
def main():
    groups_list = list()
    if current_user.is_authenticated:
        groups = db.session.query(Word.group, func.count(Word.word).label('word_count')).group_by(Word.group).filter(Word.username == load_user(current_user.get_id()).username).distinct()
        for group in groups:
            groups_list.append(dict(zip(['group', 'word_count'], group)))

    return render_template('word/main.html', word_books=groups_list)


def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/<group>')
@login_required
def wordbook(group):
    words = db.session.query(Word).\
        filter(Word.username == load_user(current_user.get_id()).username).\
        filter(Word.group == group).\
        all()
    return render_template('word/wordbook.html', words=words)


@blueprint.route('/word', methods=['PUT'])
@login_required
def word():
    if request.method == 'PUT':
        words = json.loads(request.form['words'])
        for word in words:
            target_word = db.session.query(Word).filter(Word.username == load_user(current_user.get_id()).username,
                                                        Word.group == word['group'],
                                                        Word.word == word['word'],
                                                        Word.index == word['index']
                                                        ).first()
            target_word.mean = word['mean']
            target_word.error_count = word['error_count']
            print target_word.mean
            target_word.save()
    return 'SUCCESS'




