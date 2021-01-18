# Reference.
#     https://stackoverflow.com/questions/11810461/how-to-perform-periodic-task-with-flask-in-python
#     https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
#     https://pypi.org/project/APScheduler/
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from wisk.articles.utils import get_top_headlines
from wisk.models import Article
from wisk import db
from flask import current_app

# Get all top headlines from utils and dump them into the db.
def ingest_articles_in_db():
    print('hello.')
    # print(current_app.name)

    # with current_app.app_context():
    #     article = Article.query.all()
        # print('world.')

    # # Get all top headlines.
    # articles = get_top_headlines()

    # if articles:
    #     # Add each article in the db.
    #     for article in articles:
    #         current_article = Article(
    #             source=article['source'],
    #             title=article['title'],
    #             url=article['url'],
    #             url_to_img=article['url_to_img'],
    #             ds=article['ds'],
    #             summary=article['summary'])

    #         # Add the new article in the db.
    #         db.session.add(current_article)

    #         # Commit changes to the db.
    #         db.session.commit()

# Use apscheduler to schedule a daily cron job to fetch the top headlines and dump them into the db.
def start_article_ingestion_cron_job():
    print('start_article_ingestion_cron_job')
    print(current_app.name)

    scheduler = BackgroundScheduler()
    job = scheduler.add_job(ingest_articles_in_db, 'interval', seconds=5, start_date='2020-11-27 13:32:00')
    scheduler.start()

    print(Article.query.first())
    print(current_app.name)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
