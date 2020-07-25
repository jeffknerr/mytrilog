"""
given workouts, make a plot/figure
"""

from datetime import datetime,timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

def makeFigure(workouts,now,then):
    """given workouts, make and return matplotlib Figure"""
    # get data in correct arrays
    N = 30
    sl = [0]*N    # swim list
    bl = [0]*N    # bike list
    rl = [0]*N    # run list
    xl = [0]*N    # xfit list
    dates = [0]*N # date of workout list
    for i in range(N):
        date = now - timedelta(days=(N-(i+1)))
        dates[i] = date
    doms = list(range(N))
    for i in range(len(workouts)):
        w = workouts[i]
        daysago = (N-1) - (now - w.when).days
        what = w.what
        amt = w.amount
        if what == "swim":
            sl[daysago] = amt
        elif what == "run":
            rl[daysago] = amt
        elif what == "bike":
            bl[daysago] = amt
        elif what == "xfit":
            xl[daysago] = amt
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
    dates = np.array(dates)

    fig = Figure()
    ymax = 140  # minutes
    ax = fig.add_subplot(1, 1, 1)
#   ax.set_xlim(1,N)
    ax.set_ylim(0,ymax)
    ax.set_xlabel("last 30 days")
    ax.set_ylabel("workout duration (minutes)")
    nstr = now.strftime("%m/%d/%Y")
    tstr = then.strftime("%m/%d/%Y")
    ax.set_title("triathlon training data for %s to %s" % (tstr, nstr))
    myFmt = DateFormatter("%b %d")
    ax.xaxis.set_major_formatter(myFmt)

    ind = np.array(doms)  # the x locations for the groups
    width = 0.8           # the width of the bars: can also be len(x) sequence

    ax.set_yticks(np.arange(0,ymax,10))
#   ax.set_xticks(np.arange(0,N+1,2))
    # change x ticks to be dates list!

    p1 = ax.bar(dates, swim, width, color='#3333ff')
    p2 = ax.bar(dates, bike, width, color='#00ff33', bottom=sum([swim]))
    p3 = ax.bar(dates, run , width, color='#ff33aa', bottom=sum([swim, bike]))
    p4 = ax.bar(dates, xfit, width, color='#33aacc', bottom=sum([swim, bike, run]))

    ax.grid(True)
    ax.legend( (p1[0], p2[0], p3[0], p4[0]), ('swim', 'bike', 'run ', 'xfit') , prop={'size':8})
    ## Rotate date labels automatically
    fig.autofmt_xdate()

    return fig

