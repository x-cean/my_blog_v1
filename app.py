from flask import Flask
from flask import render_template
import json

app = Flask(__name__)


def get_blog_posts():
    try:
        with open("blog_posts.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("blog_posts.json", "w") as f:
            json.dump([], f)
            return []

@app.route('/')
def index():
    blog_posts = get_blog_posts()
    return render_template("index.html", posts=blog_posts)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)