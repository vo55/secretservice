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

def get_secrets_metadata(logger):
    secrets = get_encrypted_parameters(logger) + get_secretsmanager_secrets(logger) + get_iam_access_keys()
    logger.debug('Found {} secrets'.format(str(len(secrets))))
    return secrets


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
    return normalize_ssm_secrets(securestrings)


def get_secretsmanager_secrets(logger):
    logger.debug('Getting SecretsManager secrets Meta Information')
    secrets = []
    ssm = boto3.client("secretsmanager")

    paginator = ssm.get_paginator('list_secrets')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        secrets = secrets + page['SecretList']
    logger.debug('Gathered secretsmanager secrets: {}'.format(str(secrets)))
    return normalize_secretsmanager_secrets(secrets)


def get_iam_access_keys():
    # Todo
    return []

def normalize_ssm_secrets(secrets):
    normalized_secrets = []
    for secret in secrets:
        normalized_secrets.append({'ID': secret['Name'], 'LastRotated': secret['LastModifiedDate']})
    return normalized_secrets

def normalize_secretsmanager_secrets(secrets):
    normalized_secrets = []
    for secret in secrets:
        normalized_secrets.append({'ID': secret['ARN'], 'LastRotated': secret['LastChangedDate']})
    return normalized_secrets