//go:build !linux && !windows

package models

import (
	"fmt"
	"net"
)

// bindToInterfaceImpl 通用平台的接口绑定实现
func bindToInterfaceImpl(conn *net.UDPConn, interfaceName string) error {
	// 通用平台不支持接口绑定
	return fmt.Errorf("interface binding not supported on this platform")
}

// setSocketOptionsImpl 通用平台的socket选项设置
func setSocketOptionsImpl(conn *net.UDPConn) error {
	// 通用平台只设置基本的socket选项
	// 这里可以添加一些通用的选项设置
	return nil
}
