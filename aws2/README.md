
# create test VMs using ansible, terraform, aws

This one is similar to the aws directory information (in this repo),
but creating two VMs and putting db on one, flask app on the other.

Got some of this info from the terraform tutorials,
and some from this page:
https://www.kevinlondon.com/2016/09/20/devops-from-scratch-pt-2

Prerequisites (and versions used here):
- running these commands on ubuntu 22.04
- have vagrant installed (v2.4.0)
- have terraform installed (v1.6.2)
- have ansible installed (v2.14.5)
- have aws cli installed (v2.13.30)
- have ssh key for aws already set up
- have aws keys already set up and in ~/.aws files

Some details of these installs are at the end of this readme...


## set up terraform files

NOTE: I think this is the "not recommended" and klunky way to do this.
This page says "provisioners are a last resort":
https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax

Once I get this working (just to see how it does), I'll try the
other method (create an image with Packer)...


In `variables.tf`, change your default region and public_key_path to whatever you need:

```
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
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.aws_region
}

resource "aws_security_group" "web" {
  name        = "web"
  description = "Allow HTTP/S and SSH connections."

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "ansible_test" {
  ami                    = "ami-06db4d78cb1d3bbf9"
  instance_type          = "t2.micro"
  vpc_security_group_ids = ["${aws_security_group.web.id}"]
  key_name               = "jeffnotrootTF"

  associate_public_ip_address = true
  tags = {
    Name    = "demo"
    Ansible = "true"
  }

  provisioner "local-exec" {
    command = "echo [awsinstance] > ./inventory"
  }
  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> ./inventory"
  }
# pause to make sure remote instance is up...
  provisioner "local-exec" {
    command = "sleep 60"
  }
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ./inventory ./playbook.yml"
  }
}

output "ip" {
  value = aws_instance.ansible_test.public_ip
}

output "website_url" {
  value = "https://${aws_instance.ansible_test.public_ip}/mytrilog"
}
```

And finally, create the server (and run ansible):

```
$ terraform init
$ terraform plan
$ terraform apply
```

The above should create an EC2 instance, then run the ansible playbook.
It uses the klunky "local-exec" lines to write an "inventory" file for
use with the playbook. In the end, you should see the public ip address
of your instance:

```
$ terraform apply
...
...
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

ip = "3.88.199.94"
website_url = "https://3.88.199.94/mytrilog"
```

The server has a self-signed
SSL cert, so it works with https, but you have to ignore
the browser warnings and "proceed to the site" (i.e., click
through the browser warnings). 

I did all of this on an Ubuntu 22.04 (jammy) workstation, 
with 32GB of memory, starting in June 2023. 

Copied/stolen/modified from 
[Jeff Geerling's *ansible-for-devops* repo](https://github.com/geerlingguy/ansible-for-devops/blob/master/drupal/provisioning/playbook.yml)

## when finished

```
$ terraform destroy
```

## software installation details

### vagrant

```
$ wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
$ echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
$ sudo apt update && sudo apt install vagrant
$ vagrant --version
Vagrant 2.4.0
```

### terraform

As both vagrant and terraform are from hashicorp, the above allows you
to install terraform, too:

```
$ sudo apt install terraform
$ terraform --version
Terraform v1.6.2
```

### ansible

```
$ sudo add-apt-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible
$ ansible --version
ansible [core 2.14.5]
  config file = /home/knerr/repos/mytrilog/separate-aws/ansible.cfg
  configured module search path = ['/home/knerr/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/knerr/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] (/usr/bin/python3)
  jinja version = 3.0.3
  libyaml = True
```

### aws cli

```
$ cd
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ cd aws
$ sudo ./install
$ aws --version
aws-cli/2.13.30 Python/3.11.6 Linux/6.2.0-34-generic exe/x86_64.ubuntu.22 prompt/off
```

Also need to set up your credentials. I think this is the page
I followed to do that:

https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-user.html

with something like this example:

```
aws configure --profile your_username
AWS Access Key ID [None]: your_access_key
AWS Secret Access Key [None]: your_secret_access_key
Default region name [None]: us-east-1
Default output format [None]: json
```

Look under your account/Security Credentials for how to create the Access Keys.

And look under Computer/EC2/Key pairs for how to view/create an ssh key pair.
