# Batelec Remind Me

Facebook page web scrape daily.

I'll move this project to Flask python to utilize the fb webscrape.

## Create virtual environment for project

`python3 -m venv remind-me-batelec` command

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
- [X] Store scrape on mongodb
- [X] Store Image on Cloud Storage
    - FB images uses token when token expired image is not accessable
    - Can use image_description field (but not every image_description has information about the image)
    - Store on specific own folder like "batlec"
- [] Add CRON jobs to scrape daily (Need to research about it: (Flask-APScheduler)[https://viniciuschiele.github.io/flask-apscheduler])
- [] List scrape post collections on specific endpoint

## ISSUE
- facebook_scrapper.get_posts() not working
