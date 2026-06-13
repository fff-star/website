---
title: TCP往返时间估计与超时间隔
date: 2026-05-17
tags: [ch3, TCP, RTT, 超时, EstimatedRTT, DevRTT, 考试重点]
---

# TCP 往返时间估计与超时间隔

> 参考：Kurose §3.5.3

TCP 使用超时/重传机制处理报文段丢失。超时间隔必须大于连接的**往返时间（Round-Trip Time, RTT）**——如果超时间隔太短，会导致不必要的重传；如果太长，会降低数据传输效率。问题是：TCP 运行的环境从局域网到洲际链路，不同连接的 RTT 差异巨大，且同一条连接的 RTT 随时间波动。因此 TCP 必须动态估计 RTT 并据此设置超时间隔。

## 估计往返时间：EstimatedRTT

TCP 通过测量未重传报文段的确认到达时间来获取 **SampleRTT**——即从发送报文段到收到其 ACK 之间经过的时间。注意：**重传报文段不用于计算 SampleRTT**（因为无法区分收到的 ACK 是对原始报文还是重传报文的确认）。

TCP 维护一个估计值 **EstimatedRTT**，通过对 SampleRTT 做**指数加权移动平均（EWMA）**得到：

$$\text{EstimatedRTT} = (1 - \alpha) \times \text{EstimatedRTT} + \alpha \times \text{SampleRTT}$$

其中推荐值 $\alpha = 0.125$（即 1/8）。展开：

$$\text{EstimatedRTT} = 0.875 \times \text{EstimatedRTT} + 0.125 \times \text{SampleRTT}$$

**EWMA 的含义**：新 SampleRTT 仅贡献 1/8 的权重，历史估计贡献 7/8。这意味着单个波动的 SampleRTT 不会使 EstimatedRTT 剧烈变化，而持续的趋势会被逐步反映。EWMA 是一种计算效率高的"低通滤波器"，平滑地追踪平均 RTT。

## 估计 RTT 的波动：DevRTT

仅知道平均 RTT 不足以设置超时间隔。考虑：如果 EstimatedRTT = 100 ms，但实际 RTT 在 5 ms 到 600 ms 之间剧烈波动——将超时间隔设在略高于 100 ms 会导致大量不必要的重传（因为许多报文段的 RTT 远超 100 ms）。

因此 TCP 还需要跟踪 RTT 的**波动程度**。**DevRTT**（Deviation RTT）是对"SampleRTT 偏离 EstimatedRTT 的程度"的 EWMA 估计：

$$\text{DevRTT} = (1 - \beta) \times \text{DevRTT} + \beta \times |\text{SampleRTT} - \text{EstimatedRTT}|$$

其中推荐值 $\beta = 0.25$（即 1/4）。DevRTT 是对 RTT 标准差的粗略近似。

## 计算超时间隔

TCP 的超时间隔由 EstimatedRTT 加上一个"安全余量"构成，余量与 DevRTT 成正比：

$$\text{TimeoutInterval} = \text{EstimatedRTT} + 4 \times \text{DevRTT}$$

**为什么是 4 倍？** 这是一个工程设计选择——加上 4 倍的偏差使超时间隔在 RTT 波动时足够宽松，可以有效避免因为 RTT 的临时波动而触发错误超时。当 DevRTT 较大（RTT 波动剧烈）时，TimeoutInterval 自动增加；当波动较小时，TimeoutInterval 接近 EstimatedRTT。

此外，TimeoutInterval 有一个**初始值**（通常 1 秒）和一个**推荐最小值**（1 秒），以防止过于激进的重传。

## 重传与 RTT 估计的关系

TCP 的超时间隔使用了**指数退避**——每次超时重传后，TimeoutInterval 翻倍：

$$\text{TimeoutInterval} = 2 \times \text{TimeoutInterval}$$

当后续收到 ACK（非重传报文段的 ACK）后，重新使用 EstimatedRTT 和 DevRTT 的正常公式计算。指数退避防止了在严重拥塞时的持续快速重传。

## 数值示例

假设初始 EstimatedRTT = 100 ms，DevRTT = 10 ms，TimeoutInterval = 140 ms。随后测得 SampleRTT = 120 ms：

- 新的 EstimatedRTT = 0.875 × 100 + 0.125 × 120 = 87.5 + 15 = 102.5 ms
- 新的 DevRTT = 0.75 × 10 + 0.25 × |120 - 102.5| = 7.5 + 4.375 = 11.875 ms
- 新的 TimeoutInterval = 102.5 + 4 × 11.875 = 150 ms

EstimatedRTT 仅轻微上升，DevRTT 略有增加，TimeoutInterval 从 140 ms 调整到 150 ms。

- [[TCP可靠数据传输]]
- [[TCP概述]]
- [[TCP报文段结构]]
- [[TCP拥塞控制]]
