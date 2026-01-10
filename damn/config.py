import configparser
import logging
import os.path

class Config(object):
    def __init__(self):
        """Read in the default config file if it exists."""
        self.log = logging.getLogger(__name__)
        self.config = configparser.ConfigParser()
        self.config_filename = os.path.expanduser('~/.damnrc')
        with open(self.config_filename, 'r') as cf_fp:
            self.config.read_file(cf_fp)

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
    def next_discharge_amount(self):
        lda = self.config.get('alert_levels', 'next_discharge_amount', fallback='1000')
        return int(lda)

    @property
    def discharge_every(self):
        discharge_every = self.config.get('alert_levels', 'discharge_every', fallback='1000')
        return int(discharge_every)

    @next_discharge_amount.setter
    def next_discharge_amount(self, value):
        self.config.set('alert_levels', 'next_discharge_amount', str(value))
        # open the config file
        with open(self.config_filename, 'w') as cf_fp:
            # write out the new config
            self.config.write(cf_fp)
            self.log.debug('New config file written to disk.')
