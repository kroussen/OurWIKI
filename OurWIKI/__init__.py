from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def main_page():
        return render_template('main.html')

    @app.route('/create')
    def create_post():
        return render_template('create_post.html')

    return app
