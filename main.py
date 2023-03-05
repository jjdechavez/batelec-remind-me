from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from markupsafe import escape
import json

app = Flask(__name__)
app.config['DEBUG'] = True

mongo_client = MongoClient(
    'mongodb://root:password@localhost:27017/?authSource=admin')
db = mongo_client['batelec-dev']
post_collection = db['posts']


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/posts')
def get_posts():
    file = open('batelec.json')
    posts = json.load(file)
    # with fbscrape
    # for post in get_posts('nintendo', page=1):
    #     posts.append(post)

    return jsonify(posts)


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'
