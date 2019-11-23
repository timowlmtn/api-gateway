# Library Contains Startup Code for Building an API Gateway

## Notes

### Setup for Windows paramiko

The following errors can be resolved by re-installing py-bcrypt and pynacl respecitvely.

    ModuleNotFoundError: No module named 'nacl._sodium'
or 
    ImportError: cannot import name '_bcrypt' from 'bcrypt'
 
pip install pynacl

### Setup for the EC2 Client

The purpose of the EC2 instance is to provide a build environment that is compatible with the Lambda runtime 
environment for compiling the libraries.

This code assumes the EC2 client has been set up with the appropriate software.  You will need to create an 
EC2 instance.

 sudo apt update
 sudo apt install python3-pip
 sudo apt install awscli
 sudo apt-get install zip unzip
 aws configure