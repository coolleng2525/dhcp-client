#!/usr/bin/python3.4
# -*- coding=utf-8 -*-


import struct

def Change_Chaddr_To_MAC(chaddr): 
    '''转换16字节chaddr为MAC地址，前6字节为MAC'''
    MAC_ADDR_INT_List = struct.unpack('>16B', chaddr)[:6]
    MAC_ADDR_List = []
    for MAC_ADDR_INT in MAC_ADDR_INT_List:
        if MAC_ADDR_INT < 16:
            MAC_ADDR_List.append('0' + str(hex(MAC_ADDR_INT))[2:])
        else:
            MAC_ADDR_List.append(str(hex(MAC_ADDR_INT))[2:])
    MAC_ADDR = MAC_ADDR_List[0] + ':' + MAC_ADDR_List[1] + ':' + MAC_ADDR_List[2] + ':' + MAC_ADDR_List[3] + ':' + MAC_ADDR_List[4] + ':' + MAC_ADDR_List[5]
    return MAC_ADDR
 
def Str_to_Int(string):
    if ord(string[0]) > 90:
        int1 = ord(string[0]) - 87
    else:
        int1 = ord(string[0]) - 48

    if ord(string[1]) > 90:
        int2 = ord(string[1]) - 87
    else:
        int2 = ord(string[1]) - 48
    int_final = int1 * 16 + int2
    return int_final

def Change_MAC_To_Bytes(MAC):
    section1 = Str_to_Int(MAC.split(':')[0])
    section2 = Str_to_Int(MAC.split(':')[1])
    section3 = Str_to_Int(MAC.split(':')[2])
    section4 = Str_to_Int(MAC.split(':')[3])
    section5 = Str_to_Int(MAC.split(':')[4])
    section6 = Str_to_Int(MAC.split(':')[5])
    Bytes_MAC = struct.pack('!6B', section1, section2, section3, section4, section5, section6)
    return Bytes_MAC
 