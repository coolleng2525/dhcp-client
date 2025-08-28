//go:build linux

package models

import (
	"fmt"
	"net"
	"syscall"
	"unsafe"
)

// bindToInterfaceImpl Linux系统特定的接口绑定实现
func bindToInterfaceImpl(conn *net.UDPConn, interfaceName string) error {
	// 获取文件描述符
	sc, err := conn.SyscallConn()
	if err != nil {
		return fmt.Errorf("failed to get syscall conn: %v", err)
	}

	var bindErr error
	err = sc.Control(func(fd uintptr) {
		// 在Linux上使用SO_BINDTODEVICE选项
		// 这需要root权限
		ifaceName := []byte(interfaceName)
		_, _, errno := syscall.Syscall6(
			syscall.SOL_SOCKET,
			syscall.SO_BINDTODEVICE,
			uintptr(unsafe.Pointer(&ifaceName[0])),
			uintptr(len(ifaceName)),
			0, 0, 0,
		)
		if errno != 0 {
			bindErr = fmt.Errorf("SO_BINDTODEVICE failed: %v", errno)
			return
		}
	})

	if err != nil {
		return fmt.Errorf("control failed: %v", err)
	}

	if bindErr != nil {
		return bindErr
	}

	return nil
}

// setSocketOptionsImpl Linux系统特定的socket选项设置
func setSocketOptionsImpl(conn *net.UDPConn) error {
	sc, err := conn.SyscallConn()
	if err != nil {
		return err
	}

	var setErr error
	err = sc.Control(func(fd uintptr) {
		// 设置广播标志
		enable := 1
		_, _, errno := syscall.Syscall6(
			syscall.SOL_SOCKET,
			syscall.SO_BROADCAST,
			uintptr(unsafe.Pointer(&enable)),
			uintptr(unsafe.Sizeof(enable)),
			0, 0, 0,
		)
		if errno != 0 {
			setErr = fmt.Errorf("SO_BROADCAST failed: %v", errno)
			return
		}

		// 设置重用地址
		_, _, errno = syscall.Syscall6(
			syscall.SOL_SOCKET,
			syscall.SO_REUSEADDR,
			uintptr(unsafe.Pointer(&enable)),
			uintptr(unsafe.Sizeof(enable)),
			0, 0, 0,
		)
		if errno != 0 {
			setErr = fmt.Errorf("SO_REUSEADDR failed: %v", errno)
			return
		}
	})

	if err != nil {
		return err
	}

	return setErr
}
