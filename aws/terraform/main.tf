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
