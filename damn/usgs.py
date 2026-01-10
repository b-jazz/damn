
import logging
import re

import requests


class USGS(object):
    """
    An object that will build up enough information to fetch data from the USGS website and return parsed results to the user.
    """

    def __init__(self, site):
        self.url = 'http://waterdata.usgs.gov/nwis/uv?cb_00060=on&format=rdb&site_no={site_no}&period=1'.format(site_no=site)
        self.log = logging.getLogger(__name__)

    def fetch_dam_data(self):
        linere = re.compile(r'^.*\t\d{4}-\d{2}-\d{2} \d{2}:\d{2}\t.*$')

        try:
            tab_data = requests.get(self.url).text
            self.log.debug('Found {0} lines of data'.format(len(tab_data)))
        except Exception as ex:
            logging.error('Unable to fetch dam discharge data.')
            raise

        try:
            data_field = 4
            measurements = [measurement.split('\t')[data_field]
                            for measurement in tab_data.split('\n')
                            if linere.match(measurement)]
        except Exception as ex:
            logging.error('Unable to parse the discharge data.')
            raise

        latest_value = int(measurements[-1])
        self.log.debug('Most current reading: {0}'.format(latest_value))

        return latest_value
