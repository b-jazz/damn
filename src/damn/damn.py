import click
import logging
import re
import requests


logging.basicConfig(level=logging.DEBUG)


SITE = 12345
URL = 'http://waterdata.usgs.gov/nwis/uv?cb_00060=on&format=rdb&site_no={site_no}&period=1'.format(site_no=SITE)


def fetch_dam_data(site=SITE):
    linere = re.compile(r'^.*\t\d{4}-\d{2}-\d{2} \d{2}:\d{2}\t.*$')

    try:
        tab_data = requests.get(URL).text
        # print(tab_data)
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

    return int(measurements[-1])


def send_alert(message):
    post_data = {'token': 'PUSHOVER_TOKEN',
                 'user': 'PUSHOVER_USER',
                 'message': message}

    logging.debug('post data: {0}'.format(post_data))

    pushover_url = 'https://api.pushover.net:443/1/messages.json'

    push_result = requests.post(pushover_url, post_data)
    if push_result.ok:
        print('yes')
    else:
        print(push_result.reason, push_result.text)


@click.command()
@click.option('-l', '--level', default=7000,
              help='the discharge amount to alert on')
def main(level):
    current_discharge = fetch_dam_data()
    print(current_discharge)

    if current_discharge > level:
        send_alert('ALERT: Dam discharge is over {level} ft^3/s'.format(level=current_discharge))


if __name__ == '__main__':
    main()
