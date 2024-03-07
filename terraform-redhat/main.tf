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
  ami                    = "ami-0fe630eb857a6ec83"
  # redhat ami
  instance_type          = "t2.micro"
  vpc_security_group_ids = ["${aws_security_group.web.id}"]
  key_name               = "jeffnotrootTF"

  associate_public_ip_address = true
  tags = {
    Name    = "redhat-nginx-flask-demo"
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
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ./inventory ./redhat-playbook.yml"
  }
}

output "ip" {
  value = aws_instance.ansible_test.public_ip
}

output "website_url" {
  value = "https://${aws_instance.ansible_test.public_ip}/mytrilog"
}
