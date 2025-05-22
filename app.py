from flask import Flask, render_template, request, redirect, url_for
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


def add_blog_post(author, title, content):
    blog_posts = get_blog_posts()
    if len(blog_posts) == 0:
        post_id = 1
    else:
        post_id = max(post["id"] for post in blog_posts) + 1
    blog_posts.append({"id": post_id, "author": author, "title": title, "content": content})

    with open("database/blog_posts.JSON", "w") as f:
        json.dump(blog_posts, f)

@app.route('/')
def index():
    blog_posts = get_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post_author = request.form['author']
        post_title = request.form['title']
        post_content = request.form['content']
        add_blog_post(post_author, post_title, post_content)
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)