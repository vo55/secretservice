import os
import boto3


def set_aws_profile(profile):
    """
    Sets the aws profile through environment parameters boto3 will be checking
    :param profile: the aws profile
    :return: None
    """
    os.environ['AWS_PROFILE'] = profile

def get_secrets_metadata(logger):
    secrets = get_iam_access_keys(logger)
    regions = get_regions(logger)
    logger.info('Iterating through regions - this may take a while')
    for region in regions:
        try:
            logger.debug('Gathering information for {}'.format(region))
            secrets += get_encrypted_parameters(region) + get_secretsmanager_secrets(region)
        except:  # TODO Check if region is disabled
            pass
    logger.debug('Found {} secrets'.format(str(len(secrets))))
    return secrets


def get_regions(logger):
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    logger.debug('Available Regions: {}'.format(str(regions)))
    return regions


def get_encrypted_parameters(region):
    securestrings = []
    ssm = boto3.client("ssm", region_name=region)

    paginator = ssm.get_paginator('describe_parameters')
    operation_parameters = {'Filters': [
        {'Key': 'Type', 'Values': ['SecureString']}
    ]}
    page_iterator = paginator.paginate(**operation_parameters)
    for page in page_iterator:
        securestrings = securestrings + page['Parameters']
    return normalize_ssm_secrets(securestrings)


def get_secretsmanager_secrets(region):
    secrets = []
    ssm = boto3.client("secretsmanager", region_name=region)

    paginator = ssm.get_paginator('list_secrets')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        secrets = secrets + page['SecretList']
    return normalize_secretsmanager_secrets(secrets)


def get_iam_access_keys(logger):
    access_keys = []
    client = boto3.client('iam')
    for user in get_users(logger):
        metadata = client.list_access_keys(UserName=user['UserName'])
        if metadata['AccessKeyMetadata']:
            for key in metadata ['AccessKeyMetadata']:
                key['Id'] = user['UserName'] + '/' + key['AccessKeyId']
                access_keys.append(key)
    logger.debug('Gathered Access Key Metadata: {}'.format(str(access_keys)))
    return normalize_access_keys(access_keys, client)

def get_users(logger):
    logger.debug('Getting list of users')
    users = []
    iam = boto3.client("iam")

    paginator = iam.get_paginator('list_users')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        users = users + page['Users']
    logger.debug('Gathered all users: {}'.format(str(users)))
    return users


def normalize_ssm_secrets(secrets):
    # LastUsed not set bc not available in ssm
    normalized_secrets = []
    for secret in secrets:
        normalized_secrets.append({'ID': secret['Name'], 'LastRotated': secret['LastModifiedDate'], 'Type': 'SecureString'})
    return normalized_secrets

def normalize_secretsmanager_secrets(secrets):
    normalized_secrets = []
    for secret in secrets:
        normalized_secrets.append({'ID': secret['ARN'], 'LastRotated': secret['LastChangedDate'],
                                   'LastUsed': secret['LastAccessedDate'], 'Type': 'Secretsmanager Secret'})
    return normalized_secrets

def normalize_access_keys(secrets, client):
    normalized_secrets = []
    for key in secrets:
        if key['Status'] == "Active":  # ignore inactive keys for now
            normalized_secrets.append({'ID': key['Id'], 'LastRotated': key['CreateDate'],
                                       'LastUsed': client.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])['AccessKeyLastUsed']['LastUsedDate'],
                                       'Type': 'AccessKey'})
    return normalized_secrets