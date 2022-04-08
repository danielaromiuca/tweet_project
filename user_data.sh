#!/bin/bash
sudo yum update 
sudo yum install -y ruby
sudo yum install git -y
yum install amazon-cloudwatch-agent -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip3 install poetry
cd /home/ec2-user
git clone https://github.com/danielaromiuca/tweet_project.git
chmod -R 777 tweet_project
cd tweet/tweet_project
poetry install
get_credentials.sh
/usr/local/bin/supervisord  -c /home/ec2-user/tweet_project/supervisord.conf
sleep 5
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/home/ec2-user/tweet_project/cwagentconfig.json -s 