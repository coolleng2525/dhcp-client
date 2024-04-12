#!/usr/bin/python3.4
# -*- coding=utf-8 -*-

from kamene.all import *
import time

def DHCP_Request_Sendonly(ifname, options, wait_time = 1):
    print('Send DHCP Request mac: %s, requested IP: %s' % (options['MAC'], options['requested_addr']))
    request = Ether(dst='ff:ff:ff:ff:ff:ff',src=options['MAC'],type=0x0800)\
              /IP(src='0.0.0.0', dst='255.255.255.255')\
              /UDP(dport=67,sport=68)\
              /BOOTP(op=1,chaddr=options['client_id'] + b'\x00'*10,siaddr=options['Server_IP'],)\
              /DHCP(options=[('message-type','request'),
                     ('server_id', options['Server_IP']),
                     ('requested_addr', options['requested_addr']),
                     ('client_id', b'\x01' + options['client_id']),
                     ('param_req_list', b'\x01\x06\x0f,\x03!\x96+'), ('end')])#’end‘作为结束符，方便后续程序读取
    if wait_time != 0:
        time.sleep(wait_time)
        sendp(request, iface = ifname, verbose=False)
    else:
        sendp(request, iface = ifname, verbose=False)
    