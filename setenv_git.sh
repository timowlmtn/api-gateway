# Specify your Python script here
export PATH=/c/Program\ Files/Python37:/c/Program\ Files/Python37/scripts:$PATH

# Specify the EC2 information
export EC2_HOST="See https://console.aws.amazon.com/ec2/home?region=us-east-1#"
export EC2_PEM="owlmtn-us-east-1.pem"
export EC2_USER=ubuntu

export ENVIRONMENT=DEV
export COLOR=Green

alias set_blue="export COLOR=Blue"
alias set_green="export COLOR=Green"


export S3_STAGE_BUCKET="owlmtn-lambda-deploy"

export AWS_PROFILE="owlmtn"

export VPC_ID="See https://console.aws.amazon.com/vpc/home?region=us-east-1#vpcs:sort=VpcId"
export SUBNET_IDS="See https://console.aws.amazon.com/vpc/home?region=us-east-1#subnets:sort=SubnetId"
export LAMBDA_SECURITY_GROUP="See https://console.aws.amazon.com/vpc/home?region=us-east-1#SecurityGroups:sort=groupId"
export ENVIRONMENT="Dev"

export X_API_KEY="See https://console.aws.amazon.com/apigateway/home?region=us-east-1#/api-keys"
export API_ID="See https://console.aws.amazon.com/apigateway/main/apis?region=us-east-1"


export STACK_NAME="FileImport"