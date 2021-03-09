"""
given workouts, make a plot/figure
"""

import datetime
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
    yl = [0]*N    # yoga list
    xl = [0]*N    # xfit list
    dates = [0]*N # date of workout list
    for i in range(N):
        dt = now - datetime.timedelta(days=(N-(i+1)))
        dates[i] = datetime.date(dt.year,dt.month,dt.day)
    for i in range(len(workouts)):
        w = workouts[i]
        daysago = (N-1) - (now - w.when).days
        what = w.what
        amt = w.amount
        if what == "swim":
            sl[daysago] = amt
        elif what == "run":
            rl[daysago] = amt
        elif what == "yoga":
            yl[daysago] = amt
        elif what == "bike":
            bl[daysago] = amt
        elif what == "xfit":
            xl[daysago] = amt
        when = w.when       # datetime obj
        wstr = when.strftime("%m/%d/%Y")
        weight = w.weight   # float or None
        who = w.getUsername()
        com = w.comment
        #print(i,what,wstr,amt,weight,who,com,when,daysago,dates[daysago])
    swim = np.array(sl)
    bike = np.array(bl)
    run  = np.array(rl)
    yoga  = np.array(yl)
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
    width = 0.8           # the width of the bars
    ax.set_yticks(np.arange(0,ymax,10))

    p1 = ax.bar(dates, swim, width, color='#3333ff')
    p2 = ax.bar(dates, bike, width, color='#00ff33', bottom=sum([swim]))
    p3 = ax.bar(dates, run , width, color='#ff33aa', bottom=sum([swim, bike]))
    p4 = ax.bar(dates, xfit, width, color='#33aacc', bottom=sum([swim, bike, run]))
    p5 = ax.bar(dates, yoga, width, color='#ffa500', bottom=sum([swim, bike, run, xfit]))

    ax.grid(True)
    ax.legend( (p1[0], p2[0], p3[0], p4[0], p5[0]), ('swim', 'bike', 'run ',
                                              'xfit', 'yoga') , prop={'size':8})
    # Rotate date labels automatically
    fig.autofmt_xdate()

    return fig

def weightPlot(workouts,now,then):
    """given workouts, make and return matplotlib weight Figure"""
    # get data in correct arrays
    N = 30
    wdata = [0]*N   # weight data list
    dates = [0]*N   # date of workout list
    for i in range(N):
        dt = now - datetime.timedelta(days=(N-(i+1)))
        dates[i] = datetime.date(dt.year,dt.month,dt.day)
    wtotal = 0.0
    wcounter = 0
    for i in range(len(workouts)):
        w = workouts[i]
        daysago = (N-1) - (now - w.when).days
        what = w.what
        when = w.when       # datetime obj
        wstr = when.strftime("%m/%d/%Y")
        if w.weight == None:
            weight = 0
        else:
            weight = w.weight
            wtotal += weight
            wcounter += 1
            wdata[daysago] = weight
        com = w.comment
        #print(i,what,wstr,amt,weight,who,com,when,daysago,dates[daysago])
    realdata = []
    realdates = []
    for i in range(len(wdata)):
        if wdata[i] != 0:
            realdata.append(wdata[i])
            realdates.append(dates[i])
    fig = Figure()
    if wcounter == 0:
        average = 160
    else:
        average = wtotal/wcounter
    wdata = [average]*N
    weight = np.array(wdata)
    dates = np.array(dates)
    ymax = average + 10
    ymin = average - 10
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim((ymin,ymax))
    ax.set_xlabel("last 30 days")
    ax.set_ylabel("weight (lbs)")
    nstr = now.strftime("%m/%d/%Y")
    tstr = then.strftime("%m/%d/%Y")
    ax.set_title("weight data for %s to %s" % (tstr, nstr))
    myFmt = DateFormatter("%b %d")
    ax.xaxis.set_major_formatter(myFmt)

    ax.plot(dates, weight, 'r-')
    ax.plot(realdates, realdata, 'bh-')
    ax.grid(True)
    # Rotate date labels automatically
    fig.autofmt_xdate()

    return fig

def getStats(workouts,now,then):
    """given workouts, calc and return stats"""
    wl = []   # weight data list
    sl = []   # swim list
    bl = []   # bike list
    rl = []   # run list
    yl = []   # yoga list
    xl = []   # xfit list
    for i in range(len(workouts)):
        w = workouts[i]
        what = w.what
        amt = w.amount
        if what == "swim":
            sl.append(amt)
        elif what == "run":
            rl.append(amt)
        elif what == "yoga":
            yl.append(amt)
        elif what == "bike":
            bl.append(amt)
        elif what == "xfit":
            xl.append(amt)
        if w.weight != None:
            wl.append(w.weight)
    totrun = sum(rl)/9.0 # assumes 9-min/mile pace
    avgw = 0
    if len(wl) > 0:
      avgw = sum(wl)/len(wl)
    # average weight, total run, and total run per week
    return avgw,totrun,totrun/4.0
