---
title: DHCPv6
date: 2026-06-10
tags: [ch4, IPv6, DHCPv6, 地址分配, SLAAC]
---

# DHCPv6

> 参考：Kurose §4.3.6；RFC 8415

IPv6 的默认地址配置方式是 **SLAAC（无状态地址自动配置）**——主机通过路由器通告（Router Advertisement）获取前缀，自己拼接接口标识符形成地址，全程不需要服务器。但 SLAAC 有两个缺口：（1）它不提供 DNS 服务器地址等配置参数；（2）企业网络管理员可能不想要主机自行决定地址，需要集中管控。**DHCPv6** 填补了这两个缺口。

## 两种工作模式

| 模式 | 提供 IP 地址？ | 提供 DNS 等配置？ | 与 SLAAC 的关系 |
|:---|:---:|:---:|:---|
| **无状态 DHCPv6** | 否 | **是** | SLAAC 拿地址 + DHCPv6 补参数 |
| **有状态 DHCPv6** | **是** | **是** | 完全取代 SLAAC，所有配置由 DHCPv6 提供 |

## 与 DHCPv4 的关键差异

| | DHCPv4 | DHCPv6 |
|:---|:---|:---|
| 客户端端口 | 68 | **546** |
| 服务器端口 | 67 | **547** |
| 通信方式 | 广播（`255.255.255.255`） | **多播**（`ff02::1:2`） |
| 报文名称 | Discover → Offer → Request → ACK | **Solicit → Advertise → Request → Reply** |
| 默认网关 | DHCP 直接提供 | **不提供**——主机从路由器 RA 获取网关 |
| 链路标识 | 依赖子网 | 使用 DHCP 唯一标识符（DUID）——全局唯一，不随接口变化 |

> 注意：DHCPv6 的报文名称虽与 DHCPv4 不同（Solicit 而非 Discover、Advertise 而非 Offer），但四步交互的逻辑完全对应。

## 有状态 DHCPv6：四步过程

当路由器通告中 M 位（Managed）为 1 时，主机使用有状态 DHCPv6：

**1. Solicit（征求）**：客户端从 UDP 端口 546 向多播地址 `ff02::1:2`（链路本地范围内所有 DHCPv6 服务器和中继代理）发送 Solicit 报文，内容为「本链路上有没有 DHCPv6 服务器？」

**2. Advertise（通告）**：服务器收到 Solicit 后，单播回复 Advertise 报文，包含：服务器 DUID、建议的 IPv6 地址、DNS 服务器地址、租用期等配置。

**3. Request（请求）**：客户端从收到的多个 Advertise 中选择一个（通常选第一个），向该服务器单播发送 Request 报文，正式请求其中提供的配置。

**4. Reply（回复）**：服务器确认配置分配，回复 Reply 报文。客户端将分配的地址绑定到接口，交互完成。

注意：DHCPv6 **不提供默认网关地址**——主机通过路由器发送的 RA 消息获取网关（即路由器的链路本地地址）。这是与 DHCPv4 的一个重要区别。

## 无状态 DHCPv6：仅两步

当 RA 中 M=0 但 O 位（Other）为 1 时，主机用 SLAAC 生成地址，仅向 DHCPv6 请求其余配置参数。流程简化为两步：

1. **Information-Request**：客户端向 `ff02::1:2` 多播，询问 DNS、NTP 等配置参数
2. **Reply**：服务器单播回复所请求的参数

无状态模式下没有 Solicit/Advertise/Request——因为不需要分配地址，直接问参数即可。

## 路由器通告中的标志位

主机如何知道该走哪条路径？由路由器 RA 消息中的三个标志位决定：

| M 位 | O 位 | A 位 | 主机的行为 |
|:---:|:---:|:---:|:---|
| 1 | — | — | **有状态 DHCPv6**：向 DHCPv6 获取地址和所有配置 |
| 0 | 1 | 1 | **SLAAC + 无状态 DHCPv6**：SLAAC 生成地址、DHCPv6 提供 DNS 等参数 |
| 0 | 0 | 1 | **纯 SLAAC**：自己拼地址，不联系 DHCPv6（DNS 需另行配置） |
| 0 | 0 | 0 | **纯手动**：地址和参数均需手动配置 |

- **M 位（Managed Address Configuration）**：置 1 表示用有状态 DHCPv6
- **O 位（Other Configuration）**：置 1 表示其他配置参数可通过 DHCPv6 获取
- **A 位（Autonomous Address Configuration）**：置 1 表示前缀可用于 SLAAC

## DUID：DHCP 唯一标识符

DHCPv6 不再使用 MAC 地址来标识客户端（因为一个主机可能有多个接口，MAC 地址作为标识符不够稳定），而是使用 **DUID（DHCP Unique Identifier）**。RFC 8415 定义了三种 DUID 类型：

| 类型 | 构成 | 特征 |
|:---|:---|:---|
| **DUID-LLT** | 链路层地址 + 时间戳 | 最常用，即使换网卡也能通过时间戳区分 |
| **DUID-EN** | 企业编号 + 企业自编标识符 | 由厂商或组织分配 |
| **DUID-LL** | 仅链路层地址 | 简单，但换网卡后 DUID 变化 |

DUID 在整个主机范围内保持一致——同一台主机上所有接口使用同一个 DUID。即使主机在不同子网间移动，服务器始终通过 DUID 识别该主机，而非通过接口的 MAC 地址。这意味着无论连接到哪个网络，DHCPv6 服务器都能知道「这仍然是那台机器」。

- [[IPv6]]
- [[DHCP]]
- [[IPv4编址]]
- [[DNS]]
