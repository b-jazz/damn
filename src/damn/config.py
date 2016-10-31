import configparser
import os.path

class Config(object):
    def __init__(self):
        """Read in the default config file if it exists."""
        self.config = configparser.ConfigParser()
        self.config.read_file(open(os.path.expanduser('~/.damnrc')))

    @property
    def dam_id(self):
        return self.config.get('dam', 'dam_id', fallback='09421500')

    @property
    def app_token(self):
        return self.config.get('pushover', 'app_token')

    @property
    def user_id(self):
        return self.config.get('pushover', 'user_id')

    @property
    def last_discharge_amount(self):
        lda = self.config.get('alert_levels', 'last_discharge_amount', fallback='1000')
        return int(lda)
