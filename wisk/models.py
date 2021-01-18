# This is the database schema.
from wisk import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    url_to_img = db.Column(db.String(250), nullable=False, default='url_not_found')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    ds = db.Column(db.String(10), nullable=False)
    summary = db.Column(db.Text, nullable=False)

    # This is to print the object.
    def __repr__(self):
        return f"Article('{self.source}', '{self.title}', '{self.image_file}')"
