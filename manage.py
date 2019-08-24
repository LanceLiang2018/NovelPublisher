import os
from flask import *
from database import DataBase
import markdown
import requests

app = Flask(__name__)
db = DataBase()


def make_line(md: str, text: str):
    md += text + '\n'
    return md


@app.route('/')
def index():
    books = db.get_books()
    print(books)
    md = '# My Novels Publisher\n'
    for book in books:
        md = make_line(md, '- [%s](/%s)\n' % (book['bookname'], book['bookname']))
    html = markdown.markdown(md)
    return html


@app.route('/<string:bookname>')
def get_chapters(bookname: str):
    md = '# %s\n' % bookname
    chapters = db.get_chapters(bookname)
    for chapter in chapters:
        md = make_line(md, '- [%s](/%s/%s)' % (chapter['chaptername'],
                                               chapter['bookname'], chapter['chaptername']))
    return markdown.markdown(md)

@app.route('/<string:bookname>/<string:chaptername>')
def get_content(bookname, chaptername):
    md = '# %s\n## %s\n' % (bookname, chaptername)
    content = db.get_content(bookname, chaptername)
    if content is None:
        return markdown.markdown(md)
    try:
        raw = requests.get(content).text
        md = markdown.markdown(raw)
        return md
    except Exception as e:
        return str(e)

@app.route('/debug_clear_all')
def clear_all():
    db.db_init()
    return 'OK'


if __name__ == '__main__':
    app.run("0.0.0.0", port=int(os.environ.get('PORT', '5000')), debug=False)