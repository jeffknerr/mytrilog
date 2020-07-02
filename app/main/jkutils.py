"""
given workouts, make a plot/figure
"""

from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def makeFigure(workouts):
    """given workouts, make and return matplotlib Figure"""
    # get data in correct arrays
    N = 32
    sl = [0]*N    # swim list
    bl = [0]*N    # bike list
    rl = [0]*N    # run list
    xl = [0]*N    # xfit list
    doms = list(range(N))
    for i in range(len(workouts)):
        w = workouts[i]
        d = w.getDOM()
        what = w.what
        amt = w.amount
        if what == "swim":
            sl[d] = amt
        elif what == "run":
            rl[d] = amt
        elif what == "bike":
            bl[d] = amt
        elif what == "xfit":
            xl[d] = amt
        when = w.when       # datetime obj
        wstr = when.strftime("%m/%d/%Y")
        weight = w.weight   # float or None
        who = w.getUsername()
        com = w.comment
        print(i,what,wstr,amt,weight,who,com)
    swim = np.array(sl)
    bike = np.array(bl)
    run  = np.array(rl)
    xfit = np.array(xl)

    # make the figure/bar chart
    monthname = w.getMonthName()
    date = w.getDate()
    year = date.strftime("%Y")

    fig = Figure()
    ymax = 140
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim(1,N)
    ax.set_ylim(0,ymax)
    ax.set_xlabel("day of the month (%s)" % (monthname))
    ax.set_ylabel("workout duration (minutes)")
    ax.set_title("triathlon training data for %s, %s" % (monthname, year))

    ind = np.array(doms)  # the x locations for the groups
    width = 0.8           # the width of the bars: can also be len(x) sequence

    ax.set_yticks(np.arange(0,ymax,10))
    ax.set_xticks(np.arange(0,N+1,2))

    p1 = ax.bar(ind, swim, width, color='#3333ff')
    p2 = ax.bar(ind, bike, width, color='#00ff33', bottom=sum([swim]))
    p3 = ax.bar(ind, run , width, color='#ff33aa', bottom=sum([swim, bike]))
    p4 = ax.bar(ind, xfit, width, color='#33aacc', bottom=sum([swim, bike, run]))

    ax.grid(True)
    ax.legend( (p1[0], p2[0], p3[0], p4[0]), ('swim', 'bike', 'run ', 'xfit') , prop={'size':8})

    return fig

