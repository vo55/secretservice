from secretservice.boto_wrapper import *

class SecretService:
    def __init__(self, logger):
        #dosomething
        self.logger = logger

    def benchmark(self):
        get_encrypted_parameters(self.logger)