from facebook_scraper import get_posts
import json
import requests


def get_posts():
    file = open('batelec.json')
    data = json.load(file)
    return data


def send_posts(posts):
    result = requests.post('http://localhost:3000/posts',
                           data={'posts': json.dumps(posts)})
    # with fbscrape
    # for post in get_posts('nintendo', page=1):
    #     posts.append(post)
    # for post in posts:
    #     print(post)


def main():
    # print("Starting FB scrape...")

    posts = get_posts()
    send_posts(posts)

    # print("Done FB scrape")


main()
