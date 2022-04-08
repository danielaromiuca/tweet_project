#! bin/bash
export API_ACCESS_TOKEN=$(aws ssm get-parameter --name "api_access_token" --output text --query Parameter.Value)
export API_ACCESS_TOKEN_SECRET=$(aws ssm get-parameter --name "api_access_token_secret" --output text --query Parameter.Value)
export API_CONSUMER_SECRET=$(aws ssm get-parameter --name "api_consumer_secret" --output text --query Parameter.Value)
export API_CONSUMER_KEY=$(aws ssm get-parameter --name "api_consumer_key" --output text --query Parameter.Value)
