
# create test VM using ansible and vagrant

Below is a way to run a test server of this flask app,
if you just want to try it out. It should install a VM
that runs the flask app and a mysql/mariadb database, and
uses nginx to server the app. The server has a self-signed
SSL cert, so it works with https, but you have to ignore
the browser warnings and "proceed to the site"...

Copied/stolen/modified from 
[Jeff Geerling's *ansible-for-devops* repo](https://github.com/geerlingguy/ansible-for-devops/blob/master/drupal/provisioning/playbook.yml)

## install vagrant and ansible

I did all of this on an Ubuntu 22.04 (jammy) workstation, 
with 32GB of memory, starting in June 2023. Software
versions:

```
ii  ansible 7.6.0-1ppa~jammy
ii  vagrant 2.3.4  
```

The following should set up vagrant and ansible Ubuntu.
After this you can use vagrant to bring up the flask server.

```
$ sudo apt-add-repository -y ppa:ansible/ansible
$ sudo apt-get update
$ sudo apt-get install gnupg software-properties-common 
$ sudo apt-get install ansible vagrant git virtualbox
$ sudo vim /etc/ansible/hosts
$ cat /etc/ansible/hosts
$ vim edit /etc/ansible/hosts
[flask]
192.168.56.10

[serv:children]
flask

[serv:vars]
ansible_user=vagrant
ansible_ssh_private_key_file=~/.vagrant.d/insecure_private_key
$ alias vg=vagrant
$ export ANSIBLE_NOCOWS=1
```

## vagrant up the flask server

```
$ git clone https://github.com/jeffknerr/mytrilog.git
$ cd mytrilog
$ cd vagrant
$ alias vg=vagrant
$ export ANSIBLE_NOCOWS=1
$ vg up
$ vg status
$ vg ssh flask
flask$ ps -ef | grep guni
```

Simple test from workstation, seeing if flask app is up:

```
$ links https://192.168.56.10/mytrilog
(Yes...connect to it anyway)
```

## try the playbook on it's own

Sometimes you don't want to redo the whole vm. You can edit the
playbook and then just rerun the playbook with this:

```
$ vim playbook.yml
$ export ANSIBLE_NOCOWS=1
# sometimes need to reaccept the ssh host key
$ ssh-keygen -f "~/.ssh/known_hosts" -R "192.168.56.10"
$ ssh -i ~/.vagrant.d/insecure_private_key vagrant@192.168.56.10
The authenticity of host '192.168.56.10 (192.168.56.10)' can't be established.
ED25519 key fingerprint is SHA256:4llg+iUcjtWrkdGNStA5B+25by9LrMSCo+2byRcKWtY.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.56.10' (ED25519) to the list of known hosts.
Last login: Wed Jun 21 15:05:26 2023 from 10.0.2.2
vagrant@flask:~$ exit
Connection to 192.168.56.10 closed.
$ ansible flask -a date
$ ansible-playbook playbook.yml
```


## redo it all

If you want to start with a fresh copy...

```
vg halt flask
vg destroy flask
$ export ANSIBLE_NOCOWS=1
vg up
```

## play with the db

After the app was up and running, I registered a new user (Sammy)
and logged two workouts. Here's how to look in the db to see
the results:

```
$ vg ssh flask
Last login: Wed Jun 21 15:32:32 2023 from 192.168.56.1
vagrant@flask:~$ sudo mysql
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 37
Server version: 10.5.19-MariaDB-0+deb11u2 Debian 11

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| mytrilog           |
| performance_schema |
+--------------------+
4 rows in set (0.011 sec)

MariaDB [(none)]> use mytrilog;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [mytrilog]> show tables;
+--------------------+
| Tables_in_mytrilog |
+--------------------+
| alembic_version    |
| followers          |
| user               |
| workout            |
+--------------------+
4 rows in set (0.001 sec)

MariaDB [mytrilog]> select * from user;
+----+----------+----------------------+--------------------------------------------------------------------------------------------------------+----------+---------------------+
| id | username | email                | password_hash                                                                                          | about_me | last_seen           |
+----+----------+----------------------+--------------------------------------------------------------------------------------------------------+----------+---------------------+
|  1 | Sammy    | jk@cs.swarthmore.edu | pbkdf2:sha256:600000$1dw0kK5Yh048lIuH$55c043789c133a103e763b14c5747197d1e95306d259f2b23223be99a685961d | NULL     | 2023-06-21 15:48:04 |
+----+----------+----------------------+--------------------------------------------------------------------------------------------------------+----------+---------------------+
1 row in set (0.001 sec)

MariaDB [mytrilog]> select * from workout;
+----+------+---------------------+--------+--------+------+-----------------+
| id | what | when                | amount | weight | who  | comment         |
+----+------+---------------------+--------+--------+------+-----------------+
|  1 | swim | 2023-06-21 00:00:00 |     10 |     65 |    1 | in creek        |
|  2 | run  | 2023-06-18 00:00:00 |     28 |   NULL |    1 | down the street |
+----+------+---------------------+--------+--------+------+-----------------+
2 rows in set (0.001 sec)

MariaDB [mytrilog]>
```
