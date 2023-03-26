from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from markupsafe import escape
import cloudinary
import cloudinary.uploader
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

MONGO_CLIENT = os.getenv('MONGO_CLIENT')
MONGO_DB = os.getenv('MONGO_DB')

CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')


class SchedulerConfig:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object(SchedulerConfig())

mongo_client = MongoClient(MONGO_CLIENT)
db = mongo_client[MONGO_DB]
post_collection = db['posts']
job_collection = db['jobs']

cloudinary_config = cloudinary.config(secure=True)
scheduler = APScheduler()

scheduler.init_app(app)
scheduler.start()


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


def head_image(images=None):
    if images is None:
        return None

    if len(images) == 0:
        return None

    return images[0]


def upload_image(image=None):
    if image is None:
        return None

    upload_result = cloudinary.uploader.upload(
        image,
        folder='batelec',
        unique_filename=False,
        overwrite=True
    )
    print('Upload result: ', upload_result)
    public_id = upload_result['public_id']
    srcURL = cloudinary.CloudinaryImage(public_id).build_url()
    return srcURL


def upload_image_list(images=None):
    if images is None:
        return []

    if len(images) == 0:
        return []

    list = []
    for image in images:
        upload_result = upload_image(image)
        list.append(upload_result)

    return list


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

        image = head_image(uploaded_image_list)
        image_lowquality = head_image(uploaded_image_lowquality_list)

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


@scheduler.task('cron', id='scrape_batelec_1_fb', minute='*')
def scrape_fb_batelec():
    print('Starting to scrape on batelec 1 facebook...')
    job_id = job_collection.insert_one({
        'type': "SCRAPE_FB_BATELEC_1",
        'starts_at': datetime.today().replace(microsecond=0),
        'status': 'PROCESSING',
        'message': 'Currently working on it'
    }).inserted_id

    print(job_id)
    print("Processing job DONE")

    job_collection.update_one({'_id': job_id}, {'$set': {
        'ends_at': datetime.today().replace(microsecond=0),
        'status': 'DONE',
        'message': 'Job has been processed'
    }})


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
