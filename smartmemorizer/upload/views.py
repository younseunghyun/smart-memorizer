import json
from smartmemorizer.word.models import Word

__author__ = 'jackyun'
from flask import Blueprint, render_template, session, request
from flask_login import login_required
from flask.ext import excel
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


ALLOWED_EXTENSIONS = set(['csv','txt'])

import StringIO

@login_required
@blueprint.route('/word', methods=['GET', 'POST'])
def upload2Db():
    user = load_user(session['user_id'])
    if request.method == 'POST':
        if request.files.has_key('file'):
            file = request.files['file']
            if file and isAllowedExtentin(file.filename):
                try:
                    words = convertFile2WordList(file)
                except ValueError:
                    return 'Fail'
        else:
            print 'hi'
            words = json.loads(request.form['words'])
        for word in words:
            print word
            Word.create(group=word['group'], word=word['word'], mean=word['mean'], username=user.username)
    return 'Success'


def isAllowedExtentin(filename):
    return filename.split('.')[-1] in ALLOWED_EXTENSIONS

def convertFile2WordList(file):
    file_type = file.content_type.split('/')[-1]
    separator_map = {
        'csv' : ',',
        'tsv' : '\t',
    }
    words = []
    for wordline in file.stream.read().decode('utf8').split('\n'):
        try:
            word_candidate = wordline.split(separator_map[file_type])
            words.append({
                'group' : file.filename.split('.')[0],
                'word' : word_candidate[0],
                'mean' : word_candidate[1]
            })
        except:
            raise ValueError
    return words

