
# create test redhat VM using ansible, terraform, aws

This one is similar to the aws directory information (in this repo),
but creating a *redhat* VM with db and flask app.

## overview

Using `terraform`, this will create a redhat ec2 instance, using 
an existing ssh key for access, then run an ansible playbook to 
configure the instance and set up the db and flask app. The flask app
is started using systemd, and is served with gunicorn and nginx.

## quickstart (see below for details)

### change ssh key 

Look for the "jeffnotroot" ssh key in the repo files.
You should change all to use your own ssh key. Here are 
the files to change:

- main.tf (jeffnotrootTF)
- ansible.cfg (jeffnotrootTF.pem)
- variables.tf (jeffnotrootTF.pem)

### edit register.yml

Add your redhat developer username and password to a `register.yml` file,
which should look like this:

```
---
# redhat register variables
redhat_username: 'your_user_name'
redhat_password: 'your_password'
...
```

### edit recaptcha.yml

Add your pub and private recaptcha keys to a `recaptcha.yml` file,
which should look something like this:

```
---
# recaptcha variables
recaptcha_pubkey: 'long pubkey here'
recaptcha_privkey: 'long private key here'
...
```

### terraform.tfvars file

This needs to hold copies of your aws keys.
Here's what it should look like:

```
aws_access_key = "your_access_key"
aws_secret_key = "your_secret_key"
```

### run terraform

Run the terraform commands to create the instance and run the ansible playbook:

```
terraform init
terraform plan
terraform apply
```

If all goes well, you should see the IP address of the ec2 instance at the end.

If the instance is created, but the playbook fails, you can fix/rerun the playbook
by putting the IP address in the `inventory` file, like this:

```
[awsinstance]
your.ip.address.here
```

Then run `ansible-playbook -i inventory redhat-playbook.yml`


## notes from above and more details

#### redhat

You can register as a redhat developer and use this page to manage
which instances are registered to your account:

https://access.redhat.com/management/systems

Not sure if you need to do that or not, but without it yum complains
when you try to add packages to your instance.

#### recaptcha

Here's the google recaptcha admin page:

https://www.google.com/recaptcha/admin

And this is the page I followed to set that up:

https://pusher.com/tutorials/google-recaptcha-flask/#register-for-google-recaptcha

If you see an error on the recaptcha (invalid site), go to your
key admin page, click Settings, and add the IP address of the ec2 instance
to your recaptcha key.

#### etc

And all of this assumes you already have an aws account, the aws cli
installed and your credentials set up...
