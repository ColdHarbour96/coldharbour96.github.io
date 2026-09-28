from flask import abort, Flask, render_template
import markdown
import os

app = Flask(__name__)

def load_post(slug):
    path = f"posts/{slug}.md"
    if not os.path.exists(path):
        abort(404)
    with open(path, encoding="utf-8") as f:
        text = f.read()
        md = markdown.Markdown(extensions=["meta"])
        html = md.convert(text)
    return {"slug": slug, "title": md.Meta["title"][0], "date": md.Meta["date"][0], "html": html}

@app.route("/")
def index():
    names = [name.removesuffix(".md") for name in os.listdir("posts") if name.endswith(".md")]
    posts = [load_post(post) for post in names]
    posts = sorted(posts, key=lambda p: p["date"], reverse=True)
    return render_template("index.html", posts=posts) 

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/posts/<slug>/")
def post(slug):
    return render_template("post.html", post=load_post(slug))