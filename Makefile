init:
	pip3 install -r requirements.txt

test:
	py.test tests

deploy-lambda:
	src/tools/deploy_lambda.py --profile owlmtn --layer_name api_layer --build_lambda_zip --deploy_lambda_aws --s3_bucket owlmtn-lambda-deploy --debug T
