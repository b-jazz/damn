
import logging
import re

import click
import requests

from . import config
from . import usgs


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('requests').setLevel(logging.ERROR)


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
    def __init__(self):
        """App Object. This controls everything."""
        self.config = config.Config()
        self.usgs = usgs.USGS(self.config.dam_id)
        self.log = logging.getLogger(__name__)

        self.log.debug('app token: {0}'.format(self.config.app_token))
        self.log.debug('user id: {0}'.format(self.config.user_id))

    def run(self):
        current_discharge = self.usgs.fetch_dam_data()
        if current_discharge > self.config.last_discharge_amount:
            send_alert('ALERT: Dam discharge is over {level} ft^3/s'.format(level=current_discharge),
                       self.config.app_token, self.config.user_id)



@click.command()
def main():
    app = DamnApp()
    app.run()


if __name__ == '__main__':
    main()
