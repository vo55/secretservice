import os

def set_aws_profile(profile):
    """
    Sets the aws profile through environment parameters boto3 will be checking
    :param profile: the aws profile
    :return: None
    """
    os.environ['AWS_PROFILE'] = profile
