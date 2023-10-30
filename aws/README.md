
# create test VM using ansible and aws

Got some of this info from the terraform tutorials,
and some from this page:
https://www.kevinlondon.com/2016/09/20/devops-from-scratch-pt-2

Prerequisites (and versions used here):
- running these commands on ubuntu 22.04
- have vagrant installed (v2.3.4)
- have terraform installed (v1.4.5)
- have ansible installed (v8.5.0)
- have aws cli installed (v2.11.11)
- have ssh key for aws already set up
- have aws keys already set up and in ~/.aws files

## set up terraform files

Change your default region and public_key_path to whatever you need:

```
$ mkdir terraform
$ cd terraform
$ vim variables.tf
# These variables come from the terraform.tfvars file
variable "aws_access_key" {}
variable "aws_secret_key" {}

variable "aws_region" {
    description = "AWS region for launch."
    default = "us-east-1"
}

variable "public_key_path" {
    default = "~/.ssh/jeffnotrootTF.pem"
}
$ cat ~/.aws/credentials > terraform.tfvars
$ vim terraform.tfvars
aws_access_key = "AK_your_access_key_here"
aws_secret_key = "dkejlrjkl+_your_aws_secret_key_here"
```

Now set up `main.tf` to install a web server.
Change the ami variable to one that's available in your region.

```
$ cat main.tf
provider "aws" {
    access_key = "${var.aws_access_key}"
    secret_key = "${var.aws_secret_key}"
    region = "${var.aws_region}"
}

resource "aws_instance" "ansible_test" {
# us-east-2
#   ami = "ami-08eda224ab7296253"  
#   instance_type = "t2.micro"
# us-east-1
  ami                    = "ami-06db4d78cb1d3bbf9"
  instance_type          = "t2.micro"
    vpc_security_group_ids = ["${aws_security_group.web.id}"]
    key_name = "jeffnotrootTF"
}

resource "aws_security_group" "web" {
    name = "web"
    description = "Allow HTTP/S and SSH connections."

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
```

And finally, create the server:

```
$ terraform init
$ terraform plan
$ terraform apply
$ vim output.tf
output "ip" {
    value = "${aws_instance.ansible_test.public_ip}"
}
$ terraform output
```

The above should create an EC2 instance, which you can view in your
aws dashboard. The `output.tf` file just shows how to get the public
IP of the instance (to be used in ansible hosts file below).

## run ansible to configure server

```
$ cd ..
$ vim ansible.cfg
[defaults]
remote_user = admin
private_key_file = ~/.ssh/jeffnotrootTF.pem
nocows = 1

[ssh_connection]
pipelining = True
$ sudo vim  /etc/ansible/hosts
[awsinstance]
18.222.51.158
$ ansible-playbook  playbook.yml
```

That should run all the ansible tasks, reulting in a server
running the flask app (using nginx, gunicorn, and supervisor)
that uses a mysql/mariadb database.
The server has a self-signed
SSL cert, so it works with https, but you have to ignore
the browser warnings and "proceed to the site". In this
case (for IP 18.222.51.158) you can access the flask app
at https://18.222.51.158/mytrilog (ignore the scary browser warnings).

I did all of this on an Ubuntu 22.04 (jammy) workstation, 
with 32GB of memory, starting in June 2023. 

Copied/stolen/modified from 
[Jeff Geerling's *ansible-for-devops* repo](https://github.com/geerlingguy/ansible-for-devops/blob/master/drupal/provisioning/playbook.yml)

## when finished

```
$ cd terraform
$ terraform destroy
```

## todo

- get the IP and immediately run the playbook, all from terraform...
