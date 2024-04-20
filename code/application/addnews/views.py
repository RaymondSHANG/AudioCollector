from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user
from application import db
from sqlalchemy import desc

from application.models import News

import application.addnews.myGoogleNews as myGoogleNews

news_bp = Blueprint('news_bp', __name__)


@news_bp.route('/showNews', methods=['GET', 'POST'])
def showNews():
    # entities = MyEntity.query.order_by(MyEntity.my_date.desc()).limit(3).all()

    news_select = News.query.order_by(News.pub_date.desc()).limit(10).all()
    # News.query.all()

    return render_template('news.html', news_select=news_select)


@news_bp.route('/addNews', methods=['GET', 'POST'])
def addNews():
    myNews = myGoogleNews.myGoogleNews()
    # t = myGoogeNews.myGoogeNews()

    new_news = myNews.getNews(max_words=200, N_news=10, verbose=False)
    if request.method == 'POST':
        news_obj = [News(title=current_news['title'],
                         body=current_news['body'],
                         pub_date=current_news['date'],
                         length=current_news['length'],
                         hashtags=current_news['hashtags'],
                         level=current_news['level'])
                    for current_news in new_news]
        db.session.add_all(news_obj)
        db.session.commit()
        return redirect(url_for('news_bp.showNews'))
    else:
        return render_template('add_news.html', new_news=new_news)
