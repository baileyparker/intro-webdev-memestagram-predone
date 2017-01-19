#!/usr/bin/env python3

import os

from flask import Flask, render_template, redirect, url_for, request, send_file
from db import setup_db, get_db
from io import BytesIO
from memer import make_meme


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = bool(os.environ.get('FLASK_DEBUG', 1))
setup_db(app)

@app.route('/add_meme', methods=['POST'])
def add_meme():
    bg_url = request.form['image']
    top_caption = request.form['top_caption']
    bottom_caption = request.form['bottom_caption']

    get_db().execute('INSERT INTO memes(url, caption1, caption2, image) VALUES(?, ?, ?, ?);', (
        bg_url,
        top_caption,
        bottom_caption,
        make_meme(bg_url, top_caption, bottom_caption).getvalue()
    ))

    return redirect(url_for('index'))

@app.route('/like_meme/<id>')
def like_meme(id):
    get_db().execute('UPDATE memes SET likes = likes + 1 WHERE id = ?', [id])
    return redirect(request.referrer)

@app.route('/add_comment/<id>', methods=['POST'])
def add_comment(id):
    get_db().execute('INSERT INTO comments (meme_id, author, message) VALUES(?, ?, ?);', [
        id,
        request.form['author'],
        request.form['message']
    ])

    return redirect(url_for('show', id=id))

def get_meme_by_id(id):
    return get_db().select('SELECT * FROM memes WHERE id=?;', [int(id)])[0]

@app.route('/meme/<id>')
def show(id):
    meme = get_meme_by_id(id)
    comments = get_db().select('SELECT * FROM comments WHERE meme_id = ?', id)
    meme['num_comments'] = len(comments)
    meme['comments'] = comments

    return render_template('show.html', meme=meme)

@app.route('/meme/<id>.jpg')
def show_image(id):
    meme = get_meme_by_id(id)
    return send_file(BytesIO(meme['image']), mimetype='image/png')

@app.route('/meme_form')
def meme_form():
    return render_template('meme-form.html')

@app.route('/')
def index():
    memes = get_db().select('SELECT id, url, caption1, caption2, likes FROM memes ORDER BY likes DESC')
    for meme in memes:
        meme['num_comments'] = get_db().select('SELECT COUNT(*) AS num FROM comments WHERE meme_id = ?', [int(meme['id'])])[0]['num']

    return render_template('homepage.html', memes=memes)

def chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

app.jinja_env.globals.update(chunk=chunk)

if __name__ == '__main__':
    app.run(host=os.environ.get('BIND_TO', '127.0.0.1'),
            port=int(os.environ.get('PORT', 5000)),
            debug=bool(int(os.environ.get('FLASK_DEBUG', 1))))
