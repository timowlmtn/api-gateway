#!/usr/bin/env python
import argparse
import boto3
import os
import paramiko
import scp
import sys


def call_command_list(ssh_client, commands_list, args):
    """
    Call all the commands remotely in the list
    :param ssh_client:
    :param commands_list:
    :param args:
    :return:
    """
    for command in commands_list:
        if args.debug:
            print(command)

        stdin, stdout, stderr = ssh_client.exec_command(command)
        if args.debug:
            print(f"STDOUT: {stdout.read()}")

        stderr_out = stderr.read()
        if args.debug or len(stderr_out) > 0:
            print(f"STDERR: {stderr_out}")


def build_lambda_zip(args, ssh_client, layer_name):
    """
    Deploy the lambda to the ssh client
    :param args:
    :param ssh_client:
    :param layer_name:
    :return:
    """
    setup_commands = (
        f"rm -rf {layer_name}_deploy",
        f"mkdir -p  {layer_name}_deploy/python/lib/python3.6/site-packages/{layer_name}"
    )

    call_command_list(ssh_client, setup_commands, args)

    scp_client = scp.SCPClient(ssh_client.get_transport())
    scp_client.put(f"./src/{layer_name}",
                   recursive=True,
                   remote_path=f"{layer_name}_deploy/python/lib/python3.6/site-packages/")

    deploy_commands = (
        f"rm -rf {layer_name}_deploy/python/lib/python3.6/site-packages/{layer_name}/__pycache__",
        f"python3 -m compileall {layer_name}_deploy/python/lib/python3.6/site-packages/{layer_name}/",
        f"ls {layer_name}_deploy/python/lib/python3.6/site-packages/{layer_name}/__pycache__",
        f"cd {layer_name}_deploy; zip -r {layer_name}.zip .",
        f"aws s3 cp {layer_name}_deploy/{layer_name}.zip s3://{args.s3_bucket}"
    )

    call_command_list(ssh_client, deploy_commands, args)


def deploy_lambda_aws(args, lambda_client):
    """

    :param args:
    :param lambda_client:
    :return:
    """
    response = lambda_client.publish_layer_version(
        LayerName=args.layer_name,
        Description=args.layer_description,
        Content={
            'S3Bucket': args.s3_bucket,
            'S3Key': f"{args.layer_name}.zip"
        },
        CompatibleRuntimes=[
           'python3.6', 'python3.7', 'python3.8',
        ]
    )

    if args.debug:
        print(response)


def main(argv):
    parser = argparse.ArgumentParser(description='Create a mapping of the dependencies based on a user input.')

    parser.add_argument('--hostname',
                        default=os.getenv("EC2_HOST"),
                        help="EC2 Hostname (ec2-33-44-127-230.us-east-2.compute.amazonaws.com)")

    parser.add_argument("--username",
                        default=os.getenv("EC2_USER"),
                        help="User name")

    parser.add_argument("--pem_file",
                        default=os.getenv("EC2_PEM"),
                        help="User name")

    parser.add_argument("--profile",
                        default=None,
                        help="AWS Profile from ~/.aws/credentials file")

    parser.add_argument("--layer_name",
                        required=True,
                        help="Specify a layer name to deploy")

    parser.add_argument("--layer_description",
                        default="A default API layer",
                        help="A description of the layer")

    parser.add_argument("--s3_bucket",
                        required=True,
                        help="Specify a layer name to deploy")

    parser.add_argument('--build_lambda_zip', action="store_true",
                        help="Build the Lambda zip file")

    parser.add_argument('--deploy_lambda_aws', action="store_true",
                        help="Deploy the lambda function")

    parser.add_argument("--debug", help="Optional debug flag")

    args = parser.parse_args()

    if args.build_lambda_zip:
        hostname = args.hostname
        username = args.username
        pem_file = args.pem_file
        if args.debug:
            print(f"Connecting to {hostname} with {username} using {pem_file}")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, username=username, key_filename=pem_file)

        build_lambda_zip(args, ssh_client, args.layer_name)

    if args.deploy_lambda_aws:
        session = boto3.Session(profile_name=args.profile)
        lambda_client = session.client('lambda')
        deploy_lambda_aws(args, lambda_client)


if __name__ == "__main__":
    main(sys.argv)

