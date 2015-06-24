#! /usr/bin/env python
"""Periodically updates a Route53 hosted A alias record with the current ip of the system."""

import boto.route53
import logging
import os
import re
from re import search
import socket
import sys
from urllib2 import urlopen, Request
import json
from random import shuffle
import time

logging.basicConfig(
    level=logging.INFO,
)

def icanhazip_com():
    content = urlopen("http://icanhazip.com/").read().strip()
    ip_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', content)
    if len(ip_list) < 1:
        return None
    return ip_list[0]

def jsonip_org():
    req = Request("http://jsonip.org/", headers={'Accept': 'application/json'})
    res = urlopen(req, timeout=20).read()
    return json.loads(res).get("ip", None)

def jsonip_com():
    req = Request("http://jsonip.com/", headers={'Accept': 'application/json'})
    res = urlopen(req, timeout=20).read()
    return json.loads(res).get("ip", None)

def ipinfo_io():
    req = Request("http://ipinfo.io/", headers={'Accept': 'application/json'})
    res = urlopen(req, timeout=20).read()
    return json.loads(res).get("ip", None)

def get_ip_address():
    services = [icanhazip_com, jsonip_org, jsonip_com, ipinfo_io]
    shuffle(services)
    for srv in services:
        try:
            addr = srv()
            if addr is not None:
                try:
                    socket.inet_aton(addr)
                except socket.error:
                    logging.warning('invalid ip addr format obtained from ' + srv.__name__)
                    addr = None
                return addr
        except e:
            logging.warning(str(e))
        logging.warning("ip service %s failed, trying next..." % srv.__name__)
    logging.error('unable to determin WAN address using ANY services')
    return None


def update_dns(record_to_update, ip, aws_key=None, aws_secret=None):
    zone_to_update = '.'.join(record_to_update.split('.')[-2:])
    current_ip = get_ip_address()
    logging.info('detected WAN address as %s' % current_ip)
    r53 = boto.route53.connect_to_region('universal',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', None))
    zone = r53.get_zone(zone_to_update)
    for record in zone.get_records():
        if search(r'<Record:' + record_to_update, str(record)):
            if current_ip in record.to_print():
                logging.info('%s already pointing to %s' % (record_to_update, current_ip))
                return
            logging.info('updating %s to %s' % (record_to_update, current_ip))
            zone.delete_a(record_to_update)
            zone.add_a(record_to_update, current_ip)
            return
    logging.info('adding %s record' % (record_to_update))
    zone.add_a(record_to_update, current_ip)

def main():
    while True:
        update_dns(os.getenv('DYN53_DOMAIN', None), get_ip_address())
        time.sleep(600)

if __name__ == '__main__':
    main()
