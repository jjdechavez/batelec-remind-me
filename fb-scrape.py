from facebook_scraper import get_posts
import json
import requests

print("Starting FB scrape...")


file = open('batelec.json')
data = json.load(file)

posts = []

for post in data:
    posts.append(post)


r = requests.post('http://localhost:3000/posts',
                  data={'posts': json.dumps(posts)})
print(r.json())

# for post in get_posts('nintendo', page=1):
#     posts.append(post)


print("Done FB scrape")
