import os
import boto3
import sys


def set_aws_profile(profile):
    """
    Sets the aws profile through environment parameters boto3 will be checking
    :param profile: the aws profile
    :return: None
    """
    os.environ['AWS_PROFILE'] = profile


def get_secrets_metadata():
    secrets = get_encrypted_parameters() + get_secretsmanager_secrets() + get_iam_access_keys()
    pass


def get_encrypted_parameters(logger):
    logger.debug('Getting ssm SecureString Meta Information')
    securestrings = []
    ssm = boto3.client("ssm")

    paginator = ssm.get_paginator('describe_parameters')
    operation_parameters = {'Filters': [
        {'Key': 'Type', 'Values': ['SecureString']}
    ]}
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        securestrings = securestrings + page['Parameters']
    logger.debug('Gathered securestrings: {}'.format(str(securestrings)))

def get_secretsmanager_secrets():
    pass


def get_iam_access_keys():
    pass
