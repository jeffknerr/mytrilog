# mytrilog
A web app to log triathlon workouts.


## based on [The Flask Mega Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

_All_ of this is just adapted from 
[Miguel's excellent flask tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
Miguel's tutorial creates a blogging app. My app changes the blog entries to
workouts, allowing the user to enter workouts (e.g., 2021-07-14 run 30 minutes)
and see graphs showing progress and past workouts. The workouts also have an
optional _weight_ component, if you want to track your weight vs time.

## still (forever?) under construction

I've got a working app now! Still very rough and klunky,
but you can log workouts and see a graph and some stats.

![mytrilog screenshot](screenshot.png)

Features of the mytrilog app:
- allows user to enter run/bike/swim/xfit/yoga/rest workouts
- can do more than one workout per day (e.g., bike and run)
- all workouts are shown in _minutes_. I usually put the mileage in the comment.
- start page shows a graph of the workouts for the past 30 days
- workouts and weight graphs done with matplotlib
- optional weight tracking if you log that info
- when logging workouts, date field uses 
[Miguel's datetimepicker-example](https://gist.github.com/miguelgrinberg/5a1b3749dbe1bb254ff7a41e59cf04c9)
- Stats page shows info for past 30 days (avg miles per week, avg weight)
- user can Edit a past workout, if data was entered incorrectly
- plus all of the cool stuff from 
[Miguel's tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
(login, logout, register, reset password, etc)
- uses `PREFIX = "/mytrilog"` in `app/__init__.py` to make the website
available in the /mytrilog directory (in case you already have a full website,
and just want this deployed in a subdirectory)


Still to do:
- add more to the Stats page
- add YTD graph and stats
- add unit testing!!
- full code review...

---

# local test/installation instructions

I am running this on debian 10/ubuntu 20.04 linux computers.
That's all I've tested this on so far.

Clone the repo and then
set up the `.env` file (e.g., if you want to test emails for password resets)
in the top-level directory:

```
SECRET_KEY=your-secret-key-here
MAIL_SERVER=your.mailserver.net
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=yourusername
MAIL_PASSWORD='your.password.here'
ADMINS=["user@yourserver.net"]
```

For example, if you want to send mail using your gmail account, 
here are the settings:

```
SECRET_KEY=your-secret-key-here
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME="yourusername@gmail.com"
MAIL_PASSWORD="your 16-char app password"
ADMINS=["user@yourserver.net"]
```

Note: the `16-char app password` is a
[google app password](https://security.google.com/settings/security/apppasswords)
that you have to set up (not hard).

Also, `SECRET_KEY` is just used by Flask for security (set it to something
besides "your-secret-key-here"), and `ADMINS` is a list of string email addresses
for site admins (they get emails when things go wrong).

Next install flask and everything needed in the virtual environment:

```
apt-get install python3-venv
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
```

That should start the development server which says to use
http://127.0.0.1:5000, but because I am using `PREFIX=/mytrilog`, you 
have to go to http://127.0.0.1:5000/mytrilog, which should show
you a "Sign In" page. Click on the "Click to Register!" link to
add a new user and test out the app.

---

# production test/installation instructions

- gunicorn
- nginx
- certbot/letsencrypt
- supervisord
- git auto-deploy
- static dir link from main website back to app/static dir???

---

### stuff I always have to look up

#### manually delete entry from db

```
$ mysql -u username -p mytrilog
Enter password:  (see enviro file)
Reading table information for completion of table and column names
...
MariaDB [mytrilog]> show tables;
+--------------------+
| Tables_in_mytrilog |
+--------------------+
| alembic_version    |
| followers          |
| user               |
| workout            |
+--------------------+
4 rows in set (0.000 sec)

MariaDB [mytrilog]> select * from workout;
+-----+------+---------------------+--------+--------+------+-------------------------------------+
| id  | what | when                | amount | weight | who  | comment                             |
+-----+------+---------------------+--------+--------+------+-------------------------------------+
|   1 | xfit | 2020-07-04 00:00:00 |     26 |  162.2 |    1 | abs w/family                        |
|   2 | xfit | 2020-07-03 00:00:00 |     40 |   NULL |    1 | 20-min xfit plus 20-min yoga w/SK   |
|   3 | rest | 2020-07-02 00:00:00 |      0 |   NULL |    1 | HK moved to PA                      |
...
| 121 | run  | 2020-10-12 00:00:00 |     10 |   NULL |    1 | 1mi                                 |
| 122 | xfit | 2020-10-12 00:00:00 |     30 |  161.6 |    1 | yoga                                |
+-----+------+---------------------+--------+--------+------+-------------------------------------+
122 rows in set (0.000 sec)

MariaDB [mytrilog]> delete from `workout` where `id` = 120;
Query OK, 1 row affected (0.002 sec)

MariaDB [mytrilog]> Bye
```

#### auto-deploy

- added webhook to server
- added location and proxy_pass to nginx site enabled
- using supervisord to start/stop webhook service
- added webhook to github, also deploy key
- git commit/push for repo triggers github webhook, which is seen 
    by webhook service on server, and runs a deploy script (pull
    the repo, rsync files to /var/www location, restart webapp)

### Added Edit

I added an Edit Workout option, for when I type in the wrong date or
wrong workout "what". Thanks to Randall Degges for this page and help with the
"edit" templates and links:
[https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python](https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python)
