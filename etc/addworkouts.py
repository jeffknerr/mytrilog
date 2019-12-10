"""
add workouts from training.data file

# training data for Oct, 2019
2019-10-01:weight:158.0
2019-10-01:xfit:50:10Murph 28/5/10/15
2019-10-01:run:18:2mi
2019-10-02:weight:156.6
2019-10-02:xfit:35:275 burpees
2019-10-03:xfit:35:276 burpees, jury duty
"""

from app import db
from app.models import User, Workout
from datetime import datetime

def readfile(fn,u):
  workouts = []
  inf = open(fn,"r")
  for line in inf:
    if not line.startswith("#"):
      data = line.strip().split(":")
      date = data[0]
      year,month,day = date.split("-")
      d = datetime(int(year),int(month),int(day))
      what = data[1]
      amount = float(data[2])
      comment = ""
      weight=157.2
      if what != "weight":
        comment = data[3]
        w = Workout(what=what,when=d,amount=amount,weight=weight,comment=comment,athlete=u)
        workouts.append(w)
  inf.close()
  return workouts

users = User.query.all()
u = None
for user in users:
  if user.username == "jeff":
    u = user
print(u)

workouts = readfile("training.data",u)
for w in workouts:
  print(w)
  db.session.add(w)
db.session.commit()

#    workout = Workout(what=form.what.data, 
#                      when=form.when.data,
#                      amount=form.amount.data,
#                      weight=form.weight.data,
#                      comment=form.comment.data,
#                      athlete=current_user)
#    db.session.add(workout)

#class WorkoutForm(FlaskForm):
#    what = TextAreaField('Run/Bike/Swim/Xfit', validators=[DataRequired(), Length(min=1, max=140)])
#    when = DateField()
#    amount = FloatField()
#    weight = FloatField()
#    comment = TextAreaField('Comments?', validators=[Length(min=0, max=140)])
#    submit = SubmitField('Submit')


