
import logging
import re

import click
import requests

from . import config
from . import usgs


def send_alert(message, token, user):
    post_data = {'token': token,
                 'user': user,
                 'message': message}

    logging.debug('post data: {0}'.format(post_data))

    pushover_url = 'https://api.pushover.net:443/1/messages.json'

    push_result = requests.post(pushover_url, post_data)
    if push_result.ok:
        print('yes')
    else:
        print(push_result.reason, push_result.text)


class DamnApp(object):
    def __init__(self, debug):
        """App Object. This controls everything."""
        self.setup_logging(debug)
        self.config = config.Config()
        self.usgs = usgs.USGS(self.config.dam_id)

        self.log.debug('app token: {0}'.format(self.config.app_token))
        self.log.debug('user id: {0}'.format(self.config.user_id))

    def setup_logging(self, debug):
        log_format = '%(asctime)s {0}'.format(logging.BASIC_FORMAT)
        if debug:
            # we want to turn on debug level logging. also, leave the requests logger at debug as well.
            logging.basicConfig(format=log_format, level=logging.DEBUG)
        else:
            logging.basicConfig(format=log_format)
            # if we aren't debugging, quiet down the requests logger
            logging.getLogger('requests').setLevel(logging.ERROR)

        self.log = logging.getLogger(__name__)

    def run(self):
        current_discharge = self.usgs.fetch_dam_data()
        if current_discharge > self.config.next_discharge_amount:
            # set new discharge rate in config
            new_threshold = current_discharge + self.config.discharge_every
            msg_fmt = (u'ALERT: Dam discharge is currently {level} ft\xB3/s, '
                       'which is over the previous threshold of {threshold} ft\xB3/s. '
                       'Next alert at {new_threshold} ft\xB3/s.')
            send_alert(msg_fmt.format(level=current_discharge,
                                      threshold=self.config.next_discharge_amount,
                                      new_threshold=new_threshold),
                       self.config.app_token, self.config.user_id)
            self.config.next_discharge_amount = new_threshold



@click.command()
@click.option('--debug', default=False, is_flag=True,
              help='Outputs additional debugging information')
def main(debug):
    """
    Pull USGS dam data for the given dam and send an alert if it is above a configured value.
    """

    app = DamnApp(debug)
    app.run()


if __name__ == '__main__':
    main()
