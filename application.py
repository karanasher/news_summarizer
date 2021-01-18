# The name of this file should ALWAYS be named application for you to run this on AWS.
from wisk import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from wisk.models import Article
from wisk import db
from flask import current_app
import atexit
from wisk.articles.utils import get_top_headlines
from datetime import datetime, timedelta

# This should ALWAYS be named application for you to run this on AWS.
application = create_app()

# This function exists over here since we need the application context to perform db operations.
def ingest_articles_in_db():
    with application.app_context():
        print('Entered ingest_articles_in_db.')

        # Get today - 2 days.
        delete_beyond_ds = str(datetime.today() - timedelta(days=1))[:10]

        Article.query.delete()
        # Article.query.filter(Article.ds < delete_beyond_ds).delete()
        db.session.commit()

        print('deleted all entries in db.')

        # Get all top headlines.
        articles = get_top_headlines()

        print('Got a response from  get_top_headlines.')

        if articles:
            # Add each article in the db.
            for article in articles:
                try:
                    print('Trying to insert an article in the db.')
                    current_article = Article(
                        source=article['source'],
                        title=article['title'],
                        url=article['url'],
                        url_to_img=article['url_to_img'],
                        ds=article['ds'],
                        summary=article['summary'])

                    # Add the new article in the db.
                    db.session.add(current_article)

                    # Commit changes to the db.
                    db.session.commit()

                    print('db commit complete.')
                except Exception as e:
                    print('An exception occurred while inserting an article in the db. Continuing with the rest.')
                    print(e)
                    continue

# Schedule the cron job to run daily.
print('Initializing scheduler.')
scheduler = BackgroundScheduler()
job = scheduler.add_job(ingest_articles_in_db, 'interval', days=1, start_date='2020-11-27 09:00:00')
scheduler.start()
print('Started the scheduler.')

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    application.run(debug = True)
