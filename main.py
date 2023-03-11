from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from markupsafe import escape
import cloudinary
# from cloudinary.uploader import upload
# from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os
import json

load_dotenv()

MONGO_CLIENT = os.getenv('MONGO_CLIENT')
MONGO_DB = os.getenv('MONGO_DB')

CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')


app = Flask(__name__)
app.config['DEBUG'] = True

mongo_client = MongoClient(MONGO_CLIENT)
db = mongo_client[MONGO_DB]
post_collection = db['posts']

cloudinary_config = cloudinary.config(secure=True)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.get('/posts')
def get_posts():
    file = open('batelec.json')
    posts = json.load(file)
    # with fbscrape
    # for post in get_posts('nintendo', page=1):
    #     posts.append(post)

    return jsonify(posts)


def post_existed(post_id):
    exist_post = post_collection.count_documents({'post_id': post_id})
    return bool(exist_post)


def get_post_image(images=None):
    if images is None:
        return None

    if len(images) == 0:
        return None

    return images[0]


def upload_image_list(images=None):
    if images is None:
        return []

    if len(images) == 0:
        return []

    return images


@app.post('/posts')
def create_posts():
    file = open('batelec.json')
    posts = json.load(file)

    for post in posts:
        post_id = post['post_id']

        if post_existed(post_id) is True:
            continue

        image_list = post['images']
        image_lowquality_list = post['images_lowquality']

        uploaded_image_list = upload_image_list(image_list)
        uploaded_image_lowquality_list = upload_image_list(
            image_lowquality_list)

        image = get_post_image(uploaded_image_list)
        image_lowquality = get_post_image(uploaded_image_lowquality_list)

        document = {
            "post_id": post_id,
            "page_id": post['page_id'],
            "post_url": post['post_url'],
            "text": post['text'],
            "post_text": post['post_text'],
            "time": post['time'],
            "timestamp": post['timestamp'],
            "image": image,
            "images": uploaded_image_list,
            "images_description": post['images_description'],
            "image_lowquality": image_lowquality,
            "images_lowquality": uploaded_image_lowquality_list,
            "images_lowquality_description":
                post['images_lowquality_description'],
        }

        post_collection.insert_one(document)

    return jsonify({'status': 'OK', 'message': 'Done inserting data'})


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/collections')
def collections():
    collection_names = db.list_collection_names()
    return jsonify({'collections': collection_names})


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
