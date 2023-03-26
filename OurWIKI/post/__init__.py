from flask import Blueprint
from flask import render_template, request, redirect, url_for, g

from OurWIKI.database import get_database

post_blueprint = Blueprint('post',
                           __name__,
                           url_prefix='/',
                           template_folder='templates')


@post_blueprint.route('/')
def main():
    database = get_database()
    posts = database.execute(
        'SELECT * FROM post ORDER BY created'
    ).fetchall()
    return render_template('post/main.html', posts=posts)


@post_blueprint.route('/create', methods=('GET', 'POST'))
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required'

        if error is None:
            database = get_database()
            database.execute(
                "INSERT INTO post (title, description, author_id) VALUES (?, ?, ?)",
                (title, description, g.user['id'])
            )
            database.commit()
            return redirect(url_for('post.main'))

    return render_template('post/create_post.html')
