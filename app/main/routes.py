
from app.main.jkutils import *
from flask_login import current_user, login_required
from flask import render_template, flash, redirect, url_for, request, current_app, abort
from app import db
from app.main.forms import EditProfileForm, WorkoutForm, ChangeWorkoutForm
from app.models import User, Workout
from datetime import datetime, timedelta
from app.main import bp
from flask import make_response
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(what=form.what.data,
                          when=form.when.data,
                          amount=form.amount.data,
                          weight=form.weight.data,
                          comment=form.comment.data,
                          athlete=current_user)
        db.session.add(workout)
        db.session.commit()
        flash("Logged your workout!")
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.what.data = "rest"
    page = request.args.get('page', 1, type=int)
    workouts = current_user.followed_workouts().paginate(
        page, current_app.config['WORKOUTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=workouts.next_num) if workouts.has_next else None
    prev_url = url_for('main.index', page=workouts.prev_num) if workouts.has_prev else None

    return render_template('index.html', title='Home', form=form,
                            workouts=workouts.items, next_url=next_url,
                            prev_url=prev_url)


@bp.route('/about')
def about():
    return render_template('about.html', title='About')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    workouts = user.workouts.order_by(Workout.when.desc()).paginate(
        page, current_app.config['WORKOUTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=workouts.next_num) if workouts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=workouts.prev_num) if workouts.has_prev else None
    return render_template('user.html', user=user, workouts=workouts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                           title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    workouts = Workout.query.order_by(Workout.when.desc()).paginate(
                                      page, current_app.config['WORKOUTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=workouts.next_num) if workouts.has_next else None
    prev_url = url_for('main.explore', page=workouts.prev_num) if workouts.has_prev else None
    return render_template('index.html', title='Explore', workouts=workouts.items, 
                     next_url=next_url, prev_url=prev_url)
    # reuses index template, but without the submit form part


@bp.route('/plot/<user>')
@login_required
def plot(user):
    if current_user.username != user:
        return redirect(url_for('main.user', username=current_user.username))
    # only get current user's workouts for plotting
    now = datetime.utcnow()
    then = now - timedelta(days=29)
    dbid = current_user.get_id()
    # only get last 30 days of workouts
    workouts = Workout.query.filter_by(who=dbid).filter(Workout.when <= now, Workout.when >= then).all()
    # filter such that only workouts from last 30 days...
    # make the plot
    fig = makeFigure(workouts,now,then)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


@bp.route('/weightplot/<user>')
@login_required
def weightplot(user):
    if current_user.username != user:
        return redirect(url_for('main.user', username=current_user.username))
    # only get current user's workouts for plotting
    now = datetime.utcnow()
    then = now - timedelta(days=29)
    dbid = current_user.get_id()
    # only get last 30 days of workouts
    workouts = Workout.query.filter_by(who=dbid).filter(Workout.when <= now, Workout.when >= then).all()
    # filter such that only workouts from last 30 days...
    # make the plot
    fig = weightPlot(workouts,now,then)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@bp.route('/ytd')
@login_required
def ytd():
    return render_template('ytd.html', title='ytd')

@bp.route('/ytdplot/<user>')
@login_required
def ytdplot(user):
    if current_user.username != user:
        return redirect(url_for('main.user', username=current_user.username))
    # only get current user's workouts for plotting
    now = datetime.utcnow()
    then = now - timedelta(days=364)
    dbid = current_user.get_id()
    workouts = Workout.query.filter_by(who=dbid).filter(Workout.when <= now, Workout.when >= then).all()
    # make the plot
    fig = makeYTDFigure(workouts,now,then)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

@bp.route('/stats')
@login_required
def stats():
    # only get current user's workouts for plotting
    now = datetime.utcnow()
    then = now - timedelta(days=29)
    dbid = current_user.get_id()
    # only get last 30 days of workouts
    workouts = Workout.query.filter_by(who=dbid).filter(Workout.when <= now, Workout.when >= then).all()
    avgw, runtot, weekrun = getStats(workouts, now, then)
    # convert to strings to format nicely...
    avgw = "%.1f" % (avgw)
    runtot = "%.1f" % (runtot)
    weekrun = "%.2f" % (weekrun)
    return render_template('stats.html',
                           title='Stats',
                           user=user,
                           avgw=avgw,
                           runtot=runtot,
                           weekrun=weekrun)


@bp.route('/edit')
@login_required
def edit():
    """show workouts, allow user to select one for editing"""
    username = current_user.username
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    workouts = user.workouts.order_by(Workout.when.desc()).paginate(
        page, 5 + current_app.config['WORKOUTS_PER_PAGE'], False)
    next_url = url_for('main.edit', username=user.username, page=workouts.next_num) if workouts.has_next else None
    prev_url = url_for('main.edit', username=user.username, page=workouts.prev_num) if workouts.has_prev else None
    return render_template('edit.html', user=user, workouts=workouts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/editworkout/<what>/<when>/<who>', methods=['GET', 'POST'])
@login_required
def editworkout(what, when, who):
    """present form to user that allows them to edit the workout"""
    username = current_user.username
    dtwhen = datetime.fromisoformat(when)
    wrkout = Workout.query.filter_by(who=who).filter_by(when=dtwhen).filter_by(what=what).first_or_404()
    # make sure user is correct user
    if wrkout.getUsername() != username:
        abort(403)
    form = ChangeWorkoutForm()
    if form.validate_on_submit():
        wrkout.what = form.what.data
        wrkout.when = form.when.data
        wrkout.amount = form.amount.data
        wrkout.weight = form.weight.data
        wrkout.comment = form.comment.data
        db.session.commit()
        flash("Saved your edited workout...")
        return redirect(url_for('main.index'))
    # add the existing data here
    form.what.data = wrkout.what
    form.when.data = wrkout.when
    form.amount.data = wrkout.amount
    form.weight.data = wrkout.weight
    form.comment.data = wrkout.comment
    return render_template("changeworkout.html", form=form)
