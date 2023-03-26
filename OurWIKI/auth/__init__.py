from flask import Blueprint
from flask import render_template

auth_blueprint = Blueprint(
                            'auth',
                            __name__,
                            url_prefix='/auth',
                            template_folder='templates')


@auth_blueprint.route('/register')
def register():
    return render_template('auth/register.html')


@auth_blueprint.route('/login')
def login():
    return render_template('auth/login.html')
