---
title: Chord协议
date: 2026-05-24
tags: [ch2, P2P, Chord, DHT, 分布式哈希表]
---

# Chord 协议

> 参考：Kurose §2.5（DHT 补充）、Stoica et al., "Chord: A Scalable Peer-to-Peer Lookup Service for Internet Applications" (2001)

**Chord** 是经典的分布式哈希表（DHT）协议，用 $O(\log N)$ 的路由信息和 $O(\log N)$ 的查找跳数实现了去中心化的 (key, value) 查找。设计动机是在 BitTorrent 等 P2P 系统中以完全分布式的方式替代集中式 tracker。

## 核心思想

将节点和 key 放在**同一个环上**，按"顺时针方向第一个节点负责该 key"的规则来存储。

## 1. 环的构造

标识符空间是一个 $[0, 2^m - 1]$ 的环，使用与 key 相同的哈希函数（如 SHA-1，$m = 160$）：

- **对等方标识符**：对等方将自己的 IP 地址哈希为 $m$ 位整数，作为环上位置
- **Key 标识符**：key 也用同一哈希函数映射到环上
- **后继（successor）**：环上顺时针方向第一个对等方

假设 $m = 6$（环上 0–63），环上有四个对等方：8、22、42、58。

## 2. 存储规则

**key 存在环上恰好大于 key 的第一个对等方**（即 key 的后继）：

- key = 12 → 顺时针第一个对等方是 22 → 由对等方 22 存储
- key = 36 → 第一个对等方是 42 → 由对等方 42 存储
- key = 60 → 超过 58 须绕回环首 → 由对等方 8 存储

每个对等方只负责环上一小段区间。

## 3. Finger Table

如果每个对等方只知道自己的**直接后继**，查找需绕环一圈，最坏 $O(N)$ 跳。

Chord 的解决方案：每个对等方维护一个 **finger table**，存 $m$ 个条目。第 $i$ 个条目指向环上 $(id + 2^i) \bmod 2^m$ 位置的**后继对等方**。这个结构使得查找可以**指数跳跃**。

以对等方 8 为例（$m = 6$）：

| Finger $i$ | 起点 $= (8 + 2^i) \bmod 64$ | 实际后继 |
|:----------:|:---------------------------:|:------:|
| 0 | 9 | 22 |
| 1 | 10 | 22 |
| 2 | 12 | 22 |
| 3 | 16 | 22 |
| 4 | 24 | 42 |
| 5 | 40 | 42 |

Finger 存的是**真实的环上对等方**，而非算出的位置坐标。多个起点可能映射到同一个后继（如上表 finger 0–3 均指向 22），因此实际对等方数 $N$ 远小于 $2^m$ 时，finger table 中仅有约 $\log N$ 个不同条目。

## 4. 查找过程

查找 key = 36，从对等方 8 出发：

1. **对等方 8**：在 finger table 中找不超过 36 的最大 finger。finger[3] = 22 是最大值（finger[4] = 42 > 36）。将查询转发给 22。

2. **对等方 22**：22 的 finger table（finger 0–3 指向 42，均 > 36）中无不超过 36 的条目。查询转发给**直接后继** 42。

3. **对等方 42**：36 在 22 和 42 之间，42 就是 36 的后继。如果该 key 存在，返回 value；否则不存在。

**共 2 跳。** 关键性质：每跳至少跨越剩余距离的一半——finger $i$ 的间距 $2^i$ 以指数增长，总能在 $O(\log N)$ 跳内到达任意目标。

查找的伪代码：

```
n.find_successor(key):
    if key ∈ (n, successor]:
        return successor
    else:
        n' = closest_preceding_node(key)
        return n'.find_successor(key)

n.closest_preceding_node(key):
    for i = m-1 down to 0:
        if finger[i] ∈ (n, key):
            return finger[i]
    return n
```

## 5. 对等方加入

新对等方加入时，Chord 仅需更新少量节点：

1. 新对等方哈希自己的 IP，获得环上位置 $id$
2. 通过任意已知对等方（**bootstrap 节点**）查找自己的后继
3. 从后继处接管自己该负责的 key（后继原来存的那些 key 中，属于 $[predecessor, id]$ 区间的部分）
4. 新对等方加入后，部分节点的 finger table 失效，通过定期**稳定化协议（stabilization）** 修复

### 稳定化协议

每个对等方周期性运行：

```
n.stabilize():
    x = n.successor.predecessor
    if x ∈ (n, n.successor):
        n.successor = x      // 发现更近的后继
    n.successor.notify(n)    // 通知后继自己的存在

n.notify(n'):
    if predecessor == nil or n' ∈ (predecessor, n):
        predecessor = n'     // n' 是更近的前驱
```

稳定化协议确保：即使节点以任意顺序加入，finger table 最终都能收敛到正确状态。

## 6. 对等方离开

- **优雅离开**：将持有的 key 交给后继，通知前驱和后继
- **突然离开（故障）**：后继通过定期 ping 检测前驱是否存活。数据通过**冗余备份**保护——每个 key 在环上连续的 $r$ 个后继上都存有副本（如 $r = 3$），单个节点故障不丢失数据

## 7. 为什么是 $O(\log N)$？

- Finger table 有 $m$ 个条目，但 $N \ll 2^m$ 时，实际指向约 $\log N$ 个不同节点
- 查找从 finger $m-1$ 开始向下扫描，第一个不越过 key 的 finger 至少覆盖剩余距离的一半
- 因此最多 $\log N$ 跳到达任意目标

每个对等方只需维护 $O(\log N)$ 条路由信息，就能在 $O(\log N)$ 跳内找到任意 key——这是 Chord 设计的核心 tradeoff。

## 8. 在网络中的位置

- **BitTorrent**：去中心化的 tracker——key 是 torrent 的 infohash，value 是拥有该文件的对等方 IP 列表。Chord（或其他 DHT 实现如 Kademlia）让 tracker 功能不再需要集中式服务器
- **[[P2P文件分发]]**：DHT 与 Chord 的顶层应用场景
- **[[DNS]]**：DNS 是分层的，Chord 是扁平的——两者都是分布式查找系统，但组织方式截然不同

- [[P2P文件分发]]
- [[DNS]]
