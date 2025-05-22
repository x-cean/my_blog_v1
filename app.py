from flask import Flask, render_template, request
import json

app = Flask(__name__)


def get_blog_posts():
    try:
        with open("database/blog_posts.JSON", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("database/blog_posts.JSON", "w") as f:
            json.dump([], f)
            return []

@app.route('/')
def index():
    blog_posts = get_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # We will fill this in the next step
        pass
    return render_template('add.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)