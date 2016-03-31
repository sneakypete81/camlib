#!/usr/bin/env python
import os
import json
from flask import Flask, render_template, request

DEFAULT_JSON_PATH = "_json"
PAGE_LENGTH = 20

class CamlibFlask(Flask):
    def __init__(self, *args, **kwds):
        super(CamlibFlask, self).__init__(*args, **kwds)
        self.books = []
        self.genres = []

    def load_books(self, json_path):
        data = json.load(open(os.path.join(json_path, "camlib.json")))
        self.books = data["books"]
        self.books.sort(key=lambda book: book["rating"], reverse=True)
        self.genres = list({book["genre"] for book in self.books})

    def filter_books(self, filter_list):
        genre_list = [self.genres[i] for i in filter_list]
        return [book for book in self.books if book["genre"] in genre_list]

app = CamlibFlask(__name__)

@app.route("/")
def root():
    filter_list = _parse_filter_list(request)
    filtered_books = app.filter_books(filter_list)
    data = filtered_books[:PAGE_LENGTH]
    return render_template("root.html",
                           data=data,
                           genres=app.genres,
                           filter=request.args.get("filter", None),
                           filter_list=filter_list,
                           next_page=2)

@app.route("/fragment/books")
def books_fragment():
    page = int(request.args["page"])
    if page < 1:
        abort(400)

    start = (page - 1) * PAGE_LENGTH
    filtered_books = app.filter_books(_parse_filter_list(request))
    data = filtered_books[start:start + PAGE_LENGTH]
    if start + PAGE_LENGTH >= len(filtered_books):
        next_page = None
    else:
        next_page = page + 1

    return render_template("books_fragment.html",
                           data=data,
                           filter=request.args.get("filter", None),
                           next_page=next_page)

@app.route("/redirect/camlib")
def camlib_redirect():
    return render_template("camlib_redirect.html", isbn=request.args["isbn"])

def _parse_filter_list(request):
    if "filter" in request.args:
        data = request.args["filter"]
        return [int(i) for i in data.split(",") if i != ""]
    else:
        return range(len(app.genres))

def setup(json_path=None):
    if json_path is None:
        json_path = DEFAULT_JSON_PATH
    app.load_books(json_path)
    print "Loaded %d books" % len(app.books)

if __name__ == "__main__":
    setup()
    app.run(debug=True)
