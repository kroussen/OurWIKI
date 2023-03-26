from flask import Blueprint
from flask import render_template, request, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from OurWIKI.database import get_database

auth_blueprint = Blueprint(
                            'auth',
                            __name__,
                            url_prefix='/auth',
                            template_folder='templates')


@auth_blueprint.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        database = get_database()
        error = None

        if not username:
            error = 'Username is required'
        if not password:
            error = 'Password is required'

        if error is None:
            try:
                database.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                database.commit()
            except database.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_blueprint.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        database = get_database()
        error = None
        user = database.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('post.main'))

    return render_template('auth/login.html')


@auth_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_database().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('post.main'))


@auth_blueprint.route('/profile')
def profile():
    posts = get_database().execute(
        'SELECT * FROM post WHERE author_id = (?)', (g.user['id'],)
    )
    if g.user is not None:
        return render_template('auth/profile.html', user=g.user, posts=posts)
