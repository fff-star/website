---
title: Socket编程
date: 2026-05-17
tags: [ch2, Socket, TCP, UDP, 编程]
---

# Socket 编程

> 参考：Kurose §2.7

网络应用的核心是网络程序。编写网络程序时，开发者通过**套接字（socket）**应用程序编程接口（API）使用运输层服务。本节介绍如何使用 TCP 和 UDP 套接字编写简单的客户-服务器应用。

## 套接字编程基础

套接字是应用进程与运输层协议之间的接口。应用开发者可以控制套接字的**应用层一侧**的所有内容，但对**运输层一侧**的控制仅限于：

1. 选择运输协议（TCP 或 UDP）
2. 设置少数运输层参数（如最大缓冲区和最大报文段大小）

TCP 和 UDP 的套接字编程模型有本质区别：

| | UDP | TCP |
|------|-----|-----|
| 连接模式 | 无连接——每个分组独立寻址 | 面向连接——先建立连接再通信 |
| 数据边界 | 保留分组边界 | 不保留——字节流 |
| 可靠性 | 无保证 | 可靠、有序 |
| 编程模型 | 同一套接字收发来自任何源的数据 | 每客户端一个独立套接字 |

## UDP 套接字编程

UDP 是无连接的协议——发送分组之前不需要握手。UDP 分组在发出时被附加上目的地址（目的 IP 地址 + 目的端口号）。发送方不需要在发送前建立连接。

### 客户端-服务器交互

```
服务器:                              客户端:
socket()       创建套接字              socket()
bind()         绑定端口号
recvfrom()     等待接收               sendto()      发送数据
               处理请求
sendto()       发送响应               recvfrom()    接收响应
close()        关闭套接字              close()
```

关键点：
- 服务器使用 `bind()` 将套接字绑定到特定端口号
- 客户端不需要 `bind()`——操作系统自动分配一个临时端口号
- `sendto()` 需要指定目的地址和端口
- `recvfrom()` 返回发送方的地址和端口（以便服务器可以向正确的客户端回复）

## TCP 套接字编程

TCP 是面向连接的协议——客户端和服务器在开始交换数据之前必须先通过三次握手建立 TCP 连接。TCP 连接建立后，应用只需向套接字中写入数据，TCP 负责确保数据按序、无误地到达目的地。

### 客户端-服务器交互

```
服务器:                              客户端:
socket()       创建欢迎套接字          socket()
bind()         绑定端口号
listen()       开始监听
accept()       等待连接请求
               阻塞直到连接到达        connect()     发起连接(三次握手)
               创建新连接套接字
               ↓
recv()         接收请求               send()        发送请求
               处理请求
send()         发送响应               recv()        接收响应
close()        关闭连接套接字          close()
```

关键点：

- `listen()` 将套接字转换为**监听套接字**，准备接受来自客户端的连接请求
- `accept()` 为每个新到达的客户端创建一个**新的套接字**（连接套接字），与原来的欢迎套接字不同
- 服务器可以为每个客户端创建新线程，也可以使用线程池复用，以实现并发服务多个客户端
- `connect()` 执行三次握手：客户端发送 SYN，服务器回应 SYN-ACK，客户端发送 ACK
- TCP 没有分组边界——`recv()` 收到的字节数可能与 `send()` 发送的不完全对应

### 欢迎套接字与连接套接字

TCP 服务器维护两种套接字：

- **欢迎套接字（welcome socket）**：监听特定端口，等待来自客户端的初始 TCP 连接请求
- **连接套接字（connection socket）**：为每个已建立的 TCP 连接创建一个**独立的新套接字**

这样设计的原因是：服务器可以通过欢迎套接字继续接受新的客户端连接，与此同时通过各自的连接套接字与已连接的客户端进行通信。典型实现是服务器为每个连接套接字创建一个新线程：主线程在欢迎套接字上阻塞等待新连接；每当新连接到达，`accept()` 返回一个新的连接套接字，主线程创建一个新线程来处理该客户端的通信。

## 使用 Python 的简单例子

### UDP 客户端（发送小写句子，接收大写句子）

```python
from socket import *
serverName = 'hostname'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input('Input lowercase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
```

### UDP 服务器

```python
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to receive')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```

### TCP 客户端

```python
from socket import *
serverName = 'servername'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Input lowercase sentence:')
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence.decode())
clientSocket.close()
```

### TCP 服务器

```python
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
```

在 TCP 中，`AF_INET` 表示 IPv4，`SOCK_STREAM` 表示 TCP。`connect()` 执行与服务器的三次握手。服务器使用 `accept()` 为客户端创建一个新的连接套接字 `connectionSocket`，完成握手后与客户端通过此套接字收发数据。

- [[应用层协议原理]]
- [[TCP概述]]
- [[UDP]]
- [[P2P文件分发]]
- [[因特网的服务描述]]
- [[多路复用与多路分解]]
