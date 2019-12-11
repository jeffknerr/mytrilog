"""
given workouts, make a plot
"""

from datetime import datetime

def plot(workouts):
  for i in range(len(workouts)):
    w = workout[i]
    what = w.what
    when = w.when       # datetime obj
    wstr = when.strftime("%m/%d/%Y")
    amt = w.amount
    weight = w.weight   # float or None
    who = w.getUsername()
    com = w.comment
    print(i,what,wstr,amt,weight,who,com)

  # get current date
  # only use those workouts with same month as current date
  # plot line for weights

