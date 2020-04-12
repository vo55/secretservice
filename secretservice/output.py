class Output():
    def __init__(self, logger):
        self.offenders = []
        self.logger = logger

    def put_offender(self, resource_id, reason):
        self.offenders.append({'Resource': resource_id, 'Reason': reason})

    def list_results(self):
        for offender in self.offenders:
            self.logger.info(offender['Reason'] + " --- " + offender['Resource'])
        if len(self.offenders) == 0:
            self.logger.info('No offenders found')