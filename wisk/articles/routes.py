from flask import render_template, url_for, flash, redirect, request, Blueprint
from wisk import db
from wisk.articles.forms import SubmitArticle
from wisk.models import Article

articles = Blueprint('articles', __name__)

# To submit an article.
# methods is required to accept a form submission.
@articles.route('/submit_article', methods=['GET', 'POST'])
def submit_article():
    form = SubmitArticle()

    if form.validate_on_submit():
        # Create an article based on form submission.
        article = Article(
            source=form.source.data,
            title=form.title.data,
            url=form.url.data,
            url_to_img=form.url_to_img.data,
            ds=form.ds.data,
            summary=form.summary.data)

        # Add the new article in the db.
        db.session.add(article)

        # Commit changes to the db.
        db.session.commit()

        # Dsplay a success message.
        flash(f'Article submitted from {form.source.data}', 'success')

        # Redirect to the home page.
        return redirect(url_for('main.home'))

    return render_template('submit_article.html', title='Submit article', form=form)

@articles.route('/article/<int:article_id>')
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('article.html', title=article.title, article=article)

# Route to delete an article.
@articles.route("/article/<int:article_id>/delete", methods=['POST'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)

    db.session.delete(article)
    db.session.commit()

    flash('Your article has been deleted.', 'success')
    return redirect(url_for('main.home'))

# To show all articles from a particular source.
@articles.route('/source/<string:source_name>')
def source(source_name):
    page = request.args.get('page', 1, type=int)

    # Get the all articles from the requested source and display them on the home page. Newest first.
    # paginate allows you to restrict the number of articles that get displayed on each page.
    articles = Article.query.filter_by(source=source_name)\
        .order_by(Article.ds.desc())\
        .paginate(page=page, per_page=10)

    return render_template('source.html', articles=articles)
