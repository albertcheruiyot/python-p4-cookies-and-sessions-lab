#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    serialized_articles = [article.to_dict() for article in articles]
    return jsonify(serialized_articles)
    pass

@app.route('/articles/<int:id>')
def show_article(id):
    
    session['page_views'] = session.get('page_views', 0)

    
    session['page_views'] += 1

    
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    
    article = Article.query.get_or_404(id)

    return jsonify({
        'id': article.id,
        'author': article.author,
        'title': article.title,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date.strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': article.user_id
    })
    pass

if __name__ == '__main__':
    app.run(port=5555)
