from datetime import datetime, timedelta
import pytz

utc = pytz.UTC


def check_old_secrets(logger, secrets, output):
    max_age_in_days = utc.localize(datetime.now() - timedelta(days=90))
    logger.debug('Executing Rule old secrets')
    for secret in secrets:
        if secret['LastRotated'] < max_age_in_days:
            output.put_offender(resource_id=secret['ID'],
                                reason='{} is old and should be rotated. Age: {} days'.format(secret['Type'], (
                                            utc.localize(datetime.now()) - secret['LastRotated']).days))


def check_weak_secrets(logger, secrets, output):
    pass


def check_unused_secrets(logger, secrets, output):
    max_unused = utc.localize(datetime.now() - timedelta(days=30))
    for secret in secrets:
        if 'LastUsed' in secret.keys() and secret['LastUsed'] < max_unused:
            output.put_offender(resource_id=secret['ID'],
                                reason='{} is unused and should be deleted. Unused for: {} days'.format(secret['Type'], (
                                        utc.localize(datetime.now()) - secret['LastRotated']).days))


def check_all_rules(logger, secrets, output):
    check_old_secrets(logger, secrets, output)
    check_weak_secrets(logger, secrets, output)
    check_unused_secrets(logger, secrets, output)
