from secretservice.boto_wrapper import *
from secretservice.rule_engine import *
from secretservice.output import *

class SecretService:
    def __init__(self, logger):
        self.logger = logger
        self.output = Output(self.logger)

    def benchmark(self):
        secrets = get_secrets_metadata(self.logger)
        check_old_secrets(logger=self.logger, secrets=secrets, output=self.output)
        self.output.list_results()