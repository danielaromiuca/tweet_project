#!/bin/bash
yum update 
yum install -y ruby
yum install git -y
yum install amazon-cloudwatch-agent -y
amazon-linux-extras enable python3.8 -y
yum install python3.8 -y
pip3 install poetry


cd /home/ec2-user
mkdir logs
chmod 777 logs

git clone https://github.com/danielaromiuca/tweet_project.git
chmod -R 777 tweet_project
cd tweet_project
poetry install

aws configure set region us-east-1
export API_ACCESS_TOKEN=$(aws ssm get-parameter --name "api_access_token" --output text --query Parameter.Value)
export API_ACCESS_TOKEN_SECRET=$(aws ssm get-parameter --name "api_access_token_secret" --output text --query Parameter.Value)
export API_CONSUMER_SECRET=$(aws ssm get-parameter --name "api_consumer_secret" --output text --query Parameter.Value)
export API_CONSUMER_KEY=$(aws ssm get-parameter --name "api_consumer_key" --output text --query Parameter.Value)

poetry run supervisord -c /home/ec2-user/tweet_project/supervisord.conf
sleep 5

/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/home/ec2-user/tweet_project/cwagentconfig.json -s