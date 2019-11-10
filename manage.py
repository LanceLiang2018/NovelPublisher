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
    md = '# My Novels Publisher\n'
    for book in books:
        if type(book) is dict:
            bookname = book['bookname']
        else:
            bookname = book
        md = make_line(md, '- [%s](/%s)\n' % (bookname, bookname))
    md = make_line(md, '[更新章节](/publish)')
    html = markdown.markdown(md)
    # return html
    return render_template("reader.html", contain=html)


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'GET':
        books = db.get_books()
        chapters = db.get_chapters()
        return render_template('publish.html', booknames=books, chapternames=chapters)
    form = dict(request.form)
    args = ['password', 'bookname', 'bookname_new', 'chaptername', 'chaptername_new', 'url']
    for a in args:
        if a not in form:
            return 'Args Error.'
    if form['password'][0] != '1352040930':
        return 'Your Password %s Error.' % form['password'][0]
    if form['bookname'][0] == '':
        bookname = form['bookname_new'][0]
    else:
        bookname = form['bookname'][0]
    if form['chaptername'][0] == '':
        chaptername = form['chaptername_new'][0]
    else:
        chaptername = form['chaptername'][0]
    try:
        url = form['url'][0]
        text = requests.get(url).text
        md = markdown.markdown(text)
    except Exception as e:
        return 'Error: ' + str(e)

    db.publish(bookname, chaptername, url)
    return redirect('/%s/%s' % (bookname, chaptername))


@app.route('/<string:bookname>')
def get_chapters(bookname: str):
    path = "[%s](%s)>%s\n" % ("首页", "/", bookname)
    title = "%s - MyNovelPublisher" % (bookname, )
    md = path + '# %s\n' % bookname
    chapters = db.get_chapters(bookname)
    for chapter in chapters:
        md = make_line(md, '- [%s](/%s/%s)' % (chapter['chaptername'],
                                               chapter['bookname'], chapter['chaptername']))
    md = markdown.markdown(md)
    return render_template("reader.html", contain=md, title=title)


@app.route('/<string:bookname>/<string:chaptername>')
def get_content(bookname, chaptername):
    path = "[%s](%s)>[%s](%s)>%s\n" % ("首页", "/", bookname, "/%s" % bookname, chaptername)
    md = path + '# %s\n## %s\n' % (bookname, chaptername)
    title = "%s/%s - MyNovelPublisher" % (bookname, chaptername)
    content = db.get_content(bookname, chaptername)
    if content is None:
        return markdown.markdown(md)
    try:
        raw = requests.get(content).text
        md = markdown.markdown(raw)
        path = markdown.markdown(path)
        # return md
        comments = 'https://lance-chatroom.herokuapp.com/frame/%s_%s' % (bookname, chaptername)
        return render_template("reader_frame.html", contain=md, frame_src=comments, guidance=path, title=title)
    except Exception as e:
        return str(e)


@app.route('/debug_clear_all')
def clear_all():
    db.db_init()
    return 'OK'


if __name__ == '__main__':
    app.run("0.0.0.0", port=int(os.environ.get('PORT', '5000')), debug=False)