package models

import (
	"fmt"
	"net"
	"strings"
)

// NetworkInterface 表示网络接口信息
type NetworkInterface struct {
	Name        string
	Index       int
	MACAddress  net.HardwareAddr
	IPAddresses []net.IP
	IsUp        bool
}

// GetNetworkInterfaces 获取系统上所有可用的网络接口
func GetNetworkInterfaces() ([]NetworkInterface, error) {
	interfaces, err := net.Interfaces()
	if err != nil {
		return nil, fmt.Errorf("failed to get network interfaces: %v", err)
	}

	var result []NetworkInterface
	for _, iface := range interfaces {
		// 跳过回环接口和down状态的接口
		if iface.Flags&net.FlagLoopback != 0 || iface.Flags&net.FlagUp == 0 {
			continue
		}

		// 获取接口的IP地址
		addrs, err := iface.Addrs()
		if err != nil {
			continue
		}

		var ipAddresses []net.IP
		for _, addr := range addrs {
			if ipnet, ok := addr.(*net.IPNet); ok {
				ipAddresses = append(ipAddresses, ipnet.IP)
			}
		}

		result = append(result, NetworkInterface{
			Name:        iface.Name,
			Index:       iface.Index,
			MACAddress:  iface.HardwareAddr,
			IPAddresses: ipAddresses,
			IsUp:        iface.Flags&net.FlagUp != 0,
		})
	}

	return result, nil
}

// FindInterfaceByName 根据名称查找网络接口
func FindInterfaceByName(name string) (*NetworkInterface, error) {
	interfaces, err := GetNetworkInterfaces()
	if err != nil {
		return nil, err
	}

	for _, iface := range interfaces {
		if iface.Name == name {
			return &iface, nil
		}
	}

	return nil, fmt.Errorf("interface '%s' not found", name)
}

// FindInterfaceByMAC 根据MAC地址查找网络接口
func FindInterfaceByMAC(mac string) (*NetworkInterface, error) {
	interfaces, err := GetNetworkInterfaces()
	if err != nil {
		return nil, err
	}

	targetMAC, err := net.ParseMAC(mac)
	if err != nil {
		return nil, fmt.Errorf("invalid MAC address: %v", err)
	}

	for _, iface := range interfaces {
		if iface.MACAddress.String() == targetMAC.String() {
			return &iface, nil
		}
	}

	return nil, fmt.Errorf("interface with MAC '%s' not found", mac)
}

// PrintInterfaces 打印所有可用接口的信息
func PrintInterfaces() {
	interfaces, err := GetNetworkInterfaces()
	if err != nil {
		fmt.Printf("Error getting interfaces: %v\n", err)
		return
	}

	fmt.Println("Available network interfaces:")
	fmt.Println("=============================")
	for i, iface := range interfaces {
		fmt.Printf("%d. %s (Index: %d)\n", i+1, iface.Name, iface.Index)
		fmt.Printf("   MAC: %s\n", iface.MACAddress)
		fmt.Printf("   Status: %s\n", func() string {
			if iface.IsUp {
				return "UP"
			}
			return "DOWN"
		}())
		
		if len(iface.IPAddresses) > 0 {
			fmt.Printf("   IP Addresses: %s\n", strings.Join(func() []string {
				var ips []string
				for _, ip := range iface.IPAddresses {
					ips = append(ips, ip.String())
				}
				return ips
			}(), ", "))
		}
		fmt.Println()
	}
}
