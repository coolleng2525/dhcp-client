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

### 4. 超时和重试控制
```bash
./dhcp-client -timeout 10 -retries 5
```
这将：
- 设置每次DISCOVER尝试的超时时间为10秒
- 最多重试5次（总共6次尝试）
- 如果所有尝试都失败，程序将退出并显示错误信息

### 5. 快速测试模式
```bash
./dhcp-client -timeout 1 -retries 0
```
这将：
- 设置超时时间为1秒
- 不进行重试（只尝试1次）
- 适合快速测试网络连接

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-iface` | 指定要绑定的网络接口名称 | `-iface eth0` |
| `-list` | 列出所有可用的网络接口 | `-list` |
| `-mac` | 指定MAC地址（可选，如果不指定则使用接口的MAC） | `-mac 00:11:22:33:44:55` |
| `-ip4` | 请求的IPv4地址 | `-ip4 192.168.1.100` |
| `-retries` | 最大重试次数（默认：3） | `-retries 5` |
| `-timeout` | 每次DISCOVER尝试的超时时间（秒，默认：5） | `-timeout 10` |

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
Sent DISCOVER (attempt 1/4)
Waiting for OFFER..
```

### 超时和重试示例
```bash
$ sudo ./dhcp-client -timeout 2 -retries 2
~ v1.0  Mon, 01 Jan 2024 12:00:00 +0000
~ MAC: 637043181025

Sent DISCOVER (attempt 1/3)
Waiting for OFFER..

DISCOVER timeout, resending DISCOVER (attempt 2/3)
Sent DISCOVER (retry 1/2)
Waiting for OFFER..

OFFER received!
Server offered: 10.223.40.226
```

### 超时失败示例
```bash
$ sudo ./dhcp-client -timeout 1 -retries 0
~ v1.0  Mon, 01 Jan 2024 12:00:00 +0000
~ MAC: CE04AAC77187

Sent DISCOVER (attempt 1/1)
Waiting for OFFER..

DISCOVER timeout after 1 attempts. Giving up.
Possible causes:
  - No DHCP server available on the network
  - Network interface not properly configured
  - Firewall blocking DHCP traffic
  - Interface binding issues
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

4. **DHCP超时**
   ```
   DISCOVER timeout after 3 attempts. Giving up.
   Possible causes:
     - No DHCP server available on the network
     - Network interface not properly configured
     - Firewall blocking DHCP traffic
     - Interface binding issues
   ```
   解决方案：
   - 增加超时时间：`-timeout 10`
   - 增加重试次数：`-retries 5`
   - 检查网络连接和DHCP服务器

### 调试技巧

1. 使用 `-list` 参数确认接口状态
2. 检查接口是否处于UP状态
3. 确认有足够的权限（root）
4. 查看系统日志获取更多信息



dhcp-client.exe -iface "以太网 2"
windows 版还是有问题， 可以跳高eth 的metric 值，来让wifi 接口作为默认接口

在 Windows 系统中，可以通过命令行工具或系统设置调整网络接口的 Metric（度量值），Metric 用于决定路由优先级（值越小优先级越高）。以下是具体方法：
方法 1：使用命令行（推荐）
通过 netsh 命令直接修改接口的 Metric 值，步骤如下：

查看所有网络接口及其索引
打开命令提示符（管理员权限），执行：
cmd
netsh interface ipv4 show interfaces

输出示例：
plaintext
索引  接口名称                 类型   状态         MTU   速度
---  ------------              ----  -----------  -----  -----
12   以太网                    以太网  已连接        1500   10000000
15   WLAN                      无线    已连接        1500   54000000

记录需要调整的接口 索引（如以太网的索引为 12）。
修改接口的 Metric 值
执行以下命令（将 12 替换为接口索引，10 替换为目标 Metric 值）：
cmd
netsh interface ipv4 set interface 12 metric=10 store=persistent

store=persistent 表示设置永久生效（重启后保留）。
若只需临时生效（重启后失效），可省略 store=persistent。
验证修改结果
再次执行 netsh interface ipv4 show interfaces，确认目标接口的 Metric 值已更新。
方法 2：通过图形界面设置
打开 控制面板 > 网络和 Internet > 网络连接，右键点击目标接口（如 “以太网”），选择 属性。
双击 Internet 协议版本 4 (TCP/IPv4)，点击 高级。
在 IP 设置 选项卡中，取消勾选 自动跃点，然后在 接口跃点 中输入目标 Metric 值（如 10）。
点击 确定 保存设置。
注意事项
Metric 值越小，接口的路由优先级越高。例如，若以太网 Metric=10，WLAN Metric=20，则系统优先使用以太网。
自动 Metric 由系统根据接口速度自动分配（速度越快，Metric 越小），手动设置后会覆盖自动分配值。
修改可能需要管理员权限，且部分系统（如 Windows Server）可能有额外限制。

通过以上方法，可以在 Windows 中灵活调整接口的 Metric 值，控制网络流量的路由优先级。