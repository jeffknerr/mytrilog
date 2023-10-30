output "ip" {
    value = "${aws_instance.ansible_test.public_ip}"
}
