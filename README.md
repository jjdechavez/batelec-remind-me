# Batelec Remind Me

Facebook page web scrape daily.

I'll move this project to Flask python to utilize the fb webscrape.

## Activate venv

Virtual environment to manage dependencies of the project with `. venv/bin/activate` command

## Install dependencies

`python3 -m pip install -r requirements.txt` command

## Run development

Run `flask --app main run` command, to start the server
Debug mode `flask --app main run --debug` command

## TODOS
- [X] Setup Flask as server
- [X] Install facebook_scrapper
- [X] Implement Mongodb as database
- [] Store scrape on mongodb
- [] Store Image on Cloud Storage
    - FB images uses token when token expired image is not accessable
    - Can use image_description field (but not every image_description has information about the image)
