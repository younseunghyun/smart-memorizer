import json
from smartmemorizer.word.models import Word

__author__ = 'jackyun'
from flask import Blueprint, render_template, session, request
from flask_login import login_required, current_user
from smartmemorizer.extensions import login_manager, db
from smartmemorizer.user.models import User
from smartmemorizer.word.models import Word
from sqlalchemy import func


blueprint = Blueprint('memorizer', __name__, url_prefix='/memorizer', static_folder='../static')


@blueprint.route('/')
def main():
    """List members."""
    groups_list = list()
    if current_user.is_authenticated:
        groups = db.session.query(Word.group, func.count(Word.word).label('word_count')).group_by(Word.group).filter(Word.username == load_user(current_user.get_id()).username).distinct()
        for group in groups:
            groups_list.append(dict(zip(['group', 'word_count'], group)))

    return render_template('memorizer/main.html', word_books=groups_list)


@blueprint.route('/<group>')
@login_required
def memorize(group):
    words = db.session.query(Word).\
        filter(Word.username == load_user(current_user.get_id()).username).\
        filter(Word.group == group).\
        all()
    return render_template('memorizer/memorizer.html', words=words)


@login_required
@blueprint.route('/word', methods=['GET','POST'])
def word():
    if request.method == 'POST':
        username = load_user(current_user.get_id()).username
        group = request.form['group']
        word = request.form['word']
        items = db.session.query(Word).filter(Word.username == username, Word.group == group, Word.word == word).all()
        for item in items:
            item.increase_error_count()
    return "Success"


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))

