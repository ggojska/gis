from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .. import db
from ..models import Car


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html', mapa=True)

@main.route('/my-account', methods=['GET'])
@login_required
def my_account():
    return render_template('my_account.html')
