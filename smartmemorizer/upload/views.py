import json
from smartmemorizer.word.models import Word

__author__ = 'jackyun'
from flask import Blueprint, render_template, session, request
from flask_login import login_required
from smartmemorizer.extensions import login_manager
from smartmemorizer.user.models import User

blueprint = Blueprint('upload', __name__, url_prefix='/uploads', static_folder='../static')


@blueprint.route('/')
@login_required
def upload():
    """List members."""
    return render_template('uploads/main.html')

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


# TODO : login requried
@blueprint.route('/word', methods=['GET', 'POST'])
def upload2Db():
    user = load_user(session['user_id'])
    if request.method == 'POST':
        words = json.loads(request.form['words'])
        for word in words:
            print word
            Word.create(group=word['group'], word=word['word'], mean=word['mean'], username=user.username)
    return 'success'


