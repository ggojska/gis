from flask import render_template
from flask_login import login_required

from . import main


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html', mapa=True)

@main.route('/my-account', methods=['GET'])
@login_required
def my_account():
    return render_template('my_account.html')
