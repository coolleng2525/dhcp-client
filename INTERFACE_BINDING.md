# DHCP客户端接口绑定功能

## 概述

DHCP客户端现在支持可选的网络接口绑定功能，允许您将DHCP请求绑定到特定的网络接口上。

## 新功能

### 1. 列出可用接口
```bash
./dhcp-client -list
```
这将显示系统中所有可用的网络接口，包括：
- 接口名称
- 接口索引
- MAC地址
- 状态（UP/DOWN）
- IP地址（如果有的话）

### 2. 绑定到特定接口
```bash
./dhcp-client -iface eth0 -ip4 192.168.1.100
```
这将：
- 绑定到名为 `eth0` 的网络接口
- 请求IP地址 `192.168.1.100`
- 自动使用该接口的MAC地址（除非通过 `-mac` 参数指定）

### 3. 组合使用
```bash
./dhcp-client -iface wlan0 -mac 00:11:22:33:44:55 -ip4 192.168.1.200
```
这将：
- 绑定到名为 `wlan0` 的网络接口
- 使用指定的MAC地址 `00:11:22:33:44:55`
- 请求IP地址 `192.168.1.200`

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-iface` | 指定要绑定的网络接口名称 | `-iface eth0` |
| `-list` | 列出所有可用的网络接口 | `-list` |
| `-mac` | 指定MAC地址（可选，如果不指定则使用接口的MAC） | `-mac 00:11:22:33:44:55` |
| `-ip4` | 请求的IPv4地址 | `-ip4 192.168.1.100` |

## 技术实现

### 接口绑定机制
- 使用Linux系统的 `SO_BINDTODEVICE` socket选项
- 需要root权限才能成功绑定
- 自动设置广播和地址重用选项

### 错误处理
- 如果接口不存在，会显示错误并列出可用接口
- 如果绑定失败，会提供详细的错误信息
- 包含权限不足的提示信息

## 使用场景

1. **多网卡环境**：在服务器上有多个网络接口时，可以指定使用特定的接口
2. **网络隔离**：确保DHCP请求通过正确的网络路径
3. **调试网络**：在复杂的网络环境中进行故障排除
4. **负载均衡**：在多个网络接口之间分配DHCP请求

## 注意事项

1. **权限要求**：接口绑定功能需要root权限
2. **接口状态**：只能绑定到UP状态的接口
3. **系统兼容性**：主要支持Linux系统
4. **MAC地址**：如果不指定MAC地址，将自动使用绑定接口的MAC地址

## 示例输出

### 列出接口
```bash
$ sudo ./dhcp-client -list
Available network interfaces:
=============================
1. eth0 (Index: 2)
   MAC: 00:15:5d:01:ca:05
   Status: UP
   IP Addresses: 192.168.1.100

2. wlan0 (Index: 3)
   MAC: 00:15:5d:01:ca:06
   Status: UP
   IP Addresses: 10.0.0.50
```

### 绑定到接口
```bash
$ sudo ./dhcp-client -iface eth0 -ip4 192.168.1.200
~ v1.0  Mon, 01 Jan 2024 12:00:00 +0000
~ MAC: 00155D01CA05
~ Interface: eth0

Successfully bound to interface: eth0
Sent DISCOVER
Waiting for OFFER..
```

## 故障排除

### 常见问题

1. **权限不足**
   ```
   Failed to bind to interface 'eth0': SO_BINDTODEVICE failed: operation not permitted
   ```
   解决方案：使用 `sudo` 运行程序

2. **接口不存在**
   ```
   Error finding interface 'eth99': interface 'eth99' not found
   ```
   解决方案：使用 `-list` 参数查看可用接口

3. **接口已关闭**
   ```
   Warning: Interface binding validation failed: interface 'eth0' is down
   ```
   解决方案：确保接口处于UP状态

### 调试技巧

1. 使用 `-list` 参数确认接口状态
2. 检查接口是否处于UP状态
3. 确认有足够的权限（root）
4. 查看系统日志获取更多信息



dhcp-client.exe -iface "以太网 2"