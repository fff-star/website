---
title: 操作日志
date: 2026-05-17
tags: [log]
---

# 操作日志

| 时间               | 操作                | 涉及文件                                                                                                                             |
| ---------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| 2026-05-17 18:00 | 初始化               | index.md, log.md                                                                                                                 |
| 2026-05-17 20:00 | 清空旧条目，重开 Ingest   | 删除全部内容页面，重置 index.md, log.md                                                                                                     |
| 2026-05-17 21:00 | Ingest Kurose 第1章 | 共15条目：概述/构成/服务描述/协议/网络边缘/接入网/物理介质/网络核心/分组交换/电路交换/网络的网络/时延丢包与吞吐量/协议层次与服务模型/安全概述/历史, index.md                                      |
| 2026-05-17 22:00 | Ingest Kurose 第2章 | 共8条目：应用层协议原理/HTTP/电子邮件与SMTP/POP3与IMAP/DNS/P2P文件分发/视频流与CDN/Socket编程, index.md                                                     |
| 2026-05-17 22:59 | Lint：全库审查         | 修复7处事实错误(面向连接/P2P定义/RFC编号/流水线描述/IPv6采用率)、新增TCP往返时间估计+RIP页面、添加约40处缺失交叉引用、补充HTTP/2+HTTP/3+IPv6 SLAAC+双协议栈内容、修复GBN窗口大小论述、更新index.md |
| 2026-05-17 23:00 | Ingest Kurose 第3章 | 共14条目：运输层概述/多路复用与多路分解/UDP/可靠数据传输原理/流水线可靠传输/GBN/SR/TCP概述/TCP报文段结构/TCP可靠数据传输/TCP流量控制/TCP连接管理/拥塞控制原理/TCP拥塞控制, index.md              |
| 2026-05-17 23:30 | Lint：新增12张示意图    | TCP拥塞控制(cwnd锯齿)/TCP首部/UDP首部/IPv6首部/封装解封装/电路vs分组交换/NAT过程/GBN vs SR/ISP层次/DV路由/SDN架构/SMTP邮件系统，嵌入13个页面。删除2个空文件(IP地址与子网/应用层概述)，修复IPv6.md重复标题。generate_diagrams.py |
| 2026-05-17 23:59 | CLUADE.md 更新      | 添加参考行格式规范（第5条）                                                                                                                   |
| 2026-05-18 00:00 | Ingest Kurose 第4章 | 共9条目：网络层概述/路由器体系结构/路由器排队与调度/IPv4数据报/IPv4编址/DHCP/NAT/IPv6/通用转发与SDN数据平面, index.md                                                  |
| 2026-05-18 00:17 | Query：子网掩码范围计算  | IPv4编址.md 新增「子网掩码确定地址范围」节，含/24与/26二进制示例、速查表。来源：用户Query |
| 2026-05-18 00:21 | Query：广播地址机制      | IPv4编址.md 扩充「广播地址」节，新增定向vs受限广播对比表、受限广播逐层工作机制（IP→链路→交换机→路由器）、DHCP示例流程 |
| 2026-05-18 01:00 | Ingest Kurose 第5章 | 共8条目：网络层控制平面概述/LS路由算法/DV路由算法/OSPF/BGP/SDN控制平面/ICMP/网络管理与SNMP, index.md                                                           |
| 2026-05-18 02:00 | Lint：死链修复         | 删除空TCP.md，IP地址与子网→[[IPv4编址]](ICMP.md)，应用层概述→[[应用层协议原理]](因特网的服务描述.md,协议层次与服务模型.md)，index.md                               |
| 2026-05-18 03:00 | Lint：粒度拆分 HTTP    | 拆分HTTP.md为HTTP(概述)+HTTP持久连接与非持久连接+HTTP报文格式+Cookie+Web缓存，共4子页面，index.md                                                           |
| 2026-05-18 04:00 | Lint：粒度拆分 IPv4    | 删除IPv4数据报.md，拆分为IPv4数据报格式.md(首部)+IP分片.md(分片/重组)，更新7个页面的链接，index.md                                                               |
| 2026-05-18 05:00 | Lint：生成Python示意图  | 12幅图：IPv4首部/TCP握手/TCP挥手/路由器结构/DHCP/HTTP连接/IP分片/Dijkstra/OSPF/BGP/DNS/调度，嵌入对应页面，diagrams/generate_diagrams.py                     |
| 2026-05-18 14:39 | Ingest Kurose 第6章 | 共13条目：链路层概述/差错检测与纠错/多路访问协议/信道划分协议/随机访问协议/轮流协议与DOCSIS/链路层寻址与ARP/以太网/链路层交换机/VLAN/MPLS与链路虚拟化/数据中心网络/Web请求的一天, index.md |
| 2026-05-18 14:51 | Query：扩充 UTP 双绞线 | 物理介质.md 扩充「双绞铜线」节，新增 UTP/STP/SFTP 对比、RJ-45 连接器、Cat 3–Cat 8 类别表、以太网双绞线标准表 |
| 2026-05-18 14:58 | Query：扩充拨号接入 | 接入网.md 拆分「卫星与拨号接入」为「拨号接入」+「卫星接入」两节，补充调制解调器原理(调制/解调)、与DSL区别(FDM/语音频段)、V.90/V.92标准、拨号流程 |
| 2026-05-18 15:05 | Query：存储转发流水线 | 分组交换.md 扩充流水线解析（时序图+分步表格+公式推导），generate_diagrams.py 新增 draw_store_forward_pipeline() |
| 2026-05-18 15:09 | Query：T1 线路时分复用计算 | 电路交换.md 扩充 TDM 节，新增 T1 计算过程（PCM 采样 8000/s、DS0 64kbps 公式、T1 速率 = 193×8000 = 1.544 Mbps） |
| 2026-05-18 15:23 | Query：修正处理时延定义 | 时延丢包与吞吐量.md 补充处理时延的第三步（修改首部：递减 TTL、重算检验和） |
| 2026-05-18 15:31 | Query：GET/POST 原因 + HTTP 版本对比 | HTTP报文格式.md 补充 GET 与 POST 设计差异原因（语义分工/幂等性/缓存/长度/安全性）；HTTP.md 重写版本演进（HTTP/1.0→1.1→2→3 逐版动机+四版对比总表） |
| 2026-05-18 16:11 | Lint：修复孤儿页面与交叉引用 | Web请求的一天.md 修正 DHCP 提供 IP 与服务器 IP 相同的问题；随机访问协议.md 嵌入孤立的 csma_cd.png；新增14处缺失交叉引用（网络核心→时延丢包与吞吐量、路由器体系结构→链路层交换机、IPv4编址→链路层寻址与ARP、3个孤立页面→入链共11处） |
| 2026-05-18 16:27 | Lint：增强——4新页面+5新图+交叉引用 | 新建 MTU与MSS、SACK、ECN、TLS 四个概念页；generate_diagrams.py 新增 draw_rdt_fsm/draw_switch_self_learning/draw_nodal_delay/draw_p2p_scaling/draw_dash_adaptation 5个图函数；5幅图嵌入对应页面；新增12处交叉引用至新页面；更新 index.md |
| 2026-05-18 17:19 | Ingest Kurose 第7章 | 共8条目：无线网络概述/无线链路特性/WiFi与802.11/802.11 MAC协议/802.11帧/蜂窝网络因特网接入/移动性管理原理/无线与移动性对TCP的影响；generate_diagrams.py 新增 draw_hidden_terminal/draw_csma_ca_rts_cts/draw_lte_architecture/draw_mobile_ip 4个图函数并嵌入对应页面；更新 index.md |
| 2026-05-18 17:37 | Lint：新增9幅示意图 | CRC模2除法/MPLS标签操作/OpenFlow流表/Fat-Tree拓扑/TDM-FDM-CDMA对比/Web请求全景/CIDR子网对比/WiFi BSS体系结构/802.11数据帧结构，嵌入9个对应页面。generate_diagrams.py |
| 2026-05-18 17:59 | Lint：全库审查 | 删除空文件IP地址与子网.md；为无线与移动性对TCP的影响新增8处入链（无线网络概述/无线链路特性/WiFi与802.11/蜂窝网络因特网接入/移动性管理原理/TCP拥塞控制/TCP可靠数据传输）；拥塞控制原理新增ECN链接；时延丢包与吞吐量、分组交换新增路由器排队与调度链接 |
| 2026-05-18 20:05 | Ingest Kurose 第8章 | 共10新建条目：对称密钥密码学/公开密钥密码学/密码学哈希函数/消息认证码/数字签名/端点认证/安全电子邮件/IPsec与VPN/无线局域网安全/防火墙与入侵检测系统；更新计算机网络安全概述(并入§8.1安全四要素)；更新TLS(SSL记录格式/序号防重放/nonce/截断攻击/算法降级)；新增5张示意图(rsa_overview/digital_signature/ap4_auth/ipsec_tunnel/wpa2_handshake)；更新index.md |
| 2026-05-18 20:49 | Ingest Kurose 第9章 | 共6新建条目：多媒体网络应用概述/流式存储视频/IP语音/RTP与RTCP/SIP/服务质量；新增4张示意图(rtp_header/sip_call_flow/leaky_vs_token_bucket/diffserv_architecture)；更新index.md |
| 2026-05-18 22:26 | Lint：第8/9章审查 + log 时间排序 | 公开密钥密码学.md 删除重复段落（RSA性能说明）；index.md 删除重复 TLS 条目（其他区）、更新计算机网络安全概述摘要与日期、合并 tag；log.md 按时间顺序重新排列全部条目 |
| 2026-05-18 22:59 | Lint：删除空孤儿文件 | IP地址与子网.md（空文件，已第三次清理） |
| 2026-05-18 23:57 | Lint：全库全面审查 | **新增3页面**：FTP(Kurose §2.3,控制/数据连接分离架构)/IP多播(Kurose §4.7,IGMP/PIM-SM/DVMRP)/QUIC(RFC 9000,连接ID/0-RTT/多流)；**新增5幅示意图**：TLS握手/ARP流程/HTTP报文格式/PGP加密签名/POP3-IMAP对比(draw_tls_handshake/draw_arp_process/draw_http_message_format/draw_pgp_flow/draw_pop3_imap)嵌入对应5页面；**新增约30处交叉引用**（27个源文件，覆盖16个入链薄弱页面）；**更新index.md**（ch2+FTP/ch3+QUIC/ch4+IP多播）
| 2026-05-19 02:39 | Lint：STP页面+图+修复 | **新增STP页面**(802.1D,根桥选举/端口角色/BPDU/端口状态收敛/RSTP)；**新增1幅示意图**(draw_stp_topology)；**修复运输层概述↔NAT双向链接**(分层原则违反)；**修复OSPF自链接**；**修复log.md死链**（IP地址与子网/应用层概述）；**新增18处缺失交叉引用**；更新index.md（ch6+STP）, 链路层交换机.md（新增STP引用）
| 2026-05-19 03:10 | Lint：6个新概念页面+5幅图 | **新增6页面**：AQM与RED(Kurose §3.7.1,§4.3.2,RED三段式概率/全局同步/与ECN配合)/OFDM与OFDMA(Kurose §6.3.1,§7.3.2,子载波/循环前缀/资源块分配)/MIMO(Kurose §7.3.2,§7.4.2,空间复用/分集/波束成形/MU-MIMO)/去抖动缓冲区(Kurose §9.3.1,播放延迟/EWMA自适应/与RTP配合)/MIME(Kurose §2.3.2,Content-Type/Base64/multipart)/SDP(RFC 4566,Offer/Answer协商)；**新增5幅示意图**(draw_red_aqm/draw_ofdm_ofdma/draw_mimo_gains/draw_jitter_buffer/draw_mime_structure)；更新index.md（ch2+MIME/ch3+AQM/ch6+OFDM/ch7+MIMO/ch9+去抖动+SDP）
| 2026-05-19 11:21 | Lint：第1-4章与原文对比 | **修复5处关键事实错误**：电路交换.md(35用户概率表述修正)/QUIC.md(TCP重传序号修正+CID长度)/IPv4编址.md(233→223修复多播地址冲突)/路由器排队与调度.md(58% HOL阻塞表征修正)/可靠数据传输原理.md(rdt 3.0 FSM图移至正确章节)；**补充10处缺失概念**：HTTP持久连接(区分流水线/非流水线公式)/DNS(TCP使用场景)/IP分片(DF位+PMTUD)/DHCP(zeroconf术语澄清)/P2P文件分发(NAT穿越)/TCP拥塞控制(Tahoe/Reno/CUBIC+初始cwnd)/时延丢包(traceroute)/协议层次(分层缺点)/计算机网络历史(dot-com/宽带/移动/云)/IPv6(SLAAC隐私扩展)；**新增约80处缺失交叉引用**(覆盖约35个文件) |
| 2026-05-19 12:06 | Lint：第5-7章与原文对比 | **修复4处关键事实错误**：Web请求的一天.md(ARP过程修正——笔记本ARP默认网关IP而非DNS服务器IP)/以太网.md(曼彻斯特编码限定为10Mbps)/OFDM与OFDMA.md(错误§6.3.1引用删除)/TCP拥塞控制.md+无线与移动性对TCP的影响.md(TCP吞吐量公式0.75→1.22)；**补充重点缺失概念**：OSPF.md(IP协议89/5种消息类型/DR+BDR/5种LSA类型/ASBR/Hello协议)/BGP.md(LOCAL_PREF+MED属性/4种消息/路由撤销/路由反射器)/RIP.md(RIPv1/v2/水平分割/请求消息)/ICMP.md(PMTUD/重定向/ICMPv6邻居发现/type3code1+code4)/网络管理与SNMP.md(SMI OID树/MIB-2/SNMPv1明文社区字符串)/WiFi与802.11.md(Zigbee 802.15.4/蓝牙FHSS)/DV路由算法.md(BGP路径向量澄清)/链路层寻址与ARP.md(多播MAC地址)；**新增约25处缺失交叉引用**(覆盖约21个文件) |
49	| 2026-05-19 20:21 | Lint：第8-9章原文对比+全库交叉审查 | **修复5处严重事实错误**：公开密钥密码学.md(RSA证明重写——以欧拉定理替换错误数论结论)/TCP可靠数据传输.md(初始超时0.75s→1.0s,与TCP往返时间估计一致)/UDP.md(伪首部补UDP报文段长度字段)/去抖动缓冲区.md(K=4统计声明修正——v_i为平均偏差非标准差)/多媒体网络应用概述.md(标清视频24fps→30fps)；**修复3处次要问题**：TLS.md(参考§8→§8.6,补充TLS 1.2握手+密码套件命名+会话恢复)/运输层概述.md(新增QUIC注释消解协议数量矛盾)/服务质量.md(漏桶补桶容量参数b)；**Ch8/Ch9交叉引用增强**：对称密钥密码学/密码学哈希函数/消息认证码/数字签名/端点认证/安全电子邮件/无线局域网安全/TLS(新增约30处链接,补齐计算机网络安全概述入链)/RTP与RTCP/SIP/IP语音/视频流与CDN/流式存储视频(新增约15处横向链接,SDP与去抖动缓冲区入链显著加强)；**index.md修复**：MTU与MSS补ch3标签/AQM与RED补ch4标签/计算机网络安全概述Ch8行补ch1标签/TLS与MTU与MSS YAML标签同步修正 |
50	| 2026-05-19 20:37 | Lint：第1-7章重审（四路并行） | **修复16处事实/引用错误**：因特网的构成.md(设备数量250亿→500亿, Cisco流量2019年2ZB→2021年3.3ZB)/接入网.md(DSL速率12/1.8→24/2.5 Mbps)/电路交换.md(概率"约为"→"小于")/MIME.md(§2.3.2→§2.3.3)/FTP.md(§2.3→§2.3.5)/TCP连接管理.md(MSL 2分钟→15-30秒, TIME_WAIT 4分钟→30-60秒)/BGP.md(路径向量定性+MSSD缺失规则第4步补充+重新编号)/DHCP.md(§4.3.3→§4.3.4, 补客户端源端口68)/NAT.md(§4.3.4→§4.3.5, 删"NAT协议"不当措辞)/IPv6.md(§4.3.5→§4.3.6)/IPv4数据报格式.md(TOS补DSCP前6比特说明)/差错检测与纠错.md(奇数比特差错补x+1因子条件) |
51	52	| 2026-05-21 13:01 | Lint：全库审计修复14处问题 | **修复事实/表述问题**：应用层协议原理.md(IP地址→IPv4/IPv6区分)/TLS.md(记录格式标注TLS 1.2)/多媒体网络应用概述.md(PAL/NTSC帧率说明)/STP.md(Forward Delay×2=30s转化解释)；**补充缺失重要概念**：TCP连接管理.md(SYN泛洪攻击+SYN Cookie防御, 三次握手双理由重写)/TCP可靠数据传输.md(延迟ACK详细解释+Nagle交互)/DNS.md(SOA/PTR/TXT记录类型+DoT/DoH加密DNS)/BGP.md(RPKI路由安全+路由劫持案例)/NAT.md(STUN/TURN/ICE/UPnP穿越技术详解)；**交叉引用增强**：服务质量→去抖动缓冲区, HTTP→MIME, 多媒体网络应用概述→SDP；**index.md更新**：TCP连接管理/TCP可靠数据传输/DNS/NAT/BGP摘要与标签同步 |
| 2026-05-24 14:43 | Query：新增Chord详解 | 新建Chord.md（环结构/finger table/查找过程/对等方加入离开/稳定化协议/O(log N)分析），P2P文件分发.md精简Chord节并链接新条目，index.md新增Chord行，HTTP.md/HTTP持久连接与非持久连接.md修正HTTP/1.0默认非持久连接表述 |
| 2026-05-25 12:42 | Ingest：拆分本地DNS服务器为独立条目 | 新建 本地DNS服务器.md（递归/迭代查询、缓存机制与TTL、配置方式、公共DNS服务、加密DNS影响），DNS.md 精简本地DNS小节并添加交叉引用链接，index.md 新增条目行 |
| 2026-05-27 00:19 | Query + Ingest：域名命名规则 + DNS委托澄清 + 子域委托补充 | 新建 域名命名规则.md（层次结构/标签规则/TLD分类/FQDN/子域委托），generate_diagrams.py 新增 draw_domain_hierarchy() + draw_dns_delegation()，DNS.md 权威DNS小节改写澄清 + 新增"子域委托：当域内还有层级权威"一节（含Kurose原文引用的10消息场景/NS记录委托链），index.md 新增域名命名规则条目行 |
| 2026-06-07 15:05 | Query：FTP表示类型与格式控制补充 | FTP.md 新增"表示类型与格式控制"节（TYPE/MODE/STRU命令详解），命令表新增TYPE/MODE/STRU三行，HTTP与FTP对比表修正"默认使用二进制模式"→"默认ASCII模式（TYPE A），需手动切换至二进制模式（TYPE I）" |
| 2026-06-07 15:14 | Query：DNS递归查询与迭代查询补充 | DNS.md 新增"递归查询与迭代查询"专节（定义/对比表/混合模式原因/RD与RA标志位），查询过程节添加交叉引用；generate_diagrams.py 新增 draw_dns_query_types() 函数生成 dns_query_types.png；FTP.md 同步补充格式控制节 |
| 2026-06-07 15:46 | Fix：HTTP连接图重绘 | draw_http_connections() 全面重写：非持久连接每个对象独立TCP握手（不再共享一个握手）、响应箭头方向修正为时间正序、添加RTT括号标记+连接关闭指示；持久连接RTT 2→3（握手+HTML+流水线图片）、增加HTML解析发现标记、添加连接生命周期括号；HTTP持久连接与非持久连接.md 同步修正流水线RTT分析 |
| 2026-06-08 12:57 | Fix & Ingest：UDP表格修复 + 检验和计算示例 | UDP.md 修复常见UDP应用表格（删除空白第三列、修复[[IP语音\|VoIP/流媒体]]管道符截断、补全SNMP理由）；新增"检验和计算示例"小节（含三个16比特字完整四步计算过程、进位回卷图示、接收端验证、伪首部说明）；新增"为什么用反码求和"小节 |
| 2026-06-08 15:29 | Fix：gbn_vs_sr 时序完全重写 | generate_diagrams.py draw_gbn_vs_sr() 完全重写：所有箭头从水平改为有斜度（tail.y > head.y=下行时间方向）、ACK箭尾在上箭头在下（接收方发送→发送方接收）、流水线体现（pkt1-3在ACK0到达前连续发送）、数据包按y_send-y_recv=dy体现传输延迟、丢失标记✗、超时用横虚线标记、重传用橙色箭头区分；重新生成 gbn_vs_sr.png |
| 2026-06-08 19:24 | Ingest & Fix：UDP伪首部重构 | UDP.md "UDP 检验和"节重构：新增"检验和的覆盖范围：伪首部"独立小节（伪首部五字段表格、四条关键特性、跨协议引用TCP）、计算示例前移为检验和覆盖范围的自然延伸、原末尾注意块内容吸收进正文；generate_diagrams.py 新增 draw_udp_checksum_coverage() 函数生成 udp_checksum_coverage.png（伪首部+UDP首部+数据三层覆盖范围图）；重新生成全部图片 |
| 2026-06-08 19:49 | Ingest：UDP检验和计算细节补充 | UDP.md "检验和的计算过程"新增两个计算细节：步骤1"检验和字段暂填0"（发送方先将检验和字段置全零再计算）、步骤5"全零替换"（计算结果0x0000→0xFFFF防止与"未计算"标志混淆，反码+0/−0等价性）；计算示例说明中补充"检验和字段已置全0"的前提条件 |
| 2026-06-08 19:54 | Fix：UDP反码求和定义修正 | UDP.md 合并"反码求和"与"进位回卷"为单一操作（反码求和 = 二进制加法 + 进位回卷，不可割裂理解），步骤从 5 步精简为 4 步 |
| 2026-06-09 15:18 | Ingest：TCP字节流序号具体示例扩展 | TCP报文段结构.md "序号"节扩展：新增500个报文段的字节范围-序号对照表（ISN=0教学演示）、字节序号与报文段序号对比说明、确认号与字节序号的关系、与GBN/SR的对比并标注为常见考点 |
| 2026-06-09 16:11 | Fix：SACK示例修正 | SACK.md "累积确认的局限"示例重写：原"可能重传2000-7999全部"（GBN风格）替换为三种场景的精确对比——单段丢失（TCP Reno只需重传一个段）、多段丢失无SACK（逐个发现/逐个重传/N个RTT）、多段丢有关SACK（一次性重传全部）；消除原示例中TCP Reno与纯GBN行为的混淆 |
| 2026-06-10 12:21 | Ingest：分组调度章节大幅扩展 | 路由器排队与调度.md "分组调度"节从简要描述扩展为完整技术说明——FIFO（弃尾/无公平性）、优先权排队（饥饿问题/非抢占式）、Round Robin（工作保存/分组大小导致带宽不公平）、WFQ（权重保证速率/空闲份额重新分配/虚拟完成时间机制/逐比特轮转模拟）；新增四种调度对比表和Diffserv配合说明 |
| 2026-06-10 12:23 | Ingest：IPv4首部检验和扩展 | IPv4数据报格式.md "首部检验和"字段从简要描述扩展为：明确计算方式与UDP一致（反码求和/进位回卷）、明确覆盖范围（仅IP首部，含选项，不使用伪首部）、每跳重算原因（TTL变化）、IPv6取消检验和的动机 |
| 2026-06-10 12:27 | Ingest：WFQ逐比特轮转解释重写 | 路由器排队与调度.md WFQ节重写：用具体例子（A w=5/100bit vs B w=3/30bit → B优先）解释虚拟完成时间 L/w_i、max() 公式、分组大小与权重共同决定顺序的核心逻辑 |
| 2026-06-10 12:42 | Ingest：子网定义重写 | IPv4编址.md "接口与子网"节重写：删除「拔接口」的误导表述，改用"删除路由器"思想实验 + ASCII 拓扑图说明子网 = 没有路由器隔开的互连孤岛 |
| 2026-06-10 12:46 | Ingest：子网概念示意图 | generate_diagrams.py 新增 draw_subnet_concept()——左右对比图（原始拓扑 vs 删除路由器后），三个子网用蓝/橙/绿区域标注，IPv4编址.md 嵌入引用 |
| 2026-06-10 14:28 | Fix：DHCP图箭头方向 + 子网概念图布线 | generate_diagrams.py: draw_dhcp() 用 y<5 判方向导致 Offer 箭头反向，改为每步显式标注方向；draw_subnet_concept() 主机→交换机走线从折返改为水平总线拓扑 |
| 2026-06-10 14:31 | Fix：IPv6首部图目的地址高度错误 | generate_diagrams.py draw_ipv6_header(): 目的地址 h=0.5→h=4（与源地址相同），宽度 40→32 位，布局从 9 行改为 12 行 |
| 2026-06-10 14:39 | Ingest：DHCPv6条目新建 | 新增 DHCPv6.md——有状态(四步Solicit→Advertise→Request→Reply)/无状态(两步Information-Request→Reply)两种模式、与DHCPv4差异表、RA标志位(M/O/A)、DUID三种类型；index.md新增条目；IPv6.md交叉链接 |
| 2026-06-10 14:50 | Ingest：IPv6邻居发现协议条目新建 | 新增 IPv6邻居发现协议.md——NDP五大消息(RS/RA/NS/NA/Redirect)完整说明、RA两种触发方式(周期性/RS触发)、NS/NA取代ARP(多播替代广播)、DAD复用NS/NA、与IPv4对应关系表；index.md、IPv6.md、ICMP.md交叉链接 |
| 2026-06-10 14:58 | Ingest：通用转发与SDN数据平面重写 | 通用转发与SDN数据平面.md 全文重写：从传统转发的局限引入、用一台4端口交换机逐步扩展流表(转发→防火墙→NAT→负载均衡)展示匹配加动作范式、12匹配字段分四层归类、删除原不知所云的h5/h6/s3示例 |
| 2026-06-10 15:35 | Ingest：IP多播 MAC映射二次过滤展开 | IP多播.md "MAC层多播地址"段扩展：新增链路层/ip层两步过滤流程图解、具体数字例子(224.0.1.1 vs 238.0.1.1 → 同一MAC 01:00:5E:00:01:01)、网卡多收→ip层丢弃的完整数据路径 |
| 2026-06-10 15:40 | Lint：交叉引用修复 | 修复孤儿页面：DNS.md、本地DNS服务器.md 添加 [[域名命名规则]] 链接；缺失交叉引用：DHCP.md→[[DHCPv6]]、TCP流量控制.md→[[拥塞控制原理]]；验证全部图片引用有效 |
| 2026-06-10 15:46 | Ingest：LS路由算法 从Dijkstra输出到转发表 | LS路由算法.md 新增"从算法输出构建转发表"节：p(v)溯源推导下一跳、用表格中实际数据推导u的最终转发表、证明所有节点独立计算无冲突 |
| 2026-06-10 15:57 | Ingest：LS路由算法 开头补充两阶段流程 | LS路由算法.md 开头重写为"阶段一洪泛+阶段二计算"结构：明确LSA包含拓扑和地址两类信息、每个路由器接口的子网前缀在洪泛中就会广播、全网LSDB包含完整拓扑和子网位置 |
| 2026-06-10 16:11 | Ingest：OSPF DR/BDR和区域分层展开 | OSPF.md DR/BDR段从一句话展开为选举规则、O(n²→O(n))邻接数量削减、BDR热备份；区域分层从一段展开为骨干/非骨干/ABR/ASBR四种角色、区域间路由完整流程(源→ABR→Area0→ABR→目的)、为何强制经过骨干 |
| 2026-06-10 16:37 | Ingest：BGP全文重写 | BGP.md 从术语堆砌重写为叙事结构：从BGP解决什么问题的故事开场→前缀+AS-PATH核心机制→eBGP/iBGP拓扑图→NEXT-HOP如何对接IGP→五步路由选择各有具体例子→商业关系决定通告策略→RPKI安全→与OSPF对比表 |
