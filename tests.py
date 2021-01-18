# Reference. https://www.patricksoftwareblog.com/unit-testing-a-flask-application/.
import os
import unittest
from wisk import create_app, db
from wisk.articles.utils import get_top_headlines

TEST_DB = 'test.db'

application = create_app()

class BasicTests(unittest.TestCase):
    # Setup and teardown.

    # Executed prior to each test.
    def setUp(self):
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['DEBUG'] = False
        application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + TEST_DB

        self.application = application.test_client()

        # Need application context for any db operation.
        with application.app_context():
            db.drop_all()

            # Creates a test db in the wisk directory where site.db is located.
            db.create_all()

        self.assertEqual(application.debug, False)

    # Executed after each test.
    def tearDown(self):
        # Need application context for any db operation.
        with application.app_context():
            db.session.remove()
            db.drop_all()

    # Actual unit tests to execute.

    # Ensure that flask was set up correctly.
    def test_home_page(self):
        response = self.application.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Ensure that the about page is working correctly.
    def test_about_page(self):
        response = self.application.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is the about page.', response.data)

    # Ensure wisk/articles/utils.py is getting the top headlines.
    def test_get_top_headlines(self):
        articles = get_top_headlines()

        # Check if the articles list is non empty.
        # 'assertTrue' will check if articles returns True or not. If empty, it will be false.
        self.assertTrue(articles)

if __name__ == "__main__":
    unittest.main()
