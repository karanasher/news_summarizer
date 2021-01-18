from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from wisk.models import Article

class SubmitArticle(FlaskForm):
    source = StringField('Source', validators=[DataRequired(), Length(min=1, max=25)])
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=250)])
    url = StringField('URL', validators=[DataRequired(), Length(min=1, max=250)])
    url_to_img = StringField('URL to image', validators=[DataRequired(), Length(min=1, max=250)])
    ds = StringField('Published on', validators=[DataRequired(), Length(min=10, max=10)])
    summary = StringField('Summary', validators=[DataRequired(), Length(min=1, max=2500)])

    # Button.
    submit = SubmitField('Submit')

    # Validate that ds has a length of 10.
    def validate_ds(self, ds):
        if len(ds.data) != 10:
            raise ValidationError('ds should be of length 10. Example 2020-11-20.')
