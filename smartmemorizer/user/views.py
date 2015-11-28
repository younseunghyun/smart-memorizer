# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, session
from flask_login import login_required
from smartmemorizer.extensions import login_manager
from smartmemorizer.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    print session
    return render_template('users/members.html')

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))
