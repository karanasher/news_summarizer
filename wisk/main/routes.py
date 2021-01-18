from flask import render_template, request, Blueprint
from wisk.models import Article

main = Blueprint('main', __name__)

# Home page.
@main.route('/')
def home():
    # Get url parameter.
    page = request.args.get('page', 1, type=int)

    # Get the articles from the db and display them on the home page. Newest first.
    # paginate allows you to restrict the number of articles that get displayed on each page.
    articles = Article.query.order_by(Article.ds.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', articles=articles)

@main.route('/about')
def about():
    return 'This is the about page.'
