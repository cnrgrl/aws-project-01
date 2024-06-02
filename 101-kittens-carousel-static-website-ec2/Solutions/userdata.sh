#!/bin/bash

# Update and install httpd
sudo dnf update -y && sudo dnf install httpd -y

# Define the folder and change directory
folder="https://raw.githubusercontent.com/awsdevopsteam/101-cfn-static-web
   -ec2/master/static-web"
cd /var/www/html || exit

# Download the files using wget
sudo wget ${folder}/index.html
sudo wget ${folder}/cat0.jpg
sudo wget ${folder}/cat1.jpg
sudo wget ${folder}/cat2.jpg
sudo wget ${folder}/cat3.png

# Start and enable httpd service
sudo systemctl start httpd
sudo systemctl enable httpd
