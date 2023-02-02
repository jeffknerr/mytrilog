# mytrilog
A web app to log triathlon (and other) workouts.


## based on [The Flask Mega Tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

_All_ of this is just adapted from 
[Miguel's excellent flask tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
Miguel's tutorial creates a blogging app. My app changes the blog entries to
workouts, allowing the user to enter workouts (e.g., 2021-07-14 run 30 minutes)
and see graphs showing progress and past workouts. The workouts also have an
optional _weight_ component, if you want to track your weight vs time.

## still (forever!) under construction

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
- YTD page showing year-to-date graphs
- user can Edit a past workout, if data was entered incorrectly
- plus all of the cool stuff from 
[Miguel's tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
(login, logout, register, reset password, etc)
- uses `PREFIX = "/mytrilog"` in `app/__init__.py` to make the website
available in the /mytrilog directory (in case you already have a full website,
and just want this deployed in a subdirectory)


Still to do:
- YTD stats: add miles run
- add an export-to-csv button for the data
- finish writing the README
- add a DELETE workout option (in case two have same what)
- add more to the Stats page
- add unit testing!!
- full code review...
- write script to populate db with good fake data

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

I'm using a setup very similar to 
[Miguel's _deploy on linux_ article](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux). The main differences for me are:

- I already had a debian linux server running on
[linode.com](https://www.linode.com/) that was hosting a website, so
I wanted to host this app off the current website in `/mytrilog`. That's
why my code uses the `PREFIX = "/mytrilog"` in `app/__init__.py`
- I set up my github repo to auto-deploy, using a webhook
- I use certbot/letsencrypt for the SSL cert

Below are my notes on setting up each part of the service.

### overview

- certbot/letsencrypt: provide the SSL cert so everything is encrypted
- nginx: serves out my current website, plus uses `proxy_pass` for the
webhook (anything that starts with `/hooks/`) and the flask app (anything
that starts with `/mytrilog`)
- gunicorn: a web server running on localhost:8000 that actually serves the
flask mytrilog app (nginx forwards any requests that start with `/mytrilog`
over to the gunicorn server)
- supervisord: an easy way to start/restart gunicorn when my server boots. Also used
to start the webhook daemon that listens for connections from github.
- git auto-deploy: sends a specific request/payload to my server each time I
"git commit/push" the repo
- static dir link from main website back to app/static dir: still need to fix
this, but I have a link from `/var/www/mywebsite/static` to 
`/var/www/mytrilog/app/static/`. Without that I couldn't get any static
content (css, images) to show up on the web app.

Details on all of this below...

### certbot/letsencrypt

    sudo apt-get update
    sudo apt-get install certbot python-certbot-nginx
    sudo certbot --nginx

- give server FQDN for "domain name"
- choose "Redirect all requests to https"
- should put certs in `/etc/letsencrypt/live/your.fqdn/`

### nginx

Below is most of my `/etc/nginx/sites-enabled` file.
What it's doing:

- redirecting all port 80 traffic to https
- serving out a website at /var/www/yourFQDNsite
- sending any `https://your.fqdn/hooks` traffic to `localhost:9000`
where `webhook` is listening
- sending any `https://your.fqdn/mytrilog` traffic to `localhost:8000`
where `gunicorn` is listening


```
/etc/nginx/sites-enabled$ cat your.fqdn

server {
    # listen on port 80 (http)
    listen 80;
    server_name your.fqdn;

    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}

server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name your.fqdn;
    root   /var/www/yourFQDNsite;
    ssi on;

    # location of the self-signed SSL certificate
    ssl_certificate /etc/letsencrypt/live/your.fqdn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your.fqdn/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # write access and error logs to /var/log
    access_log /var/log/fqdn_access.log;
    error_log /var/log/fqdn_error.log;

    # forward webhook requests to local webhooks server
    # NOTE: trailing slash on location /hooks/ is IMPORTANT :(
    location /hooks/ {
        proxy_pass http://127.0.0.1:9000/hooks/;
    }

    location /mytrilog {
        # forward application requests to the gunicorn server
        proxy_pass http://127.0.0.1:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~ /.well-known/acme-challenge {
      allow all;
    }
    location ~ ^/(README|INSTALL|LICENSE|CHANGELOG|UPGRADING)$ {
      deny all;
    }

}
```

### create user account

See
[Miguel's _deploy on linux_ article](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux) 
for notes on creating and securing this account. 
He creates a user called 'ubuntu'. Below,
I'll use `appuser` for the user that runs the app.

### mysql setup

Similar to 
[Miguel's _deploy on linux_ article](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux), 
except debian uses `mariadb`. 
There's a nice
[digital ocean guide to setting up mariadb on debian 10](https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-debian-10). 

After installing I set up the db:

```
$ sudo mysql -u root
mysql> create database mytrilog character set utf8 collate utf8_bin;
mysql> create user 'appuser'@'localhost' identified by 'dbpassword';
mysql> grant all privileges on mytrilog.* to 'appuser'@'localhost';
mysql> flush privileges;
mysql> quit;
```

In the above, the 'dbpassword' string is what you put in your `.env` file,
and `appuser` is the username you use to run the app and access the database.

Here's a `.env` file for the above mariadb setup:

```
SECRET_KEY='a really long string of chars'
MAIL_SERVER=your.fqdn
DATABASE_URL=mysql+pymysql://appuser:dbpassword@127.0.0.1:3306/mytrilog
ADMINS=['adminuser@your.fqdn']
```

### gunicorn

This is the web server for the flask application. Use `pip` to install
the gunicorn package into the flask virtual environment:

```
cd /notsurewhere
git clone git@github.com:jeffknerr/mytrilog.git
cd mytrilog
vim .env         # add your env variables here
apt-get install python3-venv
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
flask db upgrade
pip install gunicorn
```

Note: I used `/notsurewhere` above because I was just showing how to install
gunicorn in the venv. See full install details below for how I set up everything. You could
make `/notsurewhere` be `/var/www`, but I don't think you want the whole git repo
in `/var/www`...

### supervisord

Install the `supervisor` package and set up two config files
in `/etc/supervisor/conf.d`:

```
$ cat mytrilog.conf
[program:mytrilog]
command=/var/www/mytrilog/venv/bin/gunicorn -b localhost:8000 -w 4 mytrilog:app
directory=/var/www/mytrilog
user=appuser
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true

$ cat webhook.conf
[program:webhook]
command=/usr/bin/webhook -hooks hooks.json -verbose -port 9000
directory=/somewhere/webhook
user=appuser
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

I'll explain the webhook next, and `/somewhere/webhook` is wherever you
want to put the webhook scripts.

Both of those configs just run daemons (gunicorn and webhook), and supervisord
will take care of starting them at boot, and restarting them if needed.

Not sure, but I might have also changed the permissions on the 
`/var/run/supervisor.sock` file:

```
/etc/supervisor $ cat supervisord.conf

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0770                      ; sockef file mode (default 0700)
chown=root:adm
...
...
```

### git webhook

This part isn't needed to run the `mytrilog` app on your server. It's really
only useful for me, if I update the repo. Might be useful for you if you 
create your own app, based on this one, and want to set it up to auto-deploy 
on a "git push". I'm really just putting my setup notes here so I can remember
what I did next time...

Install the webhook software:

```
sudo apt-get install webhook
```

See the 
[webhook docs](https://github.com/adnanh/webhook)
for all the details.

I use `/somewhere/webhook` (e.g., `/var/www/webhook`) to store
scripts that fire when the webhook is triggered, and also as the
place to `git pull` the repo. Here's an overview of all that happens
when I commit and push to the git repo:

- github sends POST request to my payload URL: `https://your.fqdn/hooks/deploy-myapp`
- nginx sees a request that starts with `/hooks` and proxy_passes it to webhook on port 9000
- webhook sees the request, with the `deploy-myapp` id, and looks for a `/somewhere/webhook/hooks.json` file
- in that json file is a deploy-myapp section that, if the secret is correct, fires a `/somewhere/webhook/deploy.sh` script I wrote
- in `deploy.sh` I do a `git pull` and fire off a second script: `deployLocal`
- finally, in `deployLocal`, I have everything needed to either start or upgrade the mytrilog app

#### github webhook setup

If you haven't already, you need ssh keys added to github to be
able to push and pull. The `appuser` also needs to be able to pull
the repo without needing a password.

To set up the github webhook:

- Settings
- Webhooks
- Add webhook
- type in payload URL (see above)
- Content type is `application/json`
- add a Secret

And here's the `hooks.json` file:

```
$ cat hooks.json
[
  {
    "id": "deploy-myapp",
    "execute-command": "/somewhere/webhook/deploy.sh",
    "command-working-directory": "/somewhere/webhook",
    "pass-arguments-to-command":
    [
      { "source": "payload", "name": "head_commit.message" },
      { "source": "payload", "name": "pusher.name" },
      { "source": "payload", "name": "head_commit.id" }
    ],
    "trigger-rule":
    {
      "and":
      [
        {
          "match":
          {
            "type": "payload-hash-sha1",
            "secret": "yourGithubSecret",
            "parameter":
            {
              "source": "header",
              "name": "X-Hub-Signature"
            }
          }
        },
        {
          "match":
          {
            "type": "value",
            "value": "refs/heads/main",
            "parameter":
            {
              "source": "payload",
              "name": "ref"
            }
          }
        }
      ]
    }
  },
]
```

And here's my `deploy.sh` script:

```
$ cat deploy.sh
#! /bin/bash -e

PREFIX=/somewhere/webhook
GHRDIR=${PREFIX}/mytrilog
TMPFILE=${PREFIX}/debug.txt
DEPLOY=${PREFIX}/deployLocal

D=`date`
cat /dev/null > $TMPFILE
echo "---------------------------------" >> $TMPFILE
echo $D >> $TMPFILE
echo "---------------------------------" >> $TMPFILE

function cleanup {
     echo "Error occoured"
     # !!Placeholder for Slack notification
}
trap cleanup ERR

commit_message=$1   # head_commit.message
pusher_name=$2      # pusher.name
commit_id=$3        # head_commit.id

${PREFIX}/gitpull >> $TMPFILE 2>&1
# should do error checking???

echo "---------------------------------" >> $TMPFILE
echo "---------------------------------" >> $TMPFILE
$DEPLOY >> $TMPFILE
echo "---------------------------------" >> $TMPFILE
echo "---------------------------------" >> $TMPFILE
```

And finally, here's my `deployLocal` script, which copies everything
needed (and only what's needed) over to `/var/www/mytrilog`. It also
tries to start and stop the app as needed when upgrading.

```
$ cat deployLocal
#!/bin/bash

# deploy from /somewhere to /var/www

umask 0022

NAME=mytrilog
PREFIX=/somewhere/webhook
REPO=${PREFIX}/$NAME
WHERE=/var/www

if [ -d $REPO ] ; then
  cd $REPO
else
  echo "no $REPO directory???"
  exit 1
fi

# stop
supervisorctl stop $NAME

# copy files
rsync -aq --delete --exclude-from ${PREFIX}/sync-exclude ${REPO} $WHERE

# check for venv file
# make if it doesn't exist
if [ ! -d ${WHERE}/${NAME}/venv ] ; then
  cd ${WHERE}/${NAME}
  python3 -m venv venv
  # must be bash for source to work...
  source ./venv/bin/activate
  pip install -r ${REPO}/requirements.txt
  pip install gunicorn
  deactivate
fi

# check for .env file, cp in if it doesn't exist
if [ ! -e ${WHERE}/${NAME}/.env ] ; then
  cd ${WHERE}/${NAME}
  cp ${PREFIX}/.env .
fi

# apply db upgrades, if any
cd ${WHERE}/${NAME}
source ./venv/bin/activate
flask db upgrade
deactivate

# restart
supervisorctl start $NAME
```

The `sync-exclude` file just contains things I don't want copied into
`/var/www`, like the `.git` directory and this README.md file:

```
$ cat sync-exclude
sync-exclude
README.md
.git
.gitignore
venv
.env
logs
app.db
app/translations
screenshot.png
etc
tests.py
```

### static link

I had to make a link from my main website back to the mytrilog/app/static dir.
Not sure why.  Without that I couldn't get any static
content (css, images) to show up on the web app.

```
cd /var/www/mywebsite
ln -s /var/www/mytrilog/app/static/ static
```

### full install details

Put all the commands here. Use this for the Quickstart section.
Try it out on a test server and make sure it all works...


### stuff I always have to look up

#### manually delete entry from db

```
$ mysql -u appuser -p mytrilog
Enter password:  (see .env file)
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

MariaDB [mytrilog]> delete from `workout` where `id` = 121;
Query OK, 1 row affected (0.002 sec)

MariaDB [mytrilog]> Bye
```


### added Edit option

I added an Edit Workout option, for when I type in the wrong date or
wrong workout "what". Thanks to Randall Degges for this page and help with the
"edit" templates and links:
[https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python](https://developer.okta.com/blog/2018/07/23/build-a-simple-crud-app-with-flask-and-python)

### mail

Note: my server already had a working postfix install, so I just used that 
for the app's mail server. 

## run in docker container???

Assumes you already have docker set up and working on your
local workstation. Also only tried this on an ubuntu linux computer.

```
mkdir docker-mytrilog
cd docker-mytrilog
git clone git@github.com:jeffknerr/mytrilog.git
python3 -m venv venv
source ./venv/bin/activate
pip install -r mytrilog/requirements.txt
flask db upgrade
flask run
```

At this point you just have a version running at `localhost:5000/mytrilog`.

```
vim mytrilog/requirements.txt
# add line for gunicorn
vim Dockerfile
FROM python:3.8-slim
COPY ./mytrilog/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY ./mytrilog/ /mytrilog
WORKDIR /mytrilog
CMD ["gunicorn", "-w", "2", "-b", ":8080", "mytrilog:app"]
```

Now build the image and run the container.

```
docker build -t "mytrilog" .
docker run -d --name mytrilog -p 8080:8080 mytrilog
```

That should have a version running at `localhost:8080/mytrilog`.

Some useful commands if things don't work:

```
docker rm d0c<TAB>
docker rmi c89<TAB>
# attach to container
docker start -a 042678f863d5
docker logs c062aa32e33d
docker inspect c062aa32e33d
# get into the image to look around, run commands manually
docker run -it  --entrypoint /bin/bash mytrilog
```

## persist the db

First, change the `config.py` file to use the sqlite db from it's
own directory (I guess a docker volume has to be a directory, and
can't be a file?).

```
$ cat mytrilog/config.db
...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, './testdb/app.db')
...
```

and make that directory in the mytrilog source directory:

```
$ mkdir mytrilog/testdb
```

Now remake everything and attach the volume when you run the container:

```
$ docker stop mytrilog
$ docker rm aa0<TAB>
$ docker rmi 5b9<TAB>

$ docker volume create app-db
$ docker volume inspect app-db
$ docker volume ls
$ sudo ls -al /var/lib/docker/volumes/app-db
$ docker build -t "mytrilog" .

$ docker run -d --name mytrilog -p 8080:8080 -v app-db:/mytrilog/testdb mytrilog
$ docker run -it  --entrypoint /bin/bash mytrilog
$ docker ps
```

With the above you should be able to stop and start the container
(even remove it and make a new one) and any users or workouts you
added will still be there.


Still to do:
- add mysql in separate container
- set it all up with a docker compose file

