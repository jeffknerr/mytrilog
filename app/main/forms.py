
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms import TextAreaField, DateField, FloatField
from wtforms.validators import ValidationError, DataRequired, Length, Optional
from app.models import User
from datetime import date


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class WorkoutForm(FlaskForm):
    wkts = "run bike swim xfit rest yoga".split()
    whats = []
    for w in wkts:
        whats.append((w,w))
    what = RadioField('Type of workout?', choices=whats)
    when = DateField(id='datepick', format='%Y-%m-%d', default=date.today)
    amount = FloatField(default=0)
    weight = FloatField('Weight (optional)', validators=[Optional()])
    comment = TextAreaField('Comments?', validators=[Length(min=0, max=140)])
    submit = SubmitField('Log it!')

