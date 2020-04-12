from datetime import datetime, timedelta
import pytz
utc = pytz.UTC

def check_old_secrets(logger, secrets, output):
    max_age_in_days = utc.localize(datetime.now() - timedelta(days=90))
    logger.debug('Checking for se')
    for secret in secrets:
        if secret['LastRotated'] < max_age_in_days:
            output.put_offender(resource_id=secret['ID'],
                                reason='Secret is old and should be rotated. Age: {} days'.format((utc.localize(datetime.now()) - secret['LastRotated']).days))
