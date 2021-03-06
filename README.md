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
