#!/usr/bin/python3.4
# -*- coding=utf-8 -*-

from kamene.all import *
from GET_MAC import get_mac_address
from Change_MAC import Change_MAC_To_Bytes
import time

def DHCP_Discover_Sendonly(ifname, MAC, wait_time = 1):
    if wait_time != 0:
        time.sleep(wait_time)
        Bytes_MAC = Change_MAC_To_Bytes(MAC)#把MAC地址转换为二进制格式
        #chaddr一共16个字节，MAC地址只有6个字节，所以需要b'\x00'*10填充到16个字节
        #param_req_list为请求的参数，没有这个部分服务器只会回送IP地址，什么参数都不给
        discover = Ether(dst='ff:ff:ff:ff:ff:ff', src=MAC, type=0x0800) \
                   / IP(src='0.0.0.0', dst='255.255.255.255') \
                   / UDP(dport=67,sport=68) \
                   / BOOTP(op=1, chaddr=Bytes_MAC + b'\x00'*10) \
                   / DHCP(options=[('message-type','discover'), ('param_req_list', b'\x01\x06\x0f,\x03!\x96+'), ('end')])
        sendp(discover, iface = ifname, verbose=False)
    else:
        Bytes_MAC = Change_MAC_To_Bytes(MAC)
        discover = Ether(dst='ff:ff:ff:ff:ff:ff', src=MAC, type=0x0800) \
                   / IP(src='0.0.0.0', dst='255.255.255.255') \
                   / UDP(dport=67,sport=68) \
                   / BOOTP(op=1, chaddr=Bytes_MAC + b'\x00'*10) \
                   / DHCP(options=[('message-type','discover'), ('param_req_list', b'\x01\x06\x0f,\x03!\x96+'), ('end')])
        sendp(discover, iface = ifname, verbose=False)  