from flask import Flask, render_template
import requests
from os import getenv

app = Flask(__name__)

GITHUB_API_TOKEN = getenv("GITHUB_API_TOKEN")
GITHUB_USERNAME  = getenv("GITHUB_USERNAME")

@app.route("/")
def index():
    stats = get_gh_stats()
    repos = get_repo_info()
    return render_template("index.html", {'repos': repos, 'stats': stats})
