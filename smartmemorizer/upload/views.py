import json
from smartmemorizer.word.models import Word

__author__ = 'jackyun'
from flask import Blueprint, render_template, session, request
from flask_login import login_required
from smartmemorizer.extensions import login_manager
from smartmemorizer.user.models import User
import requests as r
from bs4 import BeautifulSoup as bs

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


@login_required
@blueprint.route('/word', methods=['GET', 'POST'])
def upload2Db():
    user = load_user(session['user_id'])
    if request.method == 'POST':
        if request.files.has_key('file'):
            file = request.files['file']
            if file and isAllowedExtention(file.filename):
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


def isAllowedExtention(filename):
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


@login_required
@blueprint.route('/mean/<word>')
def getMean(word):
    try:
        daum_dict_bs = bs(r.get('http://dic.daum.net/search.do?q={}'.format(word)).text, 'html.parser')
        means =[mean.text for mean in  daum_dict_bs.select('.clean_word')[0].select('.list_mean') ]
        means = clean_word(means[0])
        return means
    except:
        return 'unknown'


def clean_word(target_word):
    clean_word_list=['\n']
    for word in clean_word_list:
        target_word = target_word.replace(word,' ')
    return target_word