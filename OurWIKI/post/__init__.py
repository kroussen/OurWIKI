from flask import Blueprint
from flask import render_template

post_blueprint = Blueprint('post',
                           __name__,
                           url_prefix='/',
                           template_folder='templates')


@post_blueprint.route('/')
def main():
    return render_template('post/main.html')


@post_blueprint.route('/create')
def create_post():
    return render_template('post/create_post.html')
