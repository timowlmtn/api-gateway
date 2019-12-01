deploy:
	aws cloudformation --profile ${AWS_PROFILE} package --template-file src/lambda/template.yml \
	    --s3-bucket ${S3_STAGE_BUCKET} --output-template-file src/lambda/packaged-template.yaml
	aws cloudformation --profile ${AWS_PROFILE} deploy --template-file src/lambda/packaged-template.yaml \
	    --stack-name ${STACK_NAME}${COLOR} \
	    --parameter-overrides VPC="${VPC_ID}" SecurityGroupIds="${LAMBDA_SECURITY_GROUP}" \
	        VpcSubnetIds="${SUBNET_IDS}" Environment="${ENVIRONMENT}" \
	    --capabilities CAPABILITY_NAMED_IAM

deploy-lambda-layer:
	aws lambda update-function-configuration --function-name ${STACK_NAME}${COLOR}-ParseFilename-18SUBXL65NMPJ \
        --layers

test-api:
	curl -H "X-API-KEY: ${X_API_KEY}" https://${API_ID}.execute-api.us-east-1.amazonaws.com/Prod/parse_filename?Path="api-gateway/tests/data/apple_health_tracking_201911231045steps.csv"

clean:
	aws --profile ${AWS_PROFILE} cloudformation delete-stack --stack-name ${STACK_NAME}${COLOR}

init:
	pip3 install -r requirements.txt

test:
	py.test tests


deploy-layer:
	src/tools/deploy_lambda.py --profile ${AWS_PROFILE} --layer_name api_layer --build_lambda_zip --deploy_lambda_aws \
	    --s3_bucket ${S3_STAGE_BUCKET} --debug T
