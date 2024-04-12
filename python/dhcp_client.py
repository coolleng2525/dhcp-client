#!/usr/bin/python3.4
# -*- coding=utf-8 -*-

from kamene.all import *
import multiprocessing
from Change_MAC import Change_MAC_To_Bytes
from python.DHCP_Discover import get_mac_address
from Change_MAC import Change_Chaddr_To_MAC
from DHCP_Discover import DHCP_Discover_Sendonly
from DHCP_Request import DHCP_Request_Sendonly

def DHCP_Monitor_Control(pkt):
    try:
        if pkt.getlayer(DHCP).fields['options'][0][1]== 1:#发现并且打印DHCP Discover
            print('发现DHCP Discover包，MAC地址为:',end='')
            MAC_Bytes = pkt.getlayer(BOOTP).fields['chaddr']
            MAC_ADDR = Change_Chaddr_To_MAC(MAC_Bytes)
            print('Request包中发现如下Options:')
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                print('%-15s ==> %s' %(str(option[0]),str(option[1])))          
        elif pkt.getlayer(DHCP).fields['options'][0][1]== 2:#发现并且打印DHCP OFFER
            options = {}
            MAC_Bytes = pkt.getlayer(BOOTP).fields['chaddr']
            MAC_ADDR = Change_Chaddr_To_MAC(MAC_Bytes)
            #把从OFFER得到的信息读取并且写入options字典
            options['MAC'] = MAC_ADDR
            options['client_id'] = Change_MAC_To_Bytes(MAC_ADDR)
            print('发现DHCP OFFER包，请求者得到的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
            print('OFFER包中发现如下Options:')
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                print('%-15s ==> %s' %(str(option[0]),str(option[1])))
            options['requested_addr'] = pkt.getlayer(BOOTP).fields['yiaddr']
            for i in pkt.getlayer(DHCP).fields['options']:
                if i[0] == 'server_id' :
                    options['Server_IP'] = i[1]
            Send_Request = multiprocessing.Process(target=DHCP_Request_Sendonly, args=(Global_IF,options))
            Send_Request.start()
        elif pkt.getlayer(DHCP).fields['options'][0][1]== 3:#发现并且打印DHCP Request
            print('发现DHCP Request包，请求的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
            print('Request包中发现如下Options:')
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                print('%-15s ==> %s' %(str(option[0]),str(option[1])))
        elif pkt.getlayer(DHCP).fields['options'][0][1]== 5:#发现并且打印DHCP ACK
            print('发现DHCP ACK包，确认的IP为:' + pkt.getlayer(BOOTP).fields['yiaddr'])
            print('ACK包中发现如下Options:')
            for option in pkt.getlayer(DHCP).fields['options']:
                if option == 'end':
                    break
                print('%-15s ==> %s' %(str(option[0]),str(option[1])))
    except Exception as e:   
        print(e)
        pass

# get rand mac address and send discover, request, ack

def get_rand_mac_address():
    mac = [ 0x00, 0x0c, 0x29,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def DHCP_FULL(ifname, MAC, timeout = 10):
    global Global_IF
    Global_IF = ifname
    Send_Discover = multiprocessing.Process(target=DHCP_Discover_Sendonly, args=(Global_IF,MAC))#执行多线程，target是目标程序，args是给目标闯入的参数
    Send_Discover.start()
    sniff(prn=DHCP_Monitor_Control, filter="port 68 and port 67", store=0, iface=Global_IF, timeout = timeout)#用于捕获DHCP交互的报文

if __name__ == '__main__':
    ifname = 'ens33'
    # get the ifname from *args
    if len(sys.argv) > 1:
        ifname = sys.argv[1]
    
    MAC = get_rand_mac_address()
    print('the interface:', ifname)
    print('the random MAC:', MAC)
    
    # get_mac_address(ifname)
    DHCP_FULL(ifname, MAC)