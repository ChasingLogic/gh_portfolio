from flask import Flask, render_template
from os import getenv
from functools import reduce
from threading import Timer
from werkzeug.contrib.cache import RedisCache

import requests
import logging

logging.basicConfig(filename="web.log", level=logging.INFO)

app = Flask(__name__)
cache = RedisCache(host='redis', port=6379, password=None, db=0, default_timeout=300, key_prefix=None)

GITHUB_USERNAME  = getenv("GITHUB_USERNAME")
TWITTER_USERNAME = getenv("TWITTER_USERNAME")

GITHUB_API_TOKEN = getenv("GITHUB_API_TOKEN")

FULL_NAME = getenv("FULL_NAME")
JOB_TITLE = getenv("JOB_TITLE")
EMAIL = getenv("EMAIL")
RESUME_LINK = getenv("RESUME_LINK")


headers = {
        "Authorization": "token " + GITHUB_API_TOKEN,
        "User-Agent": GITHUB_USERNAME
        }

@app.route("/")
def index():
    owner = cache.get("owner")
    repos = cache.get("repos")
    if repos == None or owner == None:
        (owner, repos) = get_repo_info()
        cache.set("owner", owner)
        cache.set("repos", repos)
    return render_template("index.html", 
            repos=repos, 
            owner=owner, 
            email=EMAIL, 
            job_title=JOB_TITLE,
            resume_link=RESUME_LINK,
            full_name=FULL_NAME,
            twitter=TWITTER_USERNAME)

def update_cache():
    app.logger.info("updating cache")
    (owner, repos) = get_repo_info()
    cache.set("owner", owner)
    cache.set("repos", repos)
    app.logger.info("cache successfully updated")
    # Update every 10800 seconds or 3 hours
    Timer(10800, update_cache).start()

def get_repo_stats(repo):
    r = requests.get("https://api.github.com/repos/" + GITHUB_USERNAME + "/" + repo['name'] + "/stats/commit_activity", headers=headers)
    if r.status_code >= 300:
        app.logger.error("Error getting repo stats: ", repo.name, r.text)
        return repo

    total_commits = 0

    for stat in r.json():
        total_commits += stat['total']

    repo['total_commits'] = total_commits
    return repo

def get_repo_info():
    r = requests.get("https://api.github.com/users/" + GITHUB_USERNAME + "/repos?sort=updated", headers=headers)
    print("https://api.github.com/users/" + GITHUB_USERNAME + "/repos")
    if r.status_code >= 300:
        print("Failed to get repos: ", r.text)
        return "Failed to get repos"
    try:
        repos = r.json() 
    except:
        print("Error parsing json: ", r.text)
        return "Error parsing json"
    
    return (repos[0]['owner'], [get_repo_stats(r) for r in repos][:4])

update_cache()
