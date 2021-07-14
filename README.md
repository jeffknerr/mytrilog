# mytrilog
Web app to log triathlon workouts


## based on [The Flask Mega Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

All of this is just adapted from 
[Miguel's excellent flask tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
The tutorial creates a blogging app. My app changes the blog entries to
workouts, allowing the user to enter workouts and see graphs showing
past workouts.

## still under construction

I've got a working app now! Still very rough and klunky,
but you can log workouts and see a graph.

I'm using `PREFIX = "/mytrilog"` in `app/__init__.py` to make the website
available in the /mytrilog directory, off of the nginx main website directory.

![mytrilog screenshot](screenshot.png)

---

# local test/installation instructions

I am running this on debian 10/ubuntu 20.04 linux computers.

Set up the `.env` file (if you want to test emails, for password resets):

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
besides "your-secret-key-here"), and `ADMINS` is a list of string email address 
for site admins (they get emails when things go wrong).

Next install flask and everything needed:

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
have to go to `http://127.0.0.1:5000/mytrilog`, which should show
you a "Sign In" page.

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
edit templates and links:
[https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python](https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python)
