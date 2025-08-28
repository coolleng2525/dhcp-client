package models

import (
	"fmt"
	"net"
)

// BindToInterface 尝试将UDP连接绑定到指定的网络接口
// 这是一个跨平台的接口，具体实现由不同操作系统的文件提供
func BindToInterface(conn *net.UDPConn, interfaceName string) error {
	return bindToInterfaceImpl(conn, interfaceName)
}

// CreateInterfaceBoundUDPConn 创建一个绑定到指定接口的UDP连接
func CreateInterfaceBoundUDPConn(interfaceName string, localAddr *net.UDPAddr) (*net.UDPConn, error) {
	// 首先创建普通的UDP连接
	conn, err := net.ListenUDP("udp4", localAddr)
	if err != nil {
		return nil, fmt.Errorf("failed to create UDP connection: %v", err)
	}

	// 尝试绑定到指定接口
	if err := BindToInterface(conn, interfaceName); err != nil {
		conn.Close()
		return nil, fmt.Errorf("failed to bind to interface '%s': %v", interfaceName, err)
	}

	// 设置一些有用的socket选项
	if err := setSocketOptions(conn); err != nil {
		fmt.Printf("Warning: Failed to set some socket options: %v\n", err)
	}

	return conn, nil
}

// setSocketOptions 设置一些有用的socket选项
func setSocketOptions(conn *net.UDPConn) error {
	return setSocketOptionsImpl(conn)
}

// ValidateInterfaceBinding 验证接口绑定是否成功
func ValidateInterfaceBinding(conn *net.UDPConn, interfaceName string) error {
	// 获取本地地址信息来验证绑定
	localAddr := conn.LocalAddr()
	if localAddr == nil {
		return fmt.Errorf("failed to get local address")
	}

	// 检查接口是否仍然存在且可用
	iface, err := FindInterfaceByName(interfaceName)
	if err != nil {
		return fmt.Errorf("interface '%s' no longer available: %v", interfaceName, err)
	}

	if !iface.IsUp {
		return fmt.Errorf("interface '%s' is down", interfaceName)
	}

	return nil
}
