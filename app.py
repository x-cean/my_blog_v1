from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def get_blog_posts():
    """
    get the posts from the JSON file
    """
    try:
        with open("database/blog_posts.JSON", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("database/blog_posts.JSON", "w") as f:
            json.dump([], f)
            return []


def add_blog_post(author, title, content):
    """
    add a new blog to the JSON file
    """
    blog_posts = get_blog_posts()
    # if empty, the first post id is 1
    if len(blog_posts) == 0:
        post_id = 1
    else:
        # get the id of the latest post and increment it by 1
        post_id = max(post["id"] for post in blog_posts) + 1
    blog_posts.append({"id": post_id, "author": author, "title": title, "content": content})
    # write the updated blog posts to the JSON file
    with open("database/blog_posts.JSON", "w") as f:
        json.dump(blog_posts, f)


def delete_blog_post(post_id):
    """
    delete a blog from the JSON file based on post id
    return None if successful, else return an error message
    """
    blog_posts = get_blog_posts()
    # check if the post id exists in the blog posts
    if post_id not in [post["id"] for post in blog_posts]:
        return "Post not found"
    else:
        for post in blog_posts:
            if post["id"] == post_id:
                # delete the post from the blog posts
                blog_posts.remove(post)
                break
        with open("database/blog_posts.JSON", "w") as f:
            json.dump(blog_posts, f)
        return None


def fetch_post_by_id(post_id):
    """
    find a post in the JSON file based on post id
    return the post if found, else return None
    """
    blog_posts = get_blog_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None

@app.route('/')
def index():
    """
    go to home page, display all blog posts
    """
    blog_posts = get_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    add a new blog post to JSON and display the home page
    """
    # get info from the form via request.form if it's a POST request
    if request.method == 'POST':
        post_author = request.form.get('author')
        post_title = request.form.get('title')
        post_content = request.form.get('content')
        add_blog_post(post_author, post_title, post_content)
        return redirect(url_for('index'))
    # if it's a GET request, display the add.html page
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    delete a blog post from JSON and display the home page
    """
    # Delete the post from the JSON file if post id exists
    delete_post = delete_blog_post(post_id)
    if delete_post is not None:
        return delete_post, 404
    else:
        return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    update a blog post in JSON and display the home page
    """
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    # Get all post from the JSON file
    posts = get_blog_posts()

    # Post not found
    if post is None:
        return "Post not found", 404

    # POST request
    if request.method == 'POST':
        # Update the post in the JSON file
        for post in posts:
            if post["id"] == post_id:
                post["author"] = request.form.get("author")
                post["title"] = request.form.get("title")
                post["content"] = request.form.get("content")
        with open("database/blog_posts.JSON", "w") as f:
            json.dump(posts, f)
        # Redirect back to index
        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)