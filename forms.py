from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SubmitDataForm(FlaskForm):
    # id_face = StringField('id')
    nume = StringField('nume')
    submit = SubmitField('Colect data')
