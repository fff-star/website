#!/usr/bin/env python3
"""Generate diagrams for the computer networks wiki."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
from matplotlib import font_manager
import numpy as np
import os

OUTPUT = os.path.dirname(os.path.abspath(__file__))

# Register CJK font
font_path = '/usr/share/fonts/google-noto-sans-cjk-fonts/NotoSansCJK-Medium.ttc'
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def save(fig, name):
    path = os.path.join(OUTPUT, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved {name}")


# ── 1. IPv4 Header Diagram ─────────────────────────────────────────────
def draw_ipv4_header():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('IPv4 数据报首部格式', fontsize=14, fontweight='bold', pad=20)

    # Field definitions: (name, bit_start, bit_end, row, height, color)
    fields = [
        ("版本\n(4bit)", 0, 4, 7, 1, '#FFE0B2'),
        ("首部长度\n(4bit)", 4, 8, 7, 1, '#FFE0B2'),
        ("服务类型 TOS (8bit)", 8, 16, 7, 1, '#FFF9C4'),
        ("总长度 Total Length (16bit)", 16, 32, 7, 1, '#FFF9C4'),

        ("标识 Identification (16bit)", 0, 16, 6, 1, '#C8E6C9'),
        ("标志(3)\n分片偏移(13)", 16, 32, 6, 1, '#C8E6C9'),

        ("寿命 TTL (8bit)", 0, 8, 5, 1, '#BBDEFB'),
        ("协议 Protocol (8bit)", 8, 16, 5, 1, '#BBDEFB'),
        ("首部检验和 Header Checksum (16bit)", 16, 32, 5, 1, '#BBDEFB'),

        ("源 IP 地址 Source Address (32bit)", 0, 32, 4, 1, '#E1BEE7'),

        ("目的 IP 地址 Destination Address (32bit)", 0, 32, 3, 1, '#E1BEE7'),

        ("选项 Options（如果有，可变长度，很少使用）", 0, 32, 2, 1, '#E0E0E0'),

        ("数据 Data（有效载荷，如 TCP/UDP 报文段）", 0, 32, 1, 1, '#FFCDD2'),
    ]

    for name, x0, x1, y0, h, color in fields:
        rect = FancyBboxPatch((x0, y0 - 0.5), x1 - x0, h,
                              boxstyle="round,pad=0.05", facecolor=color,
                              edgecolor='#333', linewidth=0.8)
        ax.add_patch(rect)
        cx = (x0 + x1) / 2
        cy = y0 - 0.5 + h / 2
        fs = 8 if len(name) > 25 else 9
        ax.text(cx, cy, name, ha='center', va='center', fontsize=fs, fontweight='normal')

    # Column label: 32 bits
    ax.text(16, 7.8, '32 比特', ha='center', fontsize=10, fontstyle='italic', color='#555')
    # Byte ruler
    for i in range(5):
        x = i * 8
        ax.plot([x, x], [0.5, 7.7], 'k--', linewidth=0.4, alpha=0.3)
    for i in range(4):
        x = i * 8 + 4
        ax.text(x, 0.2, f'{i*4}', ha='center', fontsize=6, color='gray')
        ax.text(x, 7.65, f'{i*4}', ha='center', fontsize=6, color='gray')

    ax.text(16, -0.3, '← 首部（通常 20 字节）→', ha='center', fontsize=9, color='#555')
    save(fig, 'ipv4_header.png')


# ── 2. TCP Three-Way Handshake ─────────────────────────────────────────
def draw_tcp_handshake():
    """TCP three-way handshake. Time flows downward (tail.y > head.y)."""
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('TCP 三次握手', fontsize=14, fontweight='bold', pad=15)

    # Client and Server vertical lines (top to bottom = time)
    client_x, server_x = 2, 8
    ax.plot([client_x, client_x], [0.5, 9.5], '#1565C0', linewidth=2)
    ax.plot([server_x, server_x], [0.5, 9.5], '#C62828', linewidth=2)
    ax.text(client_x, 9.8, '客户端', ha='center', fontsize=11, fontweight='bold', color='#1565C0')
    ax.text(server_x, 9.8, '服务器', ha='center', fontsize=11, fontweight='bold', color='#C62828')

    # State annotations — placed between message events (top→bottom: early→late)
    # Client: CLOSED @top, SYN-SENT after sending SYN, ESTABLISHED after receiving SYN+ACK & sending ACK
    states_c = [(8.5, 'CLOSED'), (6.8, 'SYN-SENT'), (3.5, 'ESTABLISHED')]
    states_s = [(8.5, 'LISTEN'), (5.8, 'SYN-RCVD'), (3.5, 'ESTABLISHED')]
    for y, s in states_c:
        ax.text(client_x - 1.5, y, s, fontsize=7, color='#1565C0', va='center')
    for y, s in states_s:
        ax.text(server_x + 0.5, y, s, fontsize=7, color='#C62828', va='center')

    # SYN: client→server, tail.y(7.5) > head.y(6.5) → arrow slopes downward ✓
    ax.annotate('', xy=(server_x, 6.5), xytext=(client_x, 7.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 6.7, 'SYN, seq=x\n(无数据)', ha='center', fontsize=9, color='#333')

    # SYN+ACK: server→client
    ax.annotate('', xy=(client_x, 5), xytext=(server_x, 6),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 5.3, 'SYN+ACK, seq=y, ack=x+1\n(无数据)', ha='center', fontsize=9, color='#333')

    # ACK: client→server
    ax.annotate('', xy=(server_x, 3.5), xytext=(client_x, 4.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 3.7, 'ACK, ack=y+1\n(可携带数据)', ha='center', fontsize=9, color='#333')

    # RTT bracket: from SYN sent (y=7.5) to SYN+ACK received (y=5)
    ax.annotate('', xy=(1.5, 5), xytext=(1.5, 7.5),
                arrowprops=dict(arrowstyle='<->', color='#888', lw=1.2))
    ax.text(1.2, 6.25, 'RTT', ha='center', fontsize=8, color='#888', style='italic', rotation=90, va='center')

    save(fig, 'tcp_handshake.png')


# ── 3. TCP Four-Way Wave ───────────────────────────────────────────────
def draw_tcp_wave():
    """TCP four-way wave (connection teardown). Time flows downward (tail.y > head.y)."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('TCP 四次挥手', fontsize=14, fontweight='bold', pad=15)

    client_x, server_x = 2, 8
    ax.plot([client_x, client_x], [0.5, 9.5], '#1565C0', linewidth=2)
    ax.plot([server_x, server_x], [0.5, 9.5], '#C62828', linewidth=2)
    ax.text(client_x, 9.8, '主动关闭方 (客户端)', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    ax.text(server_x, 9.8, '被动关闭方 (服务器)', ha='center', fontsize=10, fontweight='bold', color='#C62828')

    # ── Messages (top→bottom, tail.y > head.y → arrows slope downward) ──
    # 1. FIN: client→server
    ax.annotate('', xy=(server_x, 6), xytext=(client_x, 7),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 6.3, 'FIN, seq=u\n(无数据)', ha='center', fontsize=9, color='#333')

    # 2. ACK: server→client
    ax.annotate('', xy=(client_x, 5), xytext=(server_x, 5.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 4.8, 'ACK, ack=u+1', ha='center', fontsize=9, color='#333')

    # 3. FIN: server→client
    ax.annotate('', xy=(client_x, 3.5), xytext=(server_x, 4.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 3.7, 'FIN, seq=v, ack=u+1\n(无数据)', ha='center', fontsize=9, color='#333')

    # 4. ACK: client→server
    ax.annotate('', xy=(server_x, 2), xytext=(client_x, 3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 2.2, 'ACK, ack=v+1', ha='center', fontsize=9, color='#333')

    # ── State labels (left: client, right: server) ──
    # Client states (top→bottom = state transitions)
    ax.text(client_x - 1.5, 8.5, 'ESTABLISHED', fontsize=7, va='center', color='#555')
    ax.text(client_x - 1.5, 6.7, 'FIN-WAIT-1', fontsize=7, va='center', color='#555')
    ax.text(client_x - 1.5, 5.2, 'FIN-WAIT-2', fontsize=7, va='center', color='#555')
    ax.text(client_x - 1.5, 3.2, 'TIME-WAIT\n(2MSL)', fontsize=7, va='center', color='#555')
    ax.text(client_x - 1.5, 1.3, 'CLOSED', fontsize=7, va='center', color='#555')

    # Server states
    ax.text(server_x + 0.5, 8.5, 'ESTABLISHED', fontsize=7, va='center', color='#555')
    ax.text(server_x + 0.5, 5.7, 'CLOSE-WAIT', fontsize=7, va='center', color='#555')
    ax.text(server_x + 0.5, 4.2, 'LAST-ACK', fontsize=7, va='center', color='#555')
    ax.text(server_x + 0.5, 2.3, 'CLOSED', fontsize=7, va='center', color='#555')

    # 2MSL bracket: from TIME-WAIT entry (y≈3.5) to CLOSED (y≈1.3)
    ax.annotate('', xy=(client_x - 1.2, 1.3), xytext=(client_x - 1.2, 3.5),
                arrowprops=dict(arrowstyle='<->', color='#FF6F00', lw=1.5))
    ax.text(client_x - 2.3, 2.4, '2MSL\n≈ 60s', ha='center', fontsize=7, color='#FF6F00')

    save(fig, 'tcp_wave.png')


# ── 4. Router Architecture ─────────────────────────────────────────────
def draw_router_arch():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('路由器体系结构', fontsize=14, fontweight='bold', pad=15)

    # Input ports
    for i, y in enumerate([4.5, 3.5, 2.5, 1.5]):
        rect = FancyBboxPatch((0.5, y), 2.5, 0.7,
                              boxstyle="round,pad=0.1", facecolor='#BBDEFB',
                              edgecolor='#333', linewidth=1)
        ax.add_patch(rect)
        ax.text(1.75, y + 0.35, f'输入端口 {i+1}\n终结线路→查表→转发', ha='center', va='center', fontsize=7)

    # Switching fabric
    rect = FancyBboxPatch((3.5, 1.0), 5, 4.5,
                          boxstyle="round,pad=0.15", facecolor='#E0E0E0',
                          edgecolor='#333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(6, 3.8, '交换结构\n(Switching Fabric)', ha='center', va='center', fontsize=10, fontweight='bold')

    # Types
    ax.text(4.2, 1.6, '通过内存', fontsize=7, color='#555')
    ax.text(5.8, 1.6, '通过总线', fontsize=7, color='#555')
    ax.text(7.4, 1.6, '通过互联网络\n(Crossbar)', fontsize=7, color='#555')

    # Output ports
    for i, y in enumerate([4.5, 3.5, 2.5, 1.5]):
        rect = FancyBboxPatch((9.0, y), 2.5, 0.7,
                              boxstyle="round,pad=0.1", facecolor='#C8E6C9',
                              edgecolor='#333', linewidth=1)
        ax.add_patch(rect)
        ax.text(10.25, y + 0.35, f'输出端口 {i+1}\n排队→调度→线路终结', ha='center', va='center', fontsize=7)

    # Routing processor
    rect = FancyBboxPatch((4, 5.0), 4, 0.8,
                          boxstyle="round,pad=0.1", facecolor='#FFE0B2',
                          edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(6, 5.4, '路由处理器 (Routing Processor)', ha='center', va='center', fontsize=9, fontweight='bold')
    ax.text(6, 5.15, '运行路由协议 → 维护转发表', ha='center', va='center', fontsize=7, color='#555')

    # Control arrows
    ax.annotate('', xy=(4, 5.4), xytext=(3, 5.4),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=1.5, connectionstyle='arc3,rad=0.3'))
    ax.annotate('', xy=(8, 5.4), xytext=(9, 5.4),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=1.5, connectionstyle='arc3,rad=-0.3'))

    save(fig, 'router_architecture.png')


# ── 5. DHCP Four-Step Process ──────────────────────────────────────────
def draw_dhcp():
    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('DHCP 四步过程', fontsize=14, fontweight='bold', pad=15)

    cx, sx = 2, 7
    ax.plot([cx, cx], [0.5, 8.5], '#1565C0', linewidth=2)
    ax.plot([sx, sx], [0.5, 8.5], '#2E7D32', linewidth=2)
    ax.text(cx, 8.8, 'DHCP 客户端\n(新到达主机)', ha='center', fontsize=9, fontweight='bold', color='#1565C0')
    ax.text(sx, 8.8, 'DHCP 服务器\n(端口67)', ha='center', fontsize=9, fontweight='bold', color='#2E7D32')

    steps = [
        (2.0, '1. DHCP 发现 (Discover)\n   广播, src=0.0.0.0:68, dst=255.255.255.255:67', '#FF7043', '->'),
        (3.5, '2. DHCP 提供 (Offer)\n   广播/单播, 包含建议IP、子网掩码、租用期', '#FFA726', '<-'),
        (5.5, '3. DHCP 请求 (Request)\n   广播, 正式请求某个IP地址', '#42A5F5', '->'),
        (7.0, '4. DHCP ACK\n   确认, 包含最终配置参数', '#66BB6A', '<-'),
    ]
    for y, label, color, direction in steps:
        if direction == '->':
            ax.annotate('', xy=(sx, y), xytext=(cx, y - 0.3),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2))
        else:
            ax.annotate('', xy=(cx, y), xytext=(sx, y - 0.3),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2))
        ax.text(4.5, y - 0.8, label, ha='center', fontsize=8, color='#333')

    save(fig, 'dhcp_process.png')


# ── 6. HTTP Persistent vs Non-Persistent ───────────────────────────────
def draw_http_connections():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 9))

    cx, sx = 2.5, 8.5  # client x, server x

    # ── LEFT: Non-Persistent (HTTP/1.0) ──
    ax1.set_xlim(0, 11)
    ax1.set_ylim(0, 15)
    ax1.axis('off')
    ax1.set_title('非持久连接 (HTTP/1.0)', fontsize=13, fontweight='bold', pad=12)

    ax1.plot([cx, cx], [0.5, 14.2], '#1565C0', lw=2)
    ax1.plot([sx, sx], [0.5, 14.2], '#C62828', lw=2)
    ax1.text(cx, 14.6, '客户端', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    ax1.text(sx, 14.6, '服务器', ha='center', fontsize=10, fontweight='bold', color='#C62828')

    objects = [('HTML', '#FF7043'), ('JPEG 1', '#66BB6A'), ('JPEG 2', '#42A5F5'), ('GIF', '#AB47BC')]
    for i, (name, color) in enumerate(objects):
        y = 13.5 - i * 3.0  # top of this object's block

        # TCP handshake: SYN → SYN-ACK → GET+ACK
        ax1.annotate('', xy=(sx, y - 0.5), xytext=(cx, y),
                     arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))
        ax1.annotate('', xy=(cx, y - 0.9), xytext=(sx, y - 0.5),
                     arrowprops=dict(arrowstyle='->', color='#555', lw=1.2))
        ax1.annotate('', xy=(sx, y - 1.3), xytext=(cx, y - 0.9),
                     arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        ax1.text(5.5, y - 0.2, 'SYN', ha='center', fontsize=6.5, color='#555')
        ax1.text(5.5, y - 0.7, 'SYN-ACK', ha='center', fontsize=6.5, color='#555')
        ax1.text(5.5, y - 1.1, f'GET {name}', ha='center', fontsize=6.5, color=color,
                 fontweight='bold')

        # Response
        ax1.annotate('', xy=(cx, y - 1.8), xytext=(sx, y - 1.3),
                     arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        ax1.text(5.5, y - 1.55, f'200 {name}', ha='center', fontsize=6.5, color=color)

        # RTT bracket
        ax1.plot([0.6, 0.6], [y, y - 0.9], '#888', lw=0.8)
        ax1.plot([0.6, 0.6], [y - 0.9, y - 1.8], '#888', lw=0.8)
        ax1.text(0.3, y - 0.45, '1 RTT', fontsize=6.5, color='#888', rotation=90, va='center')
        ax1.text(0.3, y - 1.35, '1 RTT', fontsize=6.5, color='#888', rotation=90, va='center')

        # Close indicator (except last object)
        if i < 3:
            ax1.annotate('', xy=(cx, y - 2.3), xytext=(cx, y - 1.8),
                         arrowprops=dict(arrowstyle='->', color='#BDBDBD', lw=1))
            ax1.text(cx - 0.6, y - 2.05, '× 关闭', fontsize=6, color='#999')

    ax1.text(5.5, 0.7, '每对象独立的 TCP 连接：建立 → 请求 → 响应 → 关闭\n'
                        '4 对象 × 2 RTT = 8 RTT',
             ha='center', fontsize=9, color='#C62828',
             bbox=dict(boxstyle='round', facecolor='#FFEBEE', edgecolor='#EF9A9A'))

    # ── RIGHT: Persistent + Pipelining (HTTP/1.1) ──
    ax2.set_xlim(0, 11)
    ax2.set_ylim(0, 15)
    ax2.axis('off')
    ax2.set_title('持久连接 + 流水线 (HTTP/1.1)', fontsize=13, fontweight='bold', pad=12)

    ax2.plot([cx, cx], [0.5, 14.2], '#1565C0', lw=2)
    ax2.plot([sx, sx], [0.5, 14.2], '#C62828', lw=2)
    ax2.text(cx, 14.6, '客户端', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    ax2.text(sx, 14.6, '服务器', ha='center', fontsize=10, fontweight='bold', color='#C62828')

    # RTT 1: TCP handshake
    ax2.annotate('', xy=(sx, 13.0), xytext=(cx, 13.5),
                 arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax2.annotate('', xy=(cx, 12.6), xytext=(sx, 13.0),
                 arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax2.annotate('', xy=(sx, 12.2), xytext=(cx, 12.6),
                 arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax2.text(5.5, 13.7, 'SYN', ha='center', fontsize=6.5, color='#555')
    ax2.text(5.5, 13.2, 'SYN-ACK', ha='center', fontsize=6.5, color='#555')
    ax2.text(5.5, 12.8, 'ACK', ha='center', fontsize=6.5, color='#555')
    ax2.plot([0.6, 0.6], [13.5, 12.2], '#888', lw=0.8)
    ax2.text(0.3, 12.85, 'RTT 1', fontsize=7, color='#888', rotation=90, va='center')

    # RTT 2: GET HTML + response
    ax2.annotate('', xy=(sx, 10.8), xytext=(cx, 11.2),
                 arrowprops=dict(arrowstyle='->', color='#FF7043', lw=1.5))
    ax2.annotate('', xy=(cx, 10.2), xytext=(sx, 10.8),
                 arrowprops=dict(arrowstyle='->', color='#FF7043', lw=1.5))
    ax2.text(5.5, 11.4, 'GET /index.html', ha='center', fontsize=7, color='#FF7043',
             fontweight='bold')
    ax2.text(5.5, 10.5, '200 OK (HTML)', ha='center', fontsize=7, color='#FF7043')
    ax2.plot([0.6, 0.6], [11.2, 10.2], '#888', lw=0.8)
    ax2.text(0.3, 10.7, 'RTT 2', fontsize=7, color='#888', rotation=90, va='center')

    # Parse marker
    ax2.text(5.5, 9.5, '▲ 解析 HTML，发现 3 个图片', ha='center', fontsize=7,
             color='#888', style='italic')

    # RTT 3: Pipelined requests + responses
    img_colors = [('#66BB6A', 'GET /img1.jpg', '200 (JPEG1)'),
                  ('#42A5F5', 'GET /img2.jpg', '200 (JPEG2)'),
                  ('#AB47BC', 'GET /img3.gif', '200 (GIF)')]
    for j, (clr, req, resp) in enumerate(img_colors):
        y_req = 8.8 - j * 0.35
        ax2.annotate('', xy=(sx, y_req), xytext=(cx, y_req + 0.25),
                     arrowprops=dict(arrowstyle='->', color=clr, lw=1.2))
        ax2.text(5.5, y_req + 0.3, req, ha='center', fontsize=6.2, color=clr)

        y_resp = 7.3 - j * 0.35
        ax2.annotate('', xy=(cx, y_resp), xytext=(sx, y_resp + 0.25),
                     arrowprops=dict(arrowstyle='->', color=clr, lw=1.2))
        ax2.text(5.5, y_resp + 0.3, resp, ha='center', fontsize=6.2, color=clr)

    ax2.plot([0.6, 0.6], [9.05, 6.95], '#888', lw=0.8)
    ax2.text(0.3, 8.0, 'RTT 3', fontsize=7, color='#888', rotation=90, va='center')

    # Connection lifetime bracket
    ax2.annotate('', xy=(10.3, 6.2), xytext=(10.3, 13.7),
                 arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=1.5))
    ax2.text(10.7, 9.95, '同一\nTCP\n连接', fontsize=7, color='#1565C0',
             rotation=90, va='center', ha='center')

    ax2.text(5.5, 0.7, '一次 TCP 连接，三阶段串行\n'
                        '1 (握手) + 1 (HTML) + 1 (流水线获取全部图片) = 3 RTT',
             ha='center', fontsize=9, color='#2E7D32',
             bbox=dict(boxstyle='round', facecolor='#E8F5E9', edgecolor='#A5D6A7'))

    fig.tight_layout()
    save(fig, 'http_connections.png')


# ── 7. IP Fragmentation ────────────────────────────────────────────────
def draw_ip_fragmentation():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 48)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('IP 分片示例（4000 字节数据报 → MTU 1500）', fontsize=13, fontweight='bold', pad=15)

    # Original datagram
    rect = FancyBboxPatch((0.5, 3.5), 40, 0.7, boxstyle="round,pad=0.05",
                          facecolor='#BBDEFB', edgecolor='#333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(5, 3.85, 'IP首部 20B', ha='center', fontsize=8, fontweight='bold')
    ax.plot([10.5, 10.5], [3.5, 4.2], 'k-', lw=1)
    ax.text(25, 3.85, '有效载荷 3,980 字节', ha='center', fontsize=8)
    ax.text(20.5, 4.5, '原始数据报 (4000 字节)', ha='center', fontsize=10, fontweight='bold')

    # Arrow down
    ax.annotate('', xy=(20.5, 3.3), xytext=(20.5, 4.3),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2))
    ax.text(22, 3.8, 'MTU = 1500\n分片', fontsize=7, color='#FF6F00')

    # Fragments
    colors = ['#C8E6C9', '#FFF9C4', '#FFCCBC']
    for i, (offset, mf, data_size, color) in enumerate([
        (0, 1, '1480 字节', '#C8E6C9'),
        (185, 1, '1480 字节', '#FFF9C4'),
        (370, 0, '1020 字节', '#FFCCBC'),
    ]):
        y = 2.0 - i * 0.75
        # Header portion
        rect = FancyBboxPatch((0.5, y), 10.5, 0.55, boxstyle="round,pad=0.03",
                              facecolor=color, edgecolor='#333', linewidth=1)
        ax.add_patch(rect)
        ax.text(5.75, y + 0.28, f'IP首部\n标识=x', ha='center', fontsize=6.5, fontweight='bold')
        # Data portion
        data_w = float(data_size.split()[0]) / 100  # scale
        rect = FancyBboxPatch((11, y), data_w, 0.55, boxstyle="round,pad=0.03",
                              facecolor=color, edgecolor='#333', linewidth=1, alpha=0.6)
        ax.add_patch(rect)
        ax.text(11 + data_w / 2, y + 0.28, f'数据 {data_size}', ha='center', fontsize=7)
        # Annotations
        mf_text = 'MF=0 (最后)' if mf == 0 else 'MF=1'
        ax.text(45, y + 0.28, f'分片 {i+1}\n偏移={offset}\n{mf_text}',
                ha='left', fontsize=7, va='center', color='#333')

    save(fig, 'ip_fragmentation.png')


# ── 8. Dijkstra Algorithm Visualization ────────────────────────────────
def draw_dijkstra():
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.axis('off')
    ax.set_title("Dijkstra 算法：从节点 u 计算最短路径", fontsize=13, fontweight='bold', pad=15)

    # Node positions (a rough topology)
    nodes = {
        'u': (0, 4), 'v': (-2, 1), 'w': (0, 0), 'x': (2, -1),
        'y': (-3, -2), 'z': (1, -3)
    }
    # Edges with weights
    edges = [
        ('u', 'v', 2), ('u', 'w', 5), ('u', 'x', 1),
        ('v', 'w', 3), ('v', 'y', 6),
        ('w', 'x', 3), ('w', 'y', 1), ('w', 'z', 5),
        ('x', 'z', 3),
        ('y', 'z', 2)
    ]
    # Shortest path from u (precomputed): u→x:1, u→v:2, u→w:4, u→y:5, u→z:6
    shortest = {('u','x'): 1, ('u','v'): 2, ('w','y'): 1, ('y','z'): 2,
                ('x','z'): 3, ('v','w'): 3, ('u','w'): 4, ('u','y'): 5, ('u','z'): 6}

    # Draw all edges
    for a, b, w in edges:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        ax.plot([x1, x2], [y1, y2], '#BDBDBD', linewidth=1.5)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.1, my + 0.1, str(w), fontsize=8, color='#757575',
                bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none', alpha=0.7))

    # Highlight shortest path edges
    sp_edges = [('u','x'), ('x','z'), ('z','y'), ('y','w'), ('u','v')]
    for a, b in sp_edges:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        ax.plot([x1, x2], [y1, y2], '#FF6F00', linewidth=3, alpha=0.7)

    # Draw nodes
    for name, (x, y) in nodes.items():
        circle = plt.Circle((x, y), 0.4, facecolor='#42A5F5' if name != 'u' else '#FF7043',
                            edgecolor='#333', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=12, fontweight='bold',
                color='white' if name != 'u' else 'white')

    # Legend
    leg_elements = [mpatches.Patch(color='#FF7043', label='源节点 u'),
                    mpatches.Patch(color='#FF6F00', label='最短路径边')]
    ax.legend(handles=leg_elements, loc='lower right', fontsize=8)

    # Show distance table
    table_text = "从 u 的最短距离:\n  u→u: 0  |  u→x: 1  |  u→v: 2\n  u→w: 4  |  u→y: 5  |  u→z: 6"
    ax.text(-4.5, -4.5, table_text, fontsize=9,
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', edgecolor='#BDBDBD'))

    save(fig, 'dijkstra.png')


# ── 9. OSPF Area Hierarchy ─────────────────────────────────────────────
def draw_ospf_areas():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('OSPF 区域分层结构', fontsize=14, fontweight='bold', pad=15)

    # Backbone area 0
    backbone = FancyBboxPatch((3.5, 3.5), 5, 3.5, boxstyle="round,pad=0.2",
                               facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(backbone)
    ax.text(6, 6.7, '区域 0 (骨干区域, Backbone)', ha='center', fontsize=11, fontweight='bold', color='#1565C0')

    # Area border routers
    for x, y in [(4, 4), (8, 4)]:
        circle = plt.Circle((x, y), 0.25, facecolor='#FF7043', edgecolor='#333', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, y - 0.6, f'ABR', ha='center', fontsize=7, fontweight='bold', color='#FF7043')

    # Area 1
    area1 = FancyBboxPatch((1, 1.5), 3, 2, boxstyle="round,pad=0.15",
                            facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.5)
    ax.add_patch(area1)
    ax.text(2.5, 2.2, '区域 1', ha='center', fontsize=10, fontweight='bold', color='#F9A825')

    # Area 2
    area2 = FancyBboxPatch((8, 1.5), 3, 2, boxstyle="round,pad=0.15",
                            facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(area2)
    ax.text(9.5, 2.2, '区域 2', ha='center', fontsize=10, fontweight='bold', color='#2E7D32')

    # Internal routers in areas
    for ax_pos, ay in [((1.8, 2.3), 'R1'), ((3.2, 2.3), 'R2')]:
        x, y_local = ax_pos
        circle = plt.Circle((x, y_local), 0.2, facecolor='#90CAF9', edgecolor='#333', linewidth=1)
        ax.add_patch(circle)
        ax.text(x, y_local, 'R', ha='center', va='center', fontsize=7, fontweight='bold')

    for ax_pos, ay in [((8.5, 2.3), 'R3'), ((9.8, 2.3), 'R4')]:
        x, y_local = ax_pos
        circle = plt.Circle((x, y_local), 0.2, facecolor='#A5D6A7', edgecolor='#333', linewidth=1)
        ax.add_patch(circle)
        ax.text(x, y_local, 'R', ha='center', va='center', fontsize=7, fontweight='bold')

    # Connect areas to ABRs
    ax.plot([2.5, 4], [3.6, 4], 'k--', lw=1, alpha=0.5)
    ax.plot([9.5, 8], [3.6, 4], 'k--', lw=1, alpha=0.5)

    # Labels
    ax.text(2.5, 1, '区域内路由器\n运行链路状态泛洪', ha='center', fontsize=7, color='#555')
    ax.text(9.5, 1, '区域内路由器\n运行链路状态泛洪', ha='center', fontsize=7, color='#555')
    ax.text(6, 3.2, 'ABR: 连接骨干与区域，汇总路由', ha='center', fontsize=8, color='#FF7043')

    save(fig, 'ospf_areas.png')


# ── 10. BGP Topology ───────────────────────────────────────────────────
def draw_bgp():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('BGP 域间路由：AS 互联与 BGP 会话', fontsize=14, fontweight='bold', pad=15)

    # AS clouds
    as_data = [
        (1.5, 4.5, 'AS 100\n(ISP-A)', '#BBDEFB'),
        (5.5, 4.5, 'AS 200\n(ISP-B)', '#C8E6C9'),
        (9.5, 4.5, 'AS 300\n(ISP-C)', '#FFCCBC'),
        (5.5, 1.5, 'AS 400\n(客户网络)', '#E1BEE7'),
    ]

    for x, y, label, color in as_data:
        ellipse = mpatches.Ellipse((x, y), 3.5, 2.5, facecolor=color,
                                     edgecolor='#333', linewidth=2, alpha=0.7)
        ax.add_patch(ellipse)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')

    # BGP routers
    router_positions = [
        (2.5, 5.2, 'R1'), (4.5, 5.2, 'R2'),
        (6.5, 5.2, 'R3'), (8.5, 5.2, 'R4'),
        (5.5, 2.2, 'R5'),
    ]
    for x, y, name in router_positions:
        circle = plt.Circle((x, y), 0.18, facecolor='#FF7043', edgecolor='#333', linewidth=1)
        ax.add_patch(circle)
        ax.text(x, y + 0.4, name, ha='center', fontsize=8, fontweight='bold')

    # eBGP sessions
    ax.plot([4.5, 6.5], [5.2, 5.2], '#F44336', lw=2)
    ax.text(5.5, 5.7, 'eBGP', ha='center', fontsize=8, color='#F44336', fontweight='bold')

    ax.plot([8.5, 9.5], [5.2, 4.8], '#F44336', lw=2)
    ax.text(9.2, 5.6, 'eBGP', ha='center', fontsize=8, color='#F44336', fontweight='bold')

    ax.plot([5.5, 5.5], [4, 2.7], '#F44336', lw=2)
    ax.text(6, 3.5, 'eBGP', ha='center', fontsize=8, color='#F44336', fontweight='bold')

    # iBGP sessions
    ax.plot([2.5, 4.5], [5.2, 5.2], '#1565C0', lw=1.5, ls='--')
    ax.text(3.5, 5.7, 'iBGP', ha='center', fontsize=7, color='#1565C0')

    ax.plot([6.5, 8.5], [5.2, 5.2], '#1565C0', lw=1.5, ls='--')
    ax.text(7.5, 5.7, 'iBGP', ha='center', fontsize=7, color='#1565C0')

    # Legend
    leg = [mpatches.Patch(color='#F44336', label='eBGP (跨 AS)'),
           mpatches.Patch(color='#1565C0', label='iBGP (AS 内部)')]
    ax.legend(handles=leg, loc='lower center', fontsize=8, ncol=2)

    # Annotation
    ax.text(5.5, 0.5, 'BGP 运行在 TCP 端口 179 上，传播路由可达性信息（前缀 + 属性）',
            ha='center', fontsize=8, color='#555', style='italic')

    save(fig, 'bgp_topology.png')


# ── 11. DNS Resolution Process ─────────────────────────────────────────
def draw_dns():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.axis('off')
    ax.set_title('DNS 解析过程（迭代查询）', fontsize=14, fontweight='bold', pad=15)

    # Vertical lines for each entity
    entities = [
        (1.5, '客户端\n(主机)', '#1565C0'),
        (4.5, '本地 DNS\n服务器', '#6A1B9A'),
        (8.0, '根 DNS\n服务器', '#FF7043'),
        (10.5, 'TLD DNS\n(.com)', '#FFA726'),
        (13.0, '权威 DNS\n(amazon.com)', '#66BB6A'),
    ]

    for x, label, color in entities:
        ax.plot([x, x], [1, 10], color, lw=2)
        ax.text(x, 10.5, label, ha='center', fontsize=8, fontweight='bold', color=color)

    # Draw arrows with labels: (from_x, to_x, y, label, color, direction_offset)
    # Step 1: Client → Local DNS (recursive query)
    ax.annotate('', xy=(4.5, 9.2), xytext=(1.5, 9.2),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.8))
    ax.text(3.0, 9.6, '① 递归查询\nwww.amazon.com', ha='center', fontsize=7, color='#1565C0')

    # Step 2: Local DNS → Root DNS
    ax.annotate('', xy=(8.0, 8.2), xytext=(4.5, 8.2),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.text(6.25, 8.6, '② 查询 .com 的 NS', ha='center', fontsize=7, color='#333')

    # Step 3: Root DNS → Local DNS (referral to TLD)
    ax.annotate('', xy=(4.5, 7.3), xytext=(8.0, 7.3),
                arrowprops=dict(arrowstyle='->', color='#FF7043', lw=1.5))
    ax.text(6.25, 7.7, '③ 返回 .com TLD 地址', ha='center', fontsize=7, color='#FF7043')

    # Step 4: Local DNS → TLD DNS
    ax.annotate('', xy=(10.5, 6.3), xytext=(4.5, 6.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.text(7.5, 6.7, '④ 查询 amazon.com 的 NS', ha='center', fontsize=7, color='#333')

    # Step 5: TLD DNS → Local DNS (referral to authoritative)
    ax.annotate('', xy=(4.5, 5.4), xytext=(10.5, 5.4),
                arrowprops=dict(arrowstyle='->', color='#FFA726', lw=1.5))
    ax.text(7.5, 5.8, '⑤ 返回权威 DNS 地址', ha='center', fontsize=7, color='#FFA726')

    # Step 6: Local DNS → Authoritative DNS
    ax.annotate('', xy=(13.0, 4.3), xytext=(4.5, 4.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.text(8.75, 4.7, '⑥ 查询 www.amazon.com 的 A 记录', ha='center', fontsize=7, color='#333')

    # Step 7: Authoritative DNS → Local DNS (answer)
    ax.annotate('', xy=(4.5, 3.4), xytext=(13.0, 3.4),
                arrowprops=dict(arrowstyle='->', color='#66BB6A', lw=1.5))
    ax.text(8.75, 3.8, '⑦ 返回 IP 地址', ha='center', fontsize=7, color='#66BB6A')

    # Step 8: Local DNS → Client (answer)
    ax.annotate('', xy=(1.5, 2.3), xytext=(4.5, 2.3),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=1.8))
    ax.text(3.0, 2.7, '⑧ 返回 IP 地址', ha='center', fontsize=7, color='#6A1B9A')

    # Annotation
    ax.text(7.25, 1.0, '客户端 → 本地 DNS：递归查询（黑盒）   本地 DNS → 各级服务器：迭代查询',
            ha='center', fontsize=8, color='#555',
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', edgecolor='#BDBDBD'))

    save(fig, 'dns_resolution.png')


# ── DNS Query Types: Recursive vs Iterative ────────────────────────────
def draw_dns_query_types():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 9))

    # Common entity config
    entities = [
        (0.15, '客户端\n(主机)', '#1565C0'),
        (0.38, '本地 DNS\n服务器', '#6A1B9A'),
        (0.62, '根 DNS\n服务器', '#FF7043'),
        (0.82, '权威 DNS\n服务器', '#66BB6A'),
    ]

    # ── Panel 1: Recursive Query ──
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')
    ax1.set_title('递归查询 (Recursive Query)', fontsize=13, fontweight='bold', pad=12,
                  color='#6A1B9A')

    for x, label, color in entities:
        ax1.axvline(x=x, ymin=0.05, ymax=0.88, color=color, lw=2)
        ax1.text(x, 0.93, label, ha='center', fontsize=8, fontweight='bold', color=color)

    # Recursive: chain down then back up
    # Host → Local (query goes down)
    ax1.annotate('', xy=(0.38, 0.78), xytext=(0.15, 0.82),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax1.text(0.265, 0.84, '查询', ha='center', fontsize=7, color='#1565C0')

    # Local → Root (local forwards query)
    ax1.annotate('', xy=(0.62, 0.70), xytext=(0.38, 0.74),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=2))
    ax1.text(0.50, 0.76, '代为查询', ha='center', fontsize=7, color='#6A1B9A')

    # Root → Auth (root forwards query further)
    ax1.annotate('', xy=(0.82, 0.62), xytext=(0.62, 0.66),
                arrowprops=dict(arrowstyle='->', color='#FF7043', lw=2))
    ax1.text(0.72, 0.68, '代为查询', ha='center', fontsize=7, color='#FF7043')

    # Answer comes back up: Auth → Root
    ax1.annotate('', xy=(0.62, 0.54), xytext=(0.82, 0.50),
                arrowprops=dict(arrowstyle='->', color='#66BB6A', lw=2, linestyle='dashed'))
    ax1.text(0.72, 0.47, '结果', ha='center', fontsize=7, color='#66BB6A')

    # Root → Local
    ax1.annotate('', xy=(0.38, 0.42), xytext=(0.62, 0.38),
                arrowprops=dict(arrowstyle='->', color='#FF7043', lw=2, linestyle='dashed'))
    ax1.text(0.50, 0.35, '结果', ha='center', fontsize=7, color='#FF7043')

    # Local → Host
    ax1.annotate('', xy=(0.15, 0.30), xytext=(0.38, 0.26),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=2, linestyle='dashed'))
    ax1.text(0.265, 0.23, '最终结果', ha='center', fontsize=7, color='#6A1B9A')

    # Annotation box
    ax1.text(0.5, 0.08, '被查询的服务器接过查询负担\n沿层次链逐级向下传递\n最终结果沿原路返回',
             ha='center', fontsize=8, color='#555',
             bbox=dict(boxstyle='round', facecolor='#F3E5F5', edgecolor='#CE93D8'))
    ax1.text(0.5, 0.97, '■■■ 每台 DNS 服务器为上一级承担全部工作 ■■■',
             ha='center', fontsize=7, color='#888')

    # ── Panel 2: Iterative Query ──
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    ax2.set_title('迭代查询 (Iterative Query)', fontsize=13, fontweight='bold', pad=12,
                  color='#E65100')

    for x, label, color in entities:
        ax2.axvline(x=x, ymin=0.05, ymax=0.88, color=color, lw=2)
        ax2.text(x, 0.93, label, ha='center', fontsize=8, fontweight='bold', color=color)

    # Iterative: local DNS does all the chasing
    # Host → Local
    ax2.annotate('', xy=(0.38, 0.82), xytext=(0.15, 0.82),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax2.text(0.265, 0.86, '查询', ha='center', fontsize=7, color='#1565C0')

    # Local → Root (query 1)
    ax2.annotate('', xy=(0.62, 0.72), xytext=(0.38, 0.72),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=1.8))
    ax2.text(0.50, 0.76, '① 查询', ha='center', fontsize=7, color='#6A1B9A')
    # Root → Local (referral, back to local)
    ax2.annotate('', xy=(0.38, 0.66), xytext=(0.62, 0.66),
                arrowprops=dict(arrowstyle='->', color='#FF7043', lw=1.5, linestyle='dashed'))
    ax2.text(0.50, 0.62, '② "去问 .com TLD"', ha='center', fontsize=7, color='#FF7043')

    # Local → TLD-like (query 2) — reuse "权威" as the next hop
    ax2.annotate('', xy=(0.82, 0.56), xytext=(0.38, 0.56),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=1.8))
    ax2.text(0.60, 0.60, '③ 查询', ha='center', fontsize=7, color='#6A1B9A')
    # Auth → Local (referral again)
    ax2.annotate('', xy=(0.38, 0.50), xytext=(0.82, 0.50),
                arrowprops=dict(arrowstyle='->', color='#FFA726', lw=1.5, linestyle='dashed'))
    ax2.text(0.60, 0.46, '④ "去问权威 DNS"', ha='center', fontsize=7, color='#FFA726')

    # Local → Final (query 3 — final answer)
    ax2.annotate('', xy=(0.62, 0.40), xytext=(0.38, 0.40),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=1.8))
    ax2.text(0.50, 0.44, '⑤ 查询', ha='center', fontsize=7, color='#6A1B9A')
    # Auth → Local (answer)
    ax2.annotate('', xy=(0.38, 0.34), xytext=(0.62, 0.34),
                arrowprops=dict(arrowstyle='->', color='#66BB6A', lw=2, linestyle='dashed'))
    ax2.text(0.50, 0.30, '⑥ 返回 IP', ha='center', fontsize=7, color='#66BB6A')

    # Local → Host (answer)
    ax2.annotate('', xy=(0.15, 0.22), xytext=(0.38, 0.22),
                arrowprops=dict(arrowstyle='->', color='#6A1B9A', lw=2, linestyle='dashed'))
    ax2.text(0.265, 0.18, '返回 IP', ha='center', fontsize=7, color='#6A1B9A')

    # Annotation box
    ax2.text(0.5, 0.08, '被查询的服务器只返回下一步线索\n本地 DNS 自行向每个服务器逐一查询\n根和 TLD 只需处理简单的迭代请求',
             ha='center', fontsize=8, color='#555',
             bbox=dict(boxstyle='round', facecolor='#FFF3E0', edgecolor='#FFCC80'))
    ax2.text(0.5, 0.97, '■■■ 本地 DNS 承担全部追踪工作 ■■■',
             ha='center', fontsize=7, color='#888')

    plt.tight_layout()
    save(fig, 'dns_query_types.png')


# ── Domain Name Hierarchy ──────────────────────────────────────────────
def draw_domain_hierarchy():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('域名层次结构（从右向左阅读）', fontsize=14, fontweight='bold', pad=15)

    # Example domain name displayed at top
    ax.text(7, 7.3, 'gaia  .  cs  .  umass  .  edu', ha='center', fontsize=16,
            fontweight='bold', family='monospace', color='#333')
    ax.text(7, 6.7, '主机名    子域    二级域   顶级域', ha='center', fontsize=9, color='#888')

    # Draw hierarchy as nested boxes from right (TLD) to left (hostname)
    levels = [
        (10.5, 2, 6.0, 2.5, '顶级域 (TLD)\nedu', '#FF7043', '由 TLD 注册管理机构维护\n(如 Verisign 管理 .com)'),
        (7.5, 2, 5.4, 2.5, '二级域\numass', '#FFA726', '由该域的权威 DNS 服务器管理\n(注册时指定)'),
        (4.5, 2, 4.8, 2.5, '子域\ncs', '#66BB6A', '由上级域自行划分\n(umass.edu 管理 cs.umass.edu)'),
        (1.5, 2, 4.2, 2.5, '主机名\ngaia', '#42A5F5', '具体的一台机器\n(通常为 A/AAAA 记录)'),
    ]

    for cx, cy, w, h, label, color, note in levels:
        rect = FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                              boxstyle='round,pad=0.15', facecolor=color, edgecolor='#333',
                              linewidth=2, alpha=0.25)
        ax.add_patch(rect)
        ax.text(cx, cy + 0.15, label, ha='center', va='center', fontsize=10,
                fontweight='bold', color='#333')

    # Root indicator at top
    ax.text(7, 5.2, '根 (Root) "."', ha='center', fontsize=9, color='#999')
    ax.plot([7, 7], [5.0, 5.0], '.', color='#999', markersize=8)

    # Reading direction arrow
    ax.annotate('', xy=(13.2, 5.5), xytext=(0.8, 5.5),
                arrowprops=dict(arrowstyle='->', color='#E53935', lw=2.5))
    ax.text(7, 5.9, '← 从右向左阅读（最宏观 → 最具体）', ha='center', fontsize=9,
            color='#E53935', fontweight='bold')

    # Bottom note: which server knows what
    ax.axhline(y=1.3, xmin=0.1, xmax=0.9, color='#E0E0E0', lw=1)
    ax.text(7, 0.7, '根服务器 → 知道所有 TLD 服务器地址    TLD 服务器 → 知道每个注册域名的权威 DNS 地址    权威 DNS → 存储该域的实际记录 (A, MX, CNAME...)',
            ha='center', fontsize=7.5, color='#777')

    save(fig, 'domain_hierarchy.png')


# ── DNS Delegation (subdomain authoritative) ───────────────────────────
def draw_dns_delegation():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 13)
    ax.axis('off')
    ax.set_title('DNS 查询：子域委托（10 条消息）', fontsize=14, fontweight='bold', pad=15)

    entities = [
        (1.5, '客户端\ncis.poly.edu', '#1565C0'),
        (3.5, '本地 DNS\n(dns.poly.edu)', '#6A1B9A'),
        (6.5, '根 DNS\n服务器', '#FF7043'),
        (9.5, '.edu\nTLD 服务器', '#FFA726'),
        (12.5, '校级权威\n(dns.umass.edu)', '#66BB6A'),
        (15.0, '系级权威\n(dns.cs.umass.edu)', '#E53935'),
    ]

    for x, label, color in entities:
        ax.plot([x, x], [1, 12], color, lw=2)
        ax.text(x, 12.5, label, ha='center', fontsize=7.5, fontweight='bold', color=color)

    # Step annotations: (from_x, to_x, y, label, color)
    steps = [
        (1.5, 3.5, 11.2, '① 递归查询\ngaia.cs.umass.edu', '#1565C0'),
        (3.5, 6.5, 10.2, '② 迭代查询', '#333'),
        (6.5, 3.5, 9.3, '③ 返回 .edu TLD 地址', '#FF7043'),
        (3.5, 9.5, 8.3, '④ 迭代查询', '#333'),
        (9.5, 3.5, 7.4, '⑤ 返回 dns.umass.edu', '#FFA726'),
        (3.5, 12.5, 6.3, '⑥ 迭代查询\ngaia.cs.umass.edu', '#333'),
        (12.5, 3.5, 5.4, '⑦ NS: cs.umass.edu\n→ dns.cs.umass.edu', '#66BB6A'),
        (3.5, 15.0, 4.3, '⑧ 迭代查询\ngaia.cs.umass.edu', '#333'),
        (15.0, 3.5, 3.3, '⑨ A: IP 地址', '#E53935'),
        (3.5, 1.5, 2.3, '⑩ 返回 IP 地址', '#6A1B9A'),
    ]

    for fx, tx, y, label, color in steps:
        ax.annotate('', xy=(tx, y), xytext=(fx, y),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
        mx = (fx + tx) / 2
        ax.text(mx, y + 0.35, label, ha='center', fontsize=6.5, color=color)

    # Highlight the delegation step
    ax.annotate('', xy=(2.5, 5.0), xytext=(2.5, 6.15),
                arrowprops=dict(arrowstyle='->', color='#E53935', lw=2, ls='dashed'))
    ax.text(2.7, 5.5, '⑦ 是委托关键：\n校级返回系级权威\n而非 A 记录', fontsize=7, color='#E53935', fontweight='bold')

    # Bottom note
    ax.text(8.25, 1.0, '简化版 8 条消息（无委托） vs  委托版 10 条消息（多一跳子域权威）',
            ha='center', fontsize=8.5, color='#555',
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', edgecolor='#BDBDBD'))

    # Legend at bottom right
    ax.text(14.8, 0.4, 'NS 记录：\n(cs.umass.edu,\ndns.cs.umass.edu, NS)',
            fontsize=6.5, color='#66BB6A', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#E8F5E9', edgecolor='#A5D6A7'))

    save(fig, 'dns_delegation.png')


# ── 12. Packet Scheduling Comparison ───────────────────────────────────
def draw_scheduling():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    titles = ['FIFO (先到先服务)', '优先权排队 (Priority)', '轮询 (Round Robin)', '加权公平排队 (WFQ)']
    for idx, (ax, title) in enumerate(zip(axes, titles)):
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 4)
        ax.axis('off')
        ax.set_title(title, fontsize=11, fontweight='bold')

        if idx == 0:  # FIFO
            packets = [('1', '#BBDEFB'), ('2', '#C8E6C9'), ('3', '#FFCCBC')]
            for i, (label, color) in enumerate(packets):
                rect = FancyBboxPatch((i * 3.5 + 0.5, 2), 3, 0.8, boxstyle="round,pad=0.05",
                                      facecolor=color, edgecolor='#333', linewidth=1)
                ax.add_patch(rect)
                ax.text(i * 3.5 + 2, 2.4, f'分组 {label}', ha='center', fontsize=8)
            ax.annotate('', xy=(0.5, 1.2), xytext=(11, 1.2),
                        arrowprops=dict(arrowstyle='->', color='#333', lw=2))
            ax.text(5.75, 0.7, '到达顺序 = 发送顺序', ha='center', fontsize=8, color='#555')

        elif idx == 1:  # Priority
            rect = FancyBboxPatch((0.5, 2.5), 10, 0.8, boxstyle="round,pad=0.05",
                                  facecolor='#FFCCBC', edgecolor='#333', linewidth=1)
            ax.add_patch(rect)
            ax.text(5.5, 2.9, '高优先权队列 (优先发送)', ha='center', fontsize=9, fontweight='bold')
            rect = FancyBboxPatch((0.5, 1.2), 10, 0.8, boxstyle="round,pad=0.05",
                                  facecolor='#BBDEFB', edgecolor='#333', linewidth=1)
            ax.add_patch(rect)
            ax.text(5.5, 1.6, '低优先权队列 (仅当高优先权为空时发送)', ha='center', fontsize=9)
            ax.annotate('', xy=(5.5, 1.9), xytext=(5.5, 3.3),
                        arrowprops=dict(arrowstyle='<->', color='#FF6F00', lw=2))
            ax.text(7, 2.6, '饥饿风险', fontsize=8, color='#FF6F00')

        elif idx == 2:  # RR
            packets = [('1', '#BBDEFB'), ('2', '#C8E6C9'), ('3', '#FFCCBC'),
                       ('1', '#BBDEFB'), ('2', '#C8E6C9')]
            for i, (label, color) in enumerate(packets):
                rect = FancyBboxPatch((i * 2.2 + 0.3, 2), 1.8, 0.8, boxstyle="round,pad=0.05",
                                      facecolor=color, edgecolor='#333', linewidth=1)
                ax.add_patch(rect)
                ax.text(i * 2.2 + 1.2, 2.4, f'C{label}', ha='center', fontsize=7)
            ax.text(5.5, 0.7, '每个队列轮询发送一个分组', ha='center', fontsize=8, color='#555')

        elif idx == 3:  # WFQ
            bars = [('C1 (40%)', 2.5, '#BBDEFB'), ('C2 (35%)', 5, '#C8E6C9'), ('C3 (25%)', 7.5, '#FFCCBC')]
            for label, x, color in bars:
                rect = FancyBboxPatch((x - 1, 1.5), 2, 1.5, boxstyle="round,pad=0.05",
                                      facecolor=color, edgecolor='#333', linewidth=1)
                ax.add_patch(rect)
                ax.text(x, 2.25, label, ha='center', fontsize=8, fontweight='bold')
            ax.text(5.5, 0.7, '根据权重分配带宽，保证最小带宽份额', ha='center', fontsize=8, color='#555')

    fig.tight_layout()
    save(fig, 'packet_scheduling.png')


# ── 13. TCP Congestion Control Sawtooth ──────────────────────────────────
def draw_tcp_congestion_control():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_title('TCP 拥塞控制：cwnd 随时间变化的锯齿图', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('时间 (RTT)', fontsize=11)
    ax.set_ylabel('cwnd (MSS)', fontsize=11)
    ax.set_xlim(0, 26)
    ax.set_ylim(0, 42)
    ax.grid(True, alpha=0.3)

    # Trace ssthresh changes explicitly
    rtts = []
    cwnd = []
    sst_vals = []  # ssthresh at each point
    t = 0
    w = 1
    ssthresh = 32

    # Slow start
    while w < ssthresh and t < 5:
        rtts.append(t); cwnd.append(w); sst_vals.append(ssthresh)
        w *= 2; t += 1
    # Congestion avoidance
    while t < 12:
        rtts.append(t); cwnd.append(w); sst_vals.append(ssthresh)
        w += 1; t += 1

    # 3 dup ACK: ssthresh = cwnd/2, cwnd = ssthresh + 3 (enter fast recovery)
    ssthresh = w // 2        # e.g. w=33 → 16
    w_prev = w
    w = ssthresh             # exit fast recovery to congestion avoidance
    # Plot the 3-dup-ACK drop
    rtts.append(t); cwnd.append(w_prev); sst_vals.append(ssthresh)
    t += 1
    # Fast recovery: cwnd deflates to ssthresh
    rtts.append(t); cwnd.append(ssthresh); sst_vals.append(ssthresh)
    t += 1

    # Congestion avoidance again
    while t < 22:
        rtts.append(t); cwnd.append(w); sst_vals.append(ssthresh)
        w += 1; t += 1

    # Timeout: ssthresh = cwnd/2, cwnd = 1
    ssthresh = w // 2
    w = 1
    rtts.append(t); cwnd.append(1); sst_vals.append(ssthresh)
    t += 1
    # Slow start
    while t < 26:
        rtts.append(t); cwnd.append(w); sst_vals.append(ssthresh)
        w *= 2; t += 1

    ax.step(rtts, cwnd, where='post', color='#1565C0', linewidth=2.5, label='cwnd')

    # Draw ssthresh as a dashed step line using actual computed values
    ax.step(rtts, sst_vals, where='post', color='#FF6F00', linestyle='dashed',
            linewidth=1.5, label='ssthresh')

    # Annotations
    ax.annotate('慢启动\n(指数增长)', xy=(3, 8), fontsize=8, color='#2E7D32',
                bbox=dict(boxstyle='round', facecolor='#C8E6C9', alpha=0.8))
    ax.annotate('拥塞避免\n(AIMD线性增长)', xy=(9, 32), fontsize=8, color='#1565C0',
                bbox=dict(boxstyle='round', facecolor='#BBDEFB', alpha=0.8))
    ax.annotate('3 dup ACK\n→快速恢复', xy=(14, 22), fontsize=8, color='#E65100',
                bbox=dict(boxstyle='round', facecolor='#FFCCBC', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=1.5))
    ax.annotate('超时\ncwnd=1', xy=(23, 2), fontsize=8, color='#C62828',
                bbox=dict(boxstyle='round', facecolor='#FFCDD2', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.5))
    ax.annotate('慢启动\n(指数)', xy=(24.5, 8), fontsize=8, color='#2E7D32',
                bbox=dict(boxstyle='round', facecolor='#C8E6C9', alpha=0.8))

    ax.legend(loc='upper left', fontsize=9)
    save(fig, 'tcp_congestion_control.png')


# ── 14. TCP Header Structure ─────────────────────────────────────────────
def draw_tcp_header():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('TCP 报文段首部格式', fontsize=14, fontweight='bold', pad=20)

    fields = [
        ("源端口号 Source Port (16bit)", 0, 16, 7, 1, '#FFE0B2'),
        ("目的端口号 Dest Port (16bit)", 16, 32, 7, 1, '#FFE0B2'),
        ("序号 Sequence Number (32bit)", 0, 32, 6, 1, '#C8E6C9'),
        ("确认号 Acknowledgment Number (32bit)", 0, 32, 5, 1, '#C8E6C9'),
        ("首部长度(4)\n保留(6)", 0, 8, 4, 1, '#BBDEFB'),
        ("U R G", 8, 9.6, 4, 1, '#FFCDD2'),
        ("A C K", 9.6, 11.2, 4, 1, '#FFCDD2'),
        ("P S H", 11.2, 12.8, 4, 1, '#FFCDD2'),
        ("R S T", 12.8, 14.4, 4, 1, '#FFCDD2'),
        ("S Y N", 14.4, 16.0, 4, 1, '#FFCDD2'),
        ("F I N", 16.0, 17.6, 4, 1, '#FFCDD2'),
        ("接收窗口 Receive Window (16bit)", 17.6, 32, 4, 1, '#BBDEFB'),
        ("检验和 Checksum (16bit)", 0, 16, 3, 1, '#E1BEE7'),
        ("紧急指针 Urgent Pointer (16bit)", 16, 32, 3, 1, '#E1BEE7'),
        ("选项 Options（可变长度，很少使用）", 0, 32, 2, 1, '#E0E0E0'),
        ("数据 Data（有效载荷）", 0, 32, 1, 1, '#FFCDD2'),
    ]

    for name, x0, x1, y0, h, color in fields:
        rect = FancyBboxPatch((x0, y0 - 0.5), x1 - x0, h,
                              boxstyle="round,pad=0.05", facecolor=color,
                              edgecolor='#333', linewidth=0.8)
        ax.add_patch(rect)
        cx = (x0 + x1) / 2
        cy = y0 - 0.5 + h / 2
        fs = 7 if len(name) > 30 else 8
        ax.text(cx, cy, name, ha='center', va='center', fontsize=fs, fontweight='normal')

    ax.text(16, 7.8, '32 比特', ha='center', fontsize=10, fontstyle='italic', color='#555')
    for i in range(5):
        x = i * 8
        ax.plot([x, x], [0.5, 7.7], 'k--', linewidth=0.4, alpha=0.3)
    ax.text(16, -0.3, '← 首部（通常 20 字节）→', ha='center', fontsize=9, color='#555')
    save(fig, 'tcp_header.png')


# ── 14b. TCP Checksum Coverage ─────────────────────────────────────────────
def draw_tcp_checksum_coverage():
    """Show the pseudo-header + TCP segment coverage of the TCP checksum."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('TCP 检验和的计算覆盖范围', fontsize=14, fontweight='bold', pad=20)

    # Three blocks: pseudo-header, TCP header, data
    blocks = [
        (2, 7, 6, 2.0, '#E3F2FD', '伪首部（虚拟，不传输）\n'
         '源 IP 地址 (32 bit)\n'
         '目的 IP 地址 (32 bit)\n'
         '全零 (8 bit) | 协议号 = 6 (8 bit)\n'
         'TCP 报文段长度 (16 bit)'),
        (2, 4.5, 6, 2.0, '#E1BEE7', 'TCP 首部（实际传输）\n'
         '源端口 + 目的端口\n'
         '序号 + 确认号\n'
         '首部长度 + 标志 + 窗口\n'
         '检验和 (计算时此格填 0) + 紧急指针\n'
         '选项（如有）'),
        (2, 2, 6, 2.0, '#FFCDD2', 'TCP 数据（实际传输）\n应用层载荷'),
    ]

    for x, y, w, h, color, label in blocks:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=8, color='#333')

    # Big brace on the right: "checksum coverage"
    ax.plot([8.8, 9.2, 9.2, 8.8], [1.8, 1.8, 9.2, 9.2], 'k-', linewidth=1.5)
    ax.text(9.8, 5.5, '检验和\n计算\n覆盖\n范围', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#333',
            bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.2))

    # Dotted line separating virtual from actual
    ax.plot([1.5, 8.5], [4.2, 4.2], 'k--', linewidth=1, alpha=0.4)
    ax.text(5, 4.05, '———— 仅以上为虚拟，不进入网络 ————', ha='center', fontsize=7, color='#888')

    # Annotation: pseudo-header borrowed from IP
    ax.annotate('从 IP 层获取', xy=(2, 8.2), fontsize=7, color='#1565C0',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#1565C0', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1))

    save(fig, 'tcp_checksum_coverage.png')


# ── 15. UDP Header Structure ─────────────────────────────────────────────
def draw_udp_header():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('UDP 报文段结构', fontsize=14, fontweight='bold', pad=20)

    fields = [
        ("源端口号 (16bit)", 0, 16, 4, 1, '#FFE0B2'),
        ("目的端口号 (16bit)", 16, 32, 4, 1, '#FFE0B2'),
        ("长度 Length (16bit)", 0, 16, 3, 1, '#C8E6C9'),
        ("检验和 Checksum (16bit)", 16, 32, 3, 1, '#C8E6C9'),
        ("应用数据（有效载荷）", 0, 32, 1.5, 1.5, '#FFCDD2'),
    ]

    for name, x0, x1, y0, h, color in fields:
        rect = FancyBboxPatch((x0, y0 - 0.5), x1 - x0, h,
                              boxstyle="round,pad=0.05", facecolor=color,
                              edgecolor='#333', linewidth=0.8)
        ax.add_patch(rect)
        cx = (x0 + x1) / 2
        cy = y0 - 0.5 + h / 2
        ax.text(cx, cy, name, ha='center', va='center', fontsize=9, fontweight='normal')

    ax.text(16, 4.8, '32 比特', ha='center', fontsize=10, fontstyle='italic', color='#555')
    ax.text(16, 0.25, '← 首部仅 8 字节 →', ha='center', fontsize=9, color='#555')
    save(fig, 'udp_header.png')


# ── 15b. UDP Checksum Coverage (Pseudo-Header) ──────────────────────────
def draw_udp_checksum_coverage():
    """Show the pseudo-header + UDP segment coverage of the UDP checksum."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('UDP 检验和的计算覆盖范围（含伪首部）', fontsize=14, fontweight='bold', pad=20)

    # Three blocks: pseudo-header, UDP header, data
    blocks = [
        (2, 7, 6, 2.0, '#E3F2FD', '伪首部（Pseudo-Header，虚拟，不传输）\n'
         '源 IP 地址 (32 bit)\n'
         '目的 IP 地址 (32 bit)\n'
         '全零 (8 bit) | 协议号 = 17 (8 bit)\n'
         'UDP 报文段长度 (16 bit)'),
        (2, 5, 6, 1.5, '#E1BEE7', 'UDP 首部（实际传输，8 字节）\n'
         '源端口号 (16 bit) + 目的端口号 (16 bit)\n'
         '长度 (16 bit) + 检验和 (16 bit，计算时此格填 0)'),
        (2, 2.5, 6, 2.0, '#FFCDD2', 'UDP 数据（实际传输）\n应用层载荷'),
    ]

    for x, y, w, h, color, label in blocks:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=8, color='#333')

    # Big brace on the right: "checksum coverage"
    ax.plot([8.8, 9.2, 9.2, 8.8], [2.3, 2.3, 9.2, 9.2], 'k-', linewidth=1.5)
    ax.text(9.8, 5.75, '检验和\n计算\n覆盖\n范围', ha='center', va='center',
            fontsize=9, fontweight='bold', color='#333',
            bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.2))

    # Dotted line separating virtual from actual
    ax.plot([1.5, 8.5], [6.7, 6.7], 'k--', linewidth=1, alpha=0.4)
    ax.text(5, 6.55, '———— 伪首部不进入网络，仅参与检验和计算 ————', ha='center', fontsize=7, color='#888')

    # Annotation: pseudo-header borrowed from IP
    ax.annotate('从 IP 层获取\n（IPv4 或 IPv6）', xy=(2, 8.2), fontsize=7, color='#1565C0',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#1565C0', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1))

    # IPv4 vs IPv6 note
    ax.text(5, 1.8, 'IPv4 中检验和可选（可为 0）；IPv6 中检验和强制',
            ha='center', fontsize=8, color='#E65100', fontstyle='italic')

    save(fig, 'udp_checksum_coverage.png')


# ── 16. IPv6 Header Structure ────────────────────────────────────────────
def draw_ipv6_header():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('IPv6 数据报首部格式（40 字节固定长度）', fontsize=14, fontweight='bold', pad=20)

    fields = [
        ("版本\n(4bit)", 0, 4, 10.5, 1, '#FFE0B2'),
        ("流量类型 Traffic Class\n(8bit)", 4, 12, 10.5, 1, '#FFF9C4'),
        ("流标签 Flow Label\n(20bit)", 12, 32, 10.5, 1, '#FFF9C4'),
        ("有效载荷长度 Payload Length (16bit)", 0, 16, 9.5, 1, '#C8E6C9'),
        ("下一个首部 Next Header (8bit)", 16, 24, 9.5, 1, '#C8E6C9'),
        ("跳限制 Hop Limit (8bit)", 24, 32, 9.5, 1, '#C8E6C9'),
        ("源 IP 地址 Source Address\n(128bit — 4 行 × 32bit)", 0, 32, 5.5, 4, '#E1BEE7'),
        ("目的 IP 地址 Destination Address\n(128bit — 4 行 × 32bit)", 0, 32, 1.5, 4, '#E1BEE7'),
        ("数据 Data（有效载荷）", 0, 32, 0.5, 1, '#FFCDD2'),
    ]

    for name, x0, x1, y0, h, color in fields:
        rect = FancyBboxPatch((x0, y0 - 0.5), x1 - x0, h,
                              boxstyle="round,pad=0.05", facecolor=color,
                              edgecolor='#333', linewidth=0.8)
        ax.add_patch(rect)
        cx = (x0 + x1) / 2
        cy = y0 - 0.5 + h / 2
        fs = 7.5 if len(name) > 30 else 8.5
        ax.text(cx, cy, name, ha='center', va='center', fontsize=fs, fontweight='normal')

    # Byte ruler — every 4 bits = 32 bits total
    for i in range(9):
        x = i * 4
        ax.plot([x, x], [0.3, 11.2], 'k--', linewidth=0.3, alpha=0.2)
    for i in range(8):
        ax.text(i * 4 + 2, 0.1, f'{i*4}', ha='center', fontsize=6, color='gray')

    ax.text(16, 11.5, '← 首部 40 字节（固定长度，无选项字段）→', ha='center', fontsize=9, fontstyle='italic', color='#555')
    save(fig, 'ipv6_header.png')


# ── 17. Encapsulation / Decapsulation ────────────────────────────────────
def draw_encapsulation():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('协议层次：封装与解封装', fontsize=14, fontweight='bold', pad=15)

    # Sender (left side) — top-down encapsulation
    # Receiver (right side) — bottom-up decapsulation
    sx, rx = 2, 14

    # Layer labels
    layers = [
        ('应用层', 9, '#FFCDD2'),
        ('运输层', 7.5, '#C8E6C9'),
        ('网络层', 6, '#BBDEFB'),
        ('链路层', 4.5, '#FFF9C4'),
        ('物理层', 3, '#E0E0E0'),
    ]

    for name, y, color in layers:
        ax.text(sx - 1.8, y, name, ha='right', fontsize=9, fontweight='bold', color='#333')
        ax.plot([sx - 1.5, rx + 1.5], [y - 0.3, y - 0.3], 'k--', lw=0.5, alpha=0.3)

    # Source label
    ax.text(sx, 9.8, '发送方\n（封装）', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    ax.plot([sx, sx], [2.5, 9.5], '#1565C0', linewidth=2)

    # Destination label
    ax.text(rx, 9.8, '接收方\n（解封装）', ha='center', fontsize=10, fontweight='bold', color='#C62828')
    ax.plot([rx, rx], [2.5, 9.5], '#C62828', linewidth=2)

    # Message at application layer — sender
    colors_data = ['#FFCDD2', '#C8E6C9', '#BBDEFB', '#FFF9C4']
    names_data = ['HTTP报文', 'TCP首部', 'IP首部', '链路首部']
    short_names = ['M', 'Ht', 'Hn', 'Hl']

    # Draw encapsulation on sender side
    data_width = 6
    # Application: just message
    rect = FancyBboxPatch((sx - 1, 8.8), 2, 0.4, boxstyle="round,pad=0.03",
                          facecolor='#FFCDD2', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(sx, 9.0, '报文 M', ha='center', fontsize=7)

    # Transport: [TCP hdr | M]
    rect = FancyBboxPatch((sx - 1.5, 7.2), 3, 0.5, boxstyle="round,pad=0.03",
                          facecolor='#C8E6C9', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(sx - 0.6, 7.45, 'Ht', ha='center', fontsize=7, fontweight='bold')
    ax.text(sx + 0.5, 7.45, 'M', ha='center', fontsize=7)
    ax.text(sx, 7.0, '报文段', ha='center', fontsize=6, color='#555')

    # Network: [IP hdr | TCP hdr | M]
    rect = FancyBboxPatch((sx - 2, 5.7), 4, 0.5, boxstyle="round,pad=0.03",
                          facecolor='#BBDEFB', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(sx - 1.3, 5.95, 'Hn', ha='center', fontsize=7, fontweight='bold')
    ax.text(sx + 0.1, 5.95, 'Ht', ha='center', fontsize=7, fontweight='bold')
    ax.text(sx + 1.1, 5.95, 'M', ha='center', fontsize=7)
    ax.text(sx, 5.5, '数据报', ha='center', fontsize=6, color='#555')

    # Link: [Link hdr | IP hdr | TCP hdr | M | Link trailer]
    rect = FancyBboxPatch((sx - 2.5, 4.2), 5, 0.5, boxstyle="round,pad=0.03",
                          facecolor='#FFF9C4', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(sx - 1.8, 4.45, 'Hl', ha='center', fontsize=7, fontweight='bold')
    ax.text(sx - 0.6, 4.45, 'Hn', ha='center', fontsize=7, fontweight='bold')
    ax.text(sx + 0.5, 4.45, 'Ht', ha='center', fontsize=7, fontweight='bold')
    ax.text(sx + 1.6, 4.45, 'M', ha='center', fontsize=7)
    ax.text(sx + 2.0, 4.45, 'Tl', ha='center', fontsize=7, fontweight='bold')
    ax.text(sx, 4.0, '帧', ha='center', fontsize=6, color='#555')

    # Physical: bits
    ax.text(sx, 2.8, '01001010...', ha='center', fontsize=8, fontfamily='monospace', color='#555')
    ax.text(sx, 2.4, '比特流', ha='center', fontsize=6, color='#555')

    # Down arrow on sender side
    ax.annotate('', xy=(sx, 3.0), xytext=(sx, 9.3),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(sx + 0.5, 6.2, '封装\n(加首部)', ha='left', fontsize=8, color='#1565C0')

    # Up arrow on receiver side
    ax.annotate('', xy=(rx, 9.3), xytext=(rx, 3.0),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2))
    ax.text(rx - 3.5, 6.2, '(剥首部)\n解封装', ha='right', fontsize=8, color='#C62828')

    # Draw decapsulation on receiver side (mirror)
    rect = FancyBboxPatch((rx - 2.5, 4.2), 5, 0.5, boxstyle="round,pad=0.03",
                          facecolor='#FFF9C4', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(rx, 4.45, 'Hl|Hn|Ht|M|Tl', ha='center', fontsize=7)
    ax.text(rx, 4.0, '帧', ha='center', fontsize=6, color='#555')

    rect = FancyBboxPatch((rx - 2, 5.7), 4, 0.5, boxstyle="round,pad=0.03",
                          facecolor='#BBDEFB', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(rx, 5.95, 'Hn|Ht|M', ha='center', fontsize=7)
    ax.text(rx, 5.5, '数据报', ha='center', fontsize=6, color='#555')

    rect = FancyBboxPatch((rx - 1.5, 7.2), 3, 0.5, boxstyle="round,pad=0.03",
                          facecolor='#C8E6C9', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(rx, 7.45, 'Ht|M', ha='center', fontsize=7)
    ax.text(rx, 7.0, '报文段', ha='center', fontsize=6, color='#555')

    rect = FancyBboxPatch((rx - 1, 8.8), 2, 0.4, boxstyle="round,pad=0.03",
                          facecolor='#FFCDD2', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(rx, 9.0, '报文 M', ha='center', fontsize=7)

    ax.text(rx, 2.8, '01001010...', ha='center', fontsize=8, fontfamily='monospace', color='#555')
    ax.text(rx, 2.4, '比特流', ha='center', fontsize=6, color='#555')

    # Router in middle
    ax.text(8, 5.2, '路由器\n(第1-3层)', ha='center', fontsize=7, color='#FF6F00',
            bbox=dict(boxstyle='round', facecolor='#FFF8E1', edgecolor='#FFA726'))
    ax.annotate('', xy=(11.5, 5.5), xytext=(5.5, 5.5),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=1.5))

    save(fig, 'encapsulation.png')


# ── 18. Circuit Switching vs Packet Switching ────────────────────────────
def draw_circuit_vs_packet():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    titles = ['电路交换：FDM（频分复用）', '电路交换：TDM（时分复用）', '分组交换：统计复用']
    for ax, title in zip(axes, titles):
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
        ax.axis('off')

    # FDM
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    freq_bands = [('用户 A\n(4kHz)', 1, '#BBDEFB'), ('用户 B\n(4kHz)', 3, '#C8E6C9'),
                  ('用户 C\n(4kHz)', 5, '#FFCCBC'), ('空闲\n(浪费)', 7, '#E0E0E0')]
    for label, y, color in freq_bands:
        rect = FancyBboxPatch((1, y - 0.8), 8, 1.5, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='#333', linewidth=1)
        ax.add_patch(rect)
        ax.text(5, y, label, ha='center', va='center', fontsize=8, fontweight='bold')
    ax.text(5, 0.2, '频率 →\n每个用户独占一个频段\n即使空闲也无法被其他用户使用',
            ha='center', fontsize=8, color='#555')

    # TDM
    ax = axes[1]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    # Frame structure
    for frame_idx, y_base in enumerate([4, 2.2]):
        ax.text(0.3, y_base + 1.2, f'帧 {frame_idx+1}', fontsize=8, fontweight='bold', color='#333')
        for slot, (label, color) in enumerate([
            ('A', '#BBDEFB'), ('B', '#C8E6C9'), ('C', '#FFCCBC'), ('空闲', '#E0E0E0')
        ]):
            x = slot * 2.5 + 1
            rect = FancyBboxPatch((x, y_base), 2.2, 1.2, boxstyle="round,pad=0.05",
                                  facecolor=color, edgecolor='#333', linewidth=1)
            ax.add_patch(rect)
            ax.text(x + 1.1, y_base + 0.6, label, ha='center', va='center', fontsize=8, fontweight='bold')
    ax.text(6, 0.2, '时间 →\n每帧固定时隙，周期重复\n空闲时隙无法被其他用户使用',
            ha='center', fontsize=8, color='#555')

    # Statistical multiplexing (packet switching)
    ax = axes[2]
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.text(0.5, 5.5, '链路带宽', fontsize=9, fontweight='bold', color='#333')
    packets = [
        (0.5, 'A1', '#BBDEFB'), (3.5, 'B1', '#C8E6C9'), (6, 'A2', '#BBDEFB'),
        (9, 'C1', '#FFCCBC'), (1.5, 'B2', '#C8E6C9'), (4.5, 'C2', '#FFCCBC'),
        (7.5, 'A3', '#BBDEFB'), (10.5, 'B3', '#C8E6C9'),
    ]
    for x, label, color in packets:
        y = 4.2 if label.startswith('A') else (3.2 if label.startswith('B') else 2.2)
        rect = FancyBboxPatch((x, y), 2.2, 0.7, boxstyle="round,pad=0.03",
                              facecolor=color, edgecolor='#333', linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x + 1.1, y + 0.35, label, ha='center', fontsize=7, fontweight='bold')
    ax.text(6, 0.5, '按需使用，统计复用\n分组交错传输，无固定分配\n空闲带宽自动被其他用户利用',
            ha='center', fontsize=8, color='#555')

    fig.tight_layout()
    save(fig, 'circuit_vs_packet.png')


# ── 19. NAT Translation Process ──────────────────────────────────────────
def draw_nat_process():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('NAT 网络地址转换过程', fontsize=14, fontweight='bold', pad=15)

    # Internal network cloud
    internal = mpatches.Ellipse((3, 3.5), 4, 2.5, facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=2, alpha=0.5)
    ax.add_patch(internal)
    ax.text(3, 3.5, '家庭网络\n10.0.0.0/24', ha='center', fontsize=10, fontweight='bold', color='#1565C0')

    # Host
    rect = FancyBboxPatch((1.5, 2.8), 3, 0.6, boxstyle="round,pad=0.05",
                          facecolor='#C8E6C9', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(3, 3.1, '主机 10.0.0.1:3345', ha='center', fontsize=8)

    # NAT Router
    rect = FancyBboxPatch((6.5, 2.5), 3, 2.4, boxstyle="round,pad=0.1",
                          facecolor='#FFE0B2', edgecolor='#FF6F00', linewidth=2)
    ax.add_patch(rect)
    ax.text(8, 4.5, 'NAT 路由器', ha='center', fontsize=10, fontweight='bold', color='#FF6F00')
    ax.text(8, 4.0, 'LAN: 10.0.0.254\nWAN: 138.76.29.7', ha='center', fontsize=8, color='#333')

    # Translation table
    rect = FancyBboxPatch((6.8, 2.6), 2.4, 0.8, boxstyle="round,pad=0.05",
                          facecolor='white', edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(8, 3.3, '转换表', ha='center', fontsize=7, fontweight='bold')
    ax.text(8, 3.0, 'LAN: 10.0.0.1:3345\n→ WAN: 138.76.29.7:5001', ha='center', fontsize=6, color='#333')

    # Internet cloud
    internet = mpatches.Ellipse((12, 6), 3.5, 2, facecolor='#E0E0E0', edgecolor='#757575', linewidth=2, alpha=0.5)
    ax.add_patch(internet)
    ax.text(12, 6, '因特网', ha='center', fontsize=10, fontweight='bold', color='#555')

    # Web server
    rect = FancyBboxPatch((10.5, 5.5), 3, 0.6, boxstyle="round,pad=0.05",
                          facecolor='#FFCCBC', edgecolor='#C62828', linewidth=1)
    ax.add_patch(rect)
    ax.text(12, 5.8, 'Web 服务器\n128.119.40.186:80', ha='center', fontsize=7)

    # Arrows for packet flow
    # Outgoing
    ax.annotate('', xy=(6.5, 3.8), xytext=(4.5, 3.4),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(5.5, 4.2, 'src: 10.0.0.1:3345\n→', ha='center', fontsize=7, color='#1565C0')

    ax.annotate('', xy=(12, 5.8), xytext=(9.5, 4),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2))
    ax.text(10.5, 5.3, 'src: 138.76.29.7:5001\n(重写后)', ha='center', fontsize=7, color='#FF6F00')

    # Incoming (response)
    ax.annotate('', xy=(9.5, 3.2), xytext=(12, 5),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2, linestyle='dashed'))
    ax.text(10.5, 3.8, '← dst: 138.76.29.7:5001', ha='center', fontsize=7, color='#C62828')

    ax.annotate('', xy=(4.5, 2.9), xytext=(6.5, 2.9),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2, linestyle='dashed'))
    ax.text(5.5, 2.4, '← dst: 10.0.0.1:3345\n(重写后)', ha='center', fontsize=7, color='#2E7D32')

    save(fig, 'nat_process.png')


# ── 20. GBN vs SR Window Comparison ──────────────────────────────────────
def draw_gbn_vs_sr():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))

    for ax, title, is_gbn in [(ax1, 'GBN（回退 N 步）— 分组 1 丢失', True),
                                (ax2, 'SR（选择重传）— 分组 1 丢失', False)]:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.axis('off')
        ax.set_title(title, fontsize=12, fontweight='bold', pad=10)

        sx, rx = 1.5, 8.5  # sender and receiver x positions
        dy = 0.4  # slant: y offset between send and receive (time flows down)

        # Sender and receiver timeline lines
        ax.plot([sx, sx], [0.5, 7.8], '#1565C0', linewidth=2)
        ax.text(sx, 8.1, '发送方', ha='center', fontsize=9, fontweight='bold', color='#1565C0')
        ax.plot([rx, rx], [0.5, 7.8], '#C62828', linewidth=2)
        ax.text(rx, 8.1, '接收方', ha='center', fontsize=9, fontweight='bold', color='#C62828')

        # Time arrow
        ax.annotate('时间 ▼', xy=(0.3, 0.8), fontsize=8, color='#888')

        # === Send packets 0,1,2,3 (流水线：连续发送，不等ACK) ===
        # y_send: y position where sender transmits (higher = earlier)
        # y_recv = y_send - dy: y position where receiver gets it (lower = later)
        pkts = [
            ('pkt0', 7.2, '#333', False),
            ('pkt1', 6.5, '#C62828', True),   # lost in transit
            ('pkt2', 5.8, '#333', False),
            ('pkt3', 5.1, '#333', False),
        ]
        for label, y_send, color, is_lost in pkts:
            y_recv = y_send - dy
            ax.annotate('', xy=(rx, y_recv), xytext=(sx, y_send),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
            ax.text(sx - 1.2, y_send, label, fontsize=7, color=color,
                    fontweight='bold' if is_lost else 'normal', va='center')
            if is_lost:
                ax.text(rx + 0.3, y_recv, '✗', fontsize=9, color='#C62828', va='center')

        # === ACK0 for pkt0 (immediate ACK, sent at same y as pkt0 arrival) ===
        # pkt0 arrives at y=7.2-dy=6.8 → ACK0 starts there immediately
        y_ack0_send = 7.2 - dy  # 6.8, same as pkt0 arrival
        y_ack0_recv = y_ack0_send - dy  # 6.4, sender receives after transmission
        ax.annotate('', xy=(sx, y_ack0_recv), xytext=(rx, y_ack0_send),
                    arrowprops=dict(arrowstyle='->', color='#888', lw=1, linestyle='dashed'))
        ax.text((sx + rx) / 2, y_ack0_recv, 'ACK0', fontsize=6, color='#888', ha='center')

        if is_gbn:
            # === GBN ===
            # pkt2 arrives at y=5.8-dy=5.4 → immediate dup ACK0 from there
            y_p2_arr = 5.8 - dy  # 5.4
            ax.text(rx + 0.3, y_p2_arr, 'X 丢弃', fontsize=7, color='#C62828', va='center')
            ax.annotate('', xy=(sx, y_p2_arr - dy), xytext=(rx, y_p2_arr),
                        arrowprops=dict(arrowstyle='->', color='#C62828', lw=1, linestyle='dashed'))
            ax.text((sx + rx) / 2, y_p2_arr - dy, 'ACK0（重复）', fontsize=6, color='#C62828', ha='center')

            # pkt3 arrives at y=5.1-dy=4.7 → immediate dup ACK0
            y_p3_arr = 5.1 - dy  # 4.7
            ax.text(rx + 0.3, y_p3_arr, 'X 丢弃', fontsize=7, color='#C62828', va='center')
            ax.annotate('', xy=(sx, y_p3_arr - dy), xytext=(rx, y_p3_arr),
                        arrowprops=dict(arrowstyle='->', color='#C62828', lw=1, linestyle='dashed'))
            ax.text((sx + rx) / 2, y_p3_arr - dy, 'ACK0（重复）', fontsize=6, color='#C62828', ha='center')

            # Timeout marker on sender timeline
            ax.axhline(y=3.5, xmin=0.05, xmax=0.35, color='#FF6F00', linewidth=2, linestyle='--')
            ax.text(sx - 1.2, 3.5, '⏰ 超时', fontsize=8, color='#FF6F00', va='center')

            # Retransmit 1,2,3
            for label, y_s in [('pkt1', 2.8), ('pkt2', 2.2), ('pkt3', 1.6)]:
                ax.annotate('', xy=(rx, y_s - dy), xytext=(sx, y_s),
                            arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2))
                ax.text(sx - 1.2, y_s, label, fontsize=7, color='#FF6F00', fontweight='bold', va='center')

            ax.text(5, 0.35, '定时器超时 → 重传全部未确认分组 (1,2,3)\n接收方无缓存，失序分组被丢弃',
                    ha='center', fontsize=7.5, color='#FF6F00',
                    bbox=dict(boxstyle='round', facecolor='#FFF8E1', edgecolor='#FFA726'))
        else:
            # === SR ===
            # pkt2 arrives at y=5.8-dy=5.4 → buffered, immediate selective ACK2
            y_p2_arr = 5.8 - dy  # 5.4
            ax.text(rx + 0.3, y_p2_arr, '✓ 缓存', fontsize=7, color='#2E7D32', va='center')
            ax.annotate('', xy=(sx, y_p2_arr - dy), xytext=(rx, y_p2_arr),
                        arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1, linestyle='dashed'))
            ax.text((sx + rx) / 2, y_p2_arr - dy, 'ACK2', fontsize=6, color='#2E7D32', ha='center')

            # pkt3 arrives at y=5.1-dy=4.7 → buffered, immediate selective ACK3
            y_p3_arr = 5.1 - dy  # 4.7
            ax.text(rx + 0.3, y_p3_arr, '✓ 缓存', fontsize=7, color='#2E7D32', va='center')
            ax.annotate('', xy=(sx, y_p3_arr - dy), xytext=(rx, y_p3_arr),
                        arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1, linestyle='dashed'))
            ax.text((sx + rx) / 2, y_p3_arr - dy, 'ACK3', fontsize=6, color='#2E7D32', ha='center')

            # Timeout marker (only pkt1's timer expires)
            ax.axhline(y=3.5, xmin=0.05, xmax=0.35, color='#FF6F00', linewidth=2, linestyle='--')
            ax.text(sx - 1.2, 3.5, '⏰ 超时', fontsize=8, color='#FF6F00', va='center')

            # Retransmit only pkt1
            ax.annotate('', xy=(rx, 2.8 - dy), xytext=(sx, 2.8),
                        arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2))
            ax.text(sx - 1.2, 2.8, 'pkt1', fontsize=7, color='#FF6F00', fontweight='bold', va='center')

            ax.text(5, 0.6, '定时器超时 → 仅重传丢失的分组 1\n接收方有缓存，pkt2、pkt3 已缓存\npkt1 到达后与缓存一起按序交付',
                    ha='center', fontsize=7.5, color='#2E7D32',
                    bbox=dict(boxstyle='round', facecolor='#E8F5E9', edgecolor='#66BB6A'))

    fig.tight_layout()
    save(fig, 'gbn_vs_sr.png')


# ── 21. ISP Hierarchy (Network Structure 5) ──────────────────────────────
def draw_isp_hierarchy():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('因特网结构：Network Structure 5（ISP 层次 + 内容提供商）', fontsize=14, fontweight='bold', pad=15)

    # Tier-1 ISPs (top)
    for i, (x, label) in enumerate([(4, 'Tier-1\nISP A'), (10, 'Tier-1\nISP B')]):
        rect = FancyBboxPatch((x - 1.5, 8.2), 3, 1.2, boxstyle="round,pad=0.1",
                              facecolor='#FFCCBC', edgecolor='#C62828', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, 8.8, label, ha='center', fontsize=9, fontweight='bold')

    # IXP
    ax.text(7, 8.8, 'IXP\n对等', ha='center', fontsize=7, color='#FF6F00',
            bbox=dict(boxstyle='round', facecolor='#FFF8E1', edgecolor='#FFA726'))
    ax.plot([5.5, 8.5], [8.8, 8.8], '#FF6F00', lw=1.5, linestyle='--')

    # Regional ISPs
    for x, label in [(3, '区域\nISP'), (7, '区域\nISP'), (11, '区域\nISP')]:
        rect = FancyBboxPatch((x - 1.2, 6.2), 2.4, 1.0, boxstyle="round,pad=0.08",
                              facecolor='#FFE0B2', edgecolor='#F9A825', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 6.7, label, ha='center', fontsize=8, fontweight='bold')

    # Connect Tier-1 to Regional
    for tx, rx in [(4, 3), (4, 7), (10, 7), (10, 11)]:
        ax.plot([tx, rx], [8.2, 7.2], '#888', lw=0.8, linestyle='dotted')

    # Access ISPs
    access_isp = [(1.5, '接入\nISP'), (3.5, '接入\nISP'), (5.5, '接入\nISP'),
                  (7.5, '接入\nISP'), (9.5, '接入\nISP'), (11.5, '接入\nISP')]
    for x, label in access_isp:
        rect = FancyBboxPatch((x - 0.9, 4.2), 1.8, 0.9, boxstyle="round,pad=0.05",
                              facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 4.65, label, ha='center', fontsize=7, fontweight='bold')

    # End systems
    for x in [1.5, 3, 4.5, 6, 7.5, 9, 10.5, 12]:
        circle = plt.Circle((x, 2.5), 0.2, facecolor='#C8E6C9', edgecolor='#333', linewidth=1)
        ax.add_patch(circle)
    ax.text(7, 1.8, '端系统（用户 & 服务器）', ha='center', fontsize=8, color='#333')

    # Content provider network (Google-like)
    cp = FancyBboxPatch((2, 0.3), 10, 1.0, boxstyle="round,pad=0.1",
                         facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=2, linestyle='--')
    ax.add_patch(cp)
    ax.text(7, 0.8, '内容提供商专用网络（如 Google）— 绕开上层，在 IXP/低层直接对等',
            ha='center', fontsize=8, fontweight='bold', color='#7B1FA2')

    save(fig, 'isp_hierarchy.png')


# ── 22. DV Routing Algorithm ─────────────────────────────────────────────
def draw_dv_routing():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('距离向量路由算法：Bellman-Ford 更新与计数到无穷', fontsize=14, fontweight='bold', pad=15)

    # ── Left column: topology + DV table ──
    nodes = {'X': (2.5, 6.3), 'Y': (2.5, 4.5), 'Z': (5.5, 5.4)}
    edges = [('X', 'Y', 2), ('Y', 'Z', 3), ('X', 'Z', 7)]

    for a, b, w in edges:
        x1, y1 = nodes[a]; x2, y2 = nodes[b]
        ax.plot([x1, x2], [y1, y2], '#BDBDBD', lw=2)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.15, my + 0.15, str(w), fontsize=10, fontweight='bold', color='#333',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='none'))

    for name, (x, y) in nodes.items():
        circle = plt.Circle((x, y), 0.35, facecolor='#42A5F5', edgecolor='#333', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=11, fontweight='bold', color='white')

    # DV table — below topology
    ax.text(2.5, 3.7, '节点 X 的距离表', fontsize=9, fontweight='bold', color='#1565C0')
    col_x = [1.2, 2.7, 4.2]
    table_data = [
        ['目的地', '代价', '下一跳'],
        ['X', '0', '—'],
        ['Y', '2', 'Y'],
        ['Z', '5', 'Y'],
    ]
    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            ax.text(col_x[j], 3.2 - i * 0.45, cell, fontsize=7, ha='center',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='#F5F5F5', edgecolor='#BDBDBD', alpha=0.8))

    # Divider
    ax.plot([6.5, 6.5], [0.3, 7.7], '#E0E0E0', lw=1.5)

    # ── Right column: three sections ──
    rx = 7.2

    # Section 1: Bellman-Ford equation
    ax.text(rx, 7.7, 'Bellman-Ford 方程', fontsize=11, fontweight='bold', color='#FF6F00', va='top')
    ax.text(rx, 7.0, r'$D_x(y) = \min_v \{c(x,v) + D_v(y)\}$', fontsize=11, color='#333', va='top')
    ax.text(rx, 6.2,
            'X→Z 的代价 = min( c(X,Y)+D_Y(Z)=2+3=5 ,\n'
            '                     c(X,Z)+D_Z(Z)=7+0=7 ) = 5\n'
            '最小值为 5，下一跳为 Y',
            fontsize=8, color='#333', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F5F5F5', edgecolor='#BDBDBD', alpha=0.5))

    # Section 2: Count to infinity
    ax.text(rx, 5.3, '计数到无穷问题', fontsize=11, fontweight='bold', color='#C62828', va='top')
    ax.text(rx, 4.6,
            'X-Y 链路断开后（代价变为 ∞）：\n'
            '1. Y 经 Z 到 X = 3+2=5    Z 经 Y 到 X = 2+3=5\n'
            '2. Y 发现 Z→X 代价变大：3+5=8\n'
            '3. Z 发现 Y→X 代价变大：2+8=10\n'
            '4. 循环递增 … 直到 ∞',
            fontsize=7.5, color='#333', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFCDD2', edgecolor='#C62828', alpha=0.7))

    # Section 3: Solutions
    ax.text(rx, 3.0, '解决方案', fontsize=11, fontweight='bold', color='#2E7D32', va='top')
    ax.text(rx, 2.3,
            '毒性逆转：不向下一跳通告从它学来的路由\n'
            '定义最大代价：RIP 跳数上限 15（∞ = 16）\n'
            '路由保持（hold-down）：抑制震荡路由',
            fontsize=7.5, color='#333', va='top',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#66BB6A', alpha=0.7))

    save(fig, 'dv_routing.png')


# ── 23. SDN Architecture ─────────────────────────────────────────────────
def draw_sdn_architecture():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('SDN 控制器架构', fontsize=14, fontweight='bold', pad=15)

    # Application layer
    apps = ['负载均衡\nApp', '路由\nApp', '防火墙\nApp', '接入控制\nApp']
    for i, (name, x) in enumerate(zip(apps, [2, 4.5, 7.5, 10])):
        rect = FancyBboxPatch((x - 1, 8.5), 2, 1.0, boxstyle="round,pad=0.08",
                              facecolor='#FFCDD2', edgecolor='#C62828', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 9.0, name, ha='center', va='center', fontsize=8, fontweight='bold')

    # Northbound interface
    ax.annotate('', xy=(6, 8.3), xytext=(6, 7.8),
                arrowprops=dict(arrowstyle='<->', color='#FF6F00', lw=2))
    ax.text(6.5, 8.05, '北向接口 (REST API)', ha='left', fontsize=8, color='#FF6F00', fontweight='bold')

    # Controller box
    controller = FancyBboxPatch((1.5, 4), 9, 3.5, boxstyle="round,pad=0.15",
                                facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=2)
    ax.add_patch(controller)
    ax.text(6, 7.3, 'SDN 控制器 (网络操作系统)', ha='center', fontsize=12, fontweight='bold', color='#F9A825')

    # Internal layers
    for y, label, color in [(6.5, '网络控制应用层接口', '#FFE0B2'),
                              (5.5, '网络范围状态管理层', '#FFF9C4'),
                              (4.5, '通信层 (南向接口协议)', '#FFCC80')]:
        rect = FancyBboxPatch((2, y - 0.3), 8, 0.55, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='#BDBDBD', linewidth=1)
        ax.add_patch(rect)
        ax.text(6, y, label, ha='center', fontsize=8, color='#333')

    # Southbound interface
    ax.annotate('', xy=(6, 3.8), xytext=(6, 3.3),
                arrowprops=dict(arrowstyle='<->', color='#1565C0', lw=2))
    ax.text(6.5, 3.55, '南向接口 (OpenFlow, TCP 6653)', ha='left', fontsize=8, color='#1565C0', fontweight='bold')

    # Infrastructure layer
    for i, x in enumerate([2, 4.5, 7, 9.5]):
        rect = FancyBboxPatch((x - 1, 1.5), 2, 1.2, boxstyle="round,pad=0.08",
                              facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 2.1, f'OpenFlow\n交换机 {i+1}', ha='center', fontsize=8)

    ax.text(6, 0.5, '数据平面（基础设施层）— 执行匹配加动作的转发规则',
            ha='center', fontsize=8, color='#555')

    save(fig, 'sdn_architecture.png')


# ── 24. SMTP Email System ────────────────────────────────────────────────
def draw_smtp_process():
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('电子邮件系统：SMTP 推送 + POP3/IMAP 拉取', fontsize=14, fontweight='bold', pad=15)

    # User Agent A
    rect = FancyBboxPatch((0.5, 2.5), 2.5, 1.2, boxstyle="round,pad=0.1",
                          facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(rect)
    ax.text(1.75, 3.1, '用户代理 A\n(UA)', ha='center', fontsize=9, fontweight='bold')

    # Mail Server A
    rect = FancyBboxPatch((4.5, 2.5), 2.5, 1.2, boxstyle="round,pad=0.1",
                          facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(rect)
    ax.text(5.75, 3.1, '邮件服务器 A\n(SMTP 客户端)', ha='center', fontsize=8, fontweight='bold')

    # Mail Server B
    rect = FancyBboxPatch((8.5, 2.5), 2.5, 1.2, boxstyle="round,pad=0.1",
                          facecolor='#FFCCBC', edgecolor='#C62828', linewidth=2)
    ax.add_patch(rect)
    ax.text(9.75, 3.1, '邮件服务器 B\n(SMTP 服务器)', ha='center', fontsize=8, fontweight='bold')

    # User Agent B
    rect = FancyBboxPatch((8.5, 0.3), 2.5, 1.2, boxstyle="round,pad=0.1",
                          facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(rect)
    ax.text(9.75, 0.9, '用户代理 B\n(UA)', ha='center', fontsize=9, fontweight='bold')

    # SMTP arrow A → Mail Server A
    ax.annotate('', xy=(4.5, 3.1), xytext=(3, 3.1),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(3.75, 3.6, 'SMTP\n(TCP 25)', ha='center', fontsize=7, color='#1565C0', fontweight='bold')

    # SMTP arrow Mail Server A → Mail Server B
    ax.annotate('', xy=(8.5, 3.1), xytext=(7, 3.1),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(7.75, 3.6, 'SMTP\n(TCP 25)', ha='center', fontsize=7, color='#2E7D32', fontweight='bold')

    # POP3/IMAP arrow Mail Server B → UA B
    ax.annotate('', xy=(9.75, 1.5), xytext=(9.75, 3.7),
                arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2, linestyle='dashed'))
    ax.text(10.75, 2.5, 'POP3 (TCP 110)\n或 IMAP (TCP 143)\n拉取', ha='center', fontsize=7, color='#7B1FA2')

    # Labels
    ax.text(1.75, 4.2, '发送方', ha='center', fontsize=8, color='#555')
    ax.text(9.75, 4.2, '接收方', ha='center', fontsize=8, color='#555')
    ax.text(5.75, 4.2, 'SMTP 是推协议\n（主动推送）', ha='center', fontsize=7, color='#2E7D32')
    ax.text(9.75, 5, 'POP3/IMAP 是拉协议\n（用户拉取）', ha='center', fontsize=7, color='#7B1FA2')

    # Queue annotation
    ax.text(5.75, 2.0, '报文队列\n(失败重试)', ha='center', fontsize=7, color='#888')

    save(fig, 'smtp_process.png')


# ── 25. Ethernet Frame Structure ───────────────────────────────────────
def draw_ethernet_frame():
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('以太网帧结构', fontsize=14, fontweight='bold', pad=20)

    fields = [
        ("前导码\n(8B)", 0, 1.6, '#E0E0E0'),
        ("目的 MAC 地址\n(6 字节)", 1.6, 3.2, '#BBDEFB'),
        ("源 MAC 地址\n(6 字节)", 3.2, 4.8, '#BBDEFB'),
        ("类型/长度\n(2B)", 4.8, 5.6, '#FFF9C4'),
        ("数据 (Payload)\n46–1500 字节", 5.6, 11.6, '#C8E6C9'),
        ("CRC\n(4B)", 11.6, 14, '#FFCDD2'),
    ]

    for label, x0, x1, color in fields:
        rect = FancyBboxPatch((x0, 1.2), x1 - x0, 2.6, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#333', linewidth=1.2)
        ax.add_patch(rect)
        ax.text((x0 + x1) / 2, 2.5, label, ha='center', va='center', fontsize=9, fontweight='bold')

    # Annotations below
    ax.annotate('', xy=(0, 0.8), xytext=(1.6, 0.8),
                arrowprops=dict(arrowstyle='<->', color='#555', lw=1.2))
    ax.text(0.8, 0.3, '8 字节', ha='center', fontsize=7, color='#555')

    ax.annotate('', xy=(1.6, 0.8), xytext=(4.8, 0.8),
                arrowprops=dict(arrowstyle='<->', color='#555', lw=1.2))
    ax.text(3.2, 0.3, '12 字节 (地址)', ha='center', fontsize=7, color='#555')

    ax.annotate('', xy=(5.6, 0.8), xytext=(11.6, 0.8),
                arrowprops=dict(arrowstyle='<->', color='#555', lw=1.2))
    ax.text(8.6, 0.3, '46–1500 字节', ha='center', fontsize=7, color='#555')

    ax.annotate('', xy=(11.6, 0.8), xytext=(14, 0.8),
                arrowprops=dict(arrowstyle='<->', color='#555', lw=1.2))
    ax.text(12.8, 0.3, '4B', ha='center', fontsize=7, color='#555')

    ax.text(7, 4.3, '帧长度：64–1518 字节（不含前导码）', ha='center', fontsize=9, color='#666', style='italic')

    save(fig, 'ethernet_frame.png')


# ── 26. Link Layer Hops ────────────────────────────────────────────────
def draw_link_layer_hops():
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_title('端到端路径上的六条链路层跳', fontsize=13, fontweight='bold', pad=15)

    nodes = [
        (0.5, '无线\n主机', '#FFE0B2'),
        (2.5, 'WiFi\nAP', '#E1BEE7'),
        (4.5, '交换机', '#BBDEFB'),
        (6.5, '路由器', '#C8E6C9'),
        (8.5, '路由器', '#C8E6C9'),
        (10.5, '交换机', '#BBDEFB'),
        (12, '服务器', '#FFCDD2'),
    ]

    for i, (x, label, color) in enumerate(nodes):
        circle = plt.Circle((x, 2.5), 0.4, facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, 1.5, label, ha='center', fontsize=7, fontweight='bold')

    # Links between nodes
    for i in range(len(nodes) - 1):
        x0, x1 = nodes[i][0] + 0.4, nodes[i + 1][0] - 0.4
        ax.annotate('', xy=(x1 + 0.05, 2.5), xytext=(x0, 2.5),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
        ax.text((x0 + x1) / 2, 3.0, f'链路{i + 1}', ha='center', fontsize=6, color='#888')

    save(fig, 'link_layer_hops.png')


# ── 27. VLAN Isolation ─────────────────────────────────────────────────
def draw_vlan_isolation():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('VLAN 隔离：一台物理交换机 → 两台虚拟交换机', fontsize=13, fontweight='bold', pad=15)

    # Physical switch
    rect = FancyBboxPatch((1, 1.5), 8, 2.5, boxstyle="round,pad=0.15",
                          facecolor='#ECEFF1', edgecolor='#333', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(5, 3.7, '物理交换机', ha='center', fontsize=10, fontweight='bold', color='#333')

    # VLAN 10
    vlan1 = FancyBboxPatch((1.3, 2.5), 3.5, 1.3, boxstyle="round,pad=0.08",
                           facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5, linestyle='--')
    ax.add_patch(vlan1)
    ax.text(3.05, 3.0, 'VLAN 10\n(工程部)', ha='center', fontsize=8, fontweight='bold', color='#1565C0')

    # VLAN 20
    vlan2 = FancyBboxPatch((5.2, 2.5), 3.5, 1.3, boxstyle="round,pad=0.08",
                           facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5, linestyle='--')
    ax.add_patch(vlan2)
    ax.text(6.95, 3.0, 'VLAN 20\n(市场部)', ha='center', fontsize=8, fontweight='bold', color='#2E7D32')

    # Hosts connected to VLAN 10
    for i, x in enumerate([1.8, 2.8, 3.8]):
        ax.plot([x, x], [1.2, 2.5], '#1565C0', linewidth=1.5)
        circle = plt.Circle((x, 1.0), 0.22, facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.2)
        ax.add_patch(circle)
        ax.text(x, 1.0, f'H{i + 1}', ha='center', va='center', fontsize=6, fontweight='bold')

    # Hosts connected to VLAN 20
    for i, x in enumerate([5.7, 6.7, 7.7]):
        ax.plot([x, x], [1.2, 2.5], '#2E7D32', linewidth=1.5)
        circle = plt.Circle((x, 1.0), 0.22, facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.2)
        ax.add_patch(circle)
        ax.text(x, 1.0, f'H{i + 4}', ha='center', va='center', fontsize=6, fontweight='bold')

    ax.annotate('广播域隔离', xy=(3.05, 2.2), xytext=(5, 4.5),
                arrowprops=dict(arrowstyle='->', color='#F44336', lw=1.2, connectionstyle='arc3,rad=0.3'),
                fontsize=8, color='#F44336', fontweight='bold')
    ax.annotate('路由器\n(VLAN 间通信)', xy=(7.5, 3.8), xytext=(8.8, 4.3),
                arrowprops=dict(arrowstyle='->', color='#FF9800', lw=1.2),
                fontsize=7, color='#FF9800', fontweight='bold')

    save(fig, 'vlan_isolation.png')


# ── 28. CSMA/CD ────────────────────────────────────────────────────────
def draw_csma_cd():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_title('CSMA/CD 碰撞与退避过程', fontsize=13, fontweight='bold', pad=15)

    # Nodes on the bus
    nodes = ['A', 'B', 'C', 'D']
    node_x = [1, 3.5, 6.5, 9]
    for i, (name, x) in enumerate(zip(nodes, node_x)):
        circle = plt.Circle((x, 4.3), 0.25, facecolor='#BBDEFB', edgecolor='#333', linewidth=1.2)
        ax.add_patch(circle)
        ax.text(x, 4.3, name, ha='center', va='center', fontsize=9, fontweight='bold')

    # Bus line
    ax.plot([0.5, 9.5], [3.5, 3.5], '#333', linewidth=2)
    ax.text(9.8, 3.5, '总线', fontsize=8, color='#555')

    # Connect nodes to bus
    for x in node_x:
        ax.plot([x, x], [3.5, 4.05], '#333', linewidth=1)

    # Scenario: A transmits, D transmits (collision)
    # A's signal
    ax.annotate('', xy=(5.5, 4.8), xytext=(1.3, 4.8),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(3.4, 5.0, "A 发送帧", fontsize=8, color='#1565C0', fontweight='bold')

    # D's signal (starts later)
    ax.annotate('', xy=(6.2, 2.8), xytext=(8.7, 2.8),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2))
    ax.text(6.0, 2.5, "D 发送帧", fontsize=8, color='#C62828', fontweight='bold')

    # Collision point
    collision = FancyBboxPatch((5.0, 2.65), 1.0, 0.7, boxstyle="round,pad=0.1",
                                facecolor='#FFEB3B', edgecolor='#F57F17', linewidth=1.5)
    ax.add_patch(collision)
    ax.text(5.5, 3.0, '碰撞!', ha='center', va='center', fontsize=8, fontweight='bold', color='#C62828')

    # Annotations for backoff
    ax.text(2, 1.8, '① 载波侦听：发送前检查信道空闲', fontsize=7, color='#333')
    ax.text(2, 1.3, '② 碰撞检测：发送时监听信道', fontsize=7, color='#333')
    ax.text(2, 0.8, '③ 二进制指数退避：随机等待后重试', fontsize=7, color='#333')
    ax.text(2, 0.3, '④ 全双工交换机式以太网不使用 CSMA/CD', fontsize=7, color='#888', style='italic')

    save(fig, 'csma_cd.png')


# ── 29. Store-and-Forward Pipeline ───────────────────────────────────
def draw_store_forward_pipeline():
    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    ax.set_title('存储转发流水线（P=3 个分组，N=4 条链路）', fontsize=13, fontweight='bold', pad=15)

    P, N = 3, 4
    hop_labels = [
        '链路 1\n(源 → R1)',
        '链路 2\n(R1 → R2)',
        '链路 3\n(R2 → R3)',
        '链路 4\n(R3 → 目的)',
        '目的\n接收',
    ]
    colors = ['#BBDEFB', '#C8E6C9', '#FFE0B2']
    pkt_labels = ['P1', 'P2', 'P3']

    # Y positions for each hop (top to bottom)
    y_positions = [4.8, 3.6, 2.4, 1.2, 0.1]

    # Draw hop labels
    for i, label in enumerate(hop_labels):
        ax.text(-0.3, y_positions[i] + 0.25, label, ha='right', va='center', fontsize=8, fontweight='bold', color='#333')
        # Horizontal guide line
        ax.plot([0, 14], [y_positions[i], y_positions[i]], '#E0E0E0', linewidth=0.5, linestyle='--')

    # Draw packets as rectangles
    for p in range(P):  # packet index
        for n in range(N):  # hop index
            # Packet p starts at hop 0 at time p, each hop adds 1
            x_start = p + n
            x_end = x_start + 1

            rect = FancyBboxPatch((x_start, y_positions[n]), x_end - x_start, 0.55,
                                  boxstyle="round,pad=0.05",
                                  facecolor=colors[p], edgecolor='#333', linewidth=1.0)
            ax.add_patch(rect)
            ax.text((x_start + x_end) / 2, y_positions[n] + 0.28, pkt_labels[p],
                    ha='center', va='center', fontsize=7, fontweight='bold')

    # Time axis
    for t in range(8):
        ax.text(t + 0.5, -0.3, f'{t}·L/R', ha='center', fontsize=7, color='#888')
    ax.text(8.5, -0.3, '时间 →', ha='left', fontsize=7, color='#666', style='italic')
    ax.plot([0, 8], [-0.05, -0.05], '#333', linewidth=1)
    for t in range(9):
        ax.plot([t, t], [-0.05, -0.2], '#333', linewidth=0.5)

    # Annotations
    ax.annotate('P1 收完\n开始转发', xy=(1, y_positions[1] + 0.55), xytext=(2.5, y_positions[1] + 1.0),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.2),
                fontsize=7, color='#1565C0', fontweight='bold')

    ax.annotate('管道打\n通！', xy=(N, y_positions[-1] + 0.55), xytext=(N + 1.5, y_positions[-1] + 1.0),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.2),
                fontsize=8, color='#C62828', fontweight='bold')

    # Formula label
    ax.text(7, 5.3, r'$d = \frac{(P+N-1) \cdot L}{R} = \frac{6L}{R}$  (忽略传播/处理/排队时延)',
            ha='center', fontsize=10, color='#333', fontweight='bold')

    save(fig, 'store_forward_pipeline.png')


# ── 26. RDT 3.0 FSM (Sender + Receiver) ─────────────────────────────────
def draw_rdt_fsm():
    fig, (ax_s, ax_r) = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('rdt 3.0 有限状态机（FSM）', fontsize=14, fontweight='bold', y=1.01)

# ── 26. RDT 3.0 FSM (Sender + Receiver) ─────────────────────────────────
def draw_rdt_fsm():
    fig, (ax_s, ax_r) = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('rdt 3.0 有限状态机（FSM）', fontsize=14, fontweight='bold', y=1.01)

    # Shared coordinate system for vertical alignment
    YLIM = (0, 10)

    # ── Sender FSM ──
    ax_s.set_xlim(0, 14)
    ax_s.set_ylim(*YLIM)
    ax_s.axis('off')
    ax_s.set_title('发送方 FSM', fontsize=13, fontweight='bold', pad=12)

    BW, BH = 2.8, 1.8  # box width, height

    # States: W0 (bottom-left) → WACK0 (bottom-right) → W1 (top-right) → WACK1 (top-left)
    S = {
        'W0':    (2, 2.5),
        'WACK0': (7, 2.5),
        'W1':    (7, 7),
        'WACK1': (2, 7),
    }
    labels_s = {
        'W0':    '等待\n0 号\n调用',
        'WACK0': '等待\nACK 0',
        'W1':    '等待\n1 号\n调用',
        'WACK1': '等待\nACK 1',
    }
    for name, (x, y) in S.items():
        rect = FancyBboxPatch((x, y), BW, BH, boxstyle="round,pad=0.1",
                              facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.5)
        ax_s.add_patch(rect)
        ax_s.text(x + BW/2, y + BH/2, labels_s[name],
                  ha='center', va='center', fontsize=9, fontweight='bold')

    def cx(name): return S[name][0] + BW/2
    def cy(name): return S[name][1] + BH/2
    def left(name): return S[name][0]
    def right(name): return S[name][0] + BW
    def top(name): return S[name][1] + BH
    def bot(name): return S[name][1]

    # ── State transitions ──
    # W0 → WACK0 (right)
    ax_s.annotate('', xy=(left('WACK0'), cy('W0')), xytext=(right('W0'), cy('W0')),
                  arrowprops=dict(arrowstyle='->', color='#333', lw=1.8))
    ax_s.text((right('W0')+left('WACK0'))/2, cy('W0')+0.3,
              'rdt_send(data)\nsndpkt=make_pkt(0,data)\nstart_timer',
              ha='center', fontsize=7, color='#333')

    # WACK0 → W1 (up)
    ax_s.annotate('', xy=(cx('W1'), bot('W1')), xytext=(cx('WACK0'), top('WACK0')),
                  arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.8))
    ax_s.text(cx('W1')+0.7, (top('WACK0')+bot('W1'))/2,
              'rdt_rcv(rcvpkt)\n&& notcorrupt\n&& isACK(0)',
              ha='center', fontsize=7, color='#2E7D32')

    # W1 → WACK1 (left)
    ax_s.annotate('', xy=(right('WACK1'), cy('W1')), xytext=(left('W1'), cy('W1')),
                  arrowprops=dict(arrowstyle='->', color='#333', lw=1.8))
    ax_s.text((left('W1')+right('WACK1'))/2, cy('W1')+0.3,
              'rdt_send(data)\nsndpkt=make_pkt(1,data)\nstart_timer',
              ha='center', fontsize=7, color='#333')

    # WACK1 → W0 (down)
    ax_s.annotate('', xy=(cx('W0'), top('W0')), xytext=(cx('WACK1'), bot('WACK1')),
                  arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.8))
    ax_s.text(cx('W0')-1.0, (bot('WACK1')+top('W0'))/2,
              'rdt_rcv(rcvpkt)\n&& notcorrupt\n&& isACK(1)',
              ha='center', fontsize=7, color='#2E7D32')

    # ── Self-loops (center at box edge, gap toward box) ──
    # RIGHT side: theta1=270→theta2=90 (drawn through east, gap at west=toward box)
    # LEFT side:  theta1=90 →theta2=270 (drawn through west, gap at east=toward box)
    # TOP:        theta1=0  →theta2=180 (drawn through north, gap at south=toward box)
    # BOTTOM:     theta1=180→theta2=360 (drawn through south, gap at north=toward box)

    # WACK0 timeout: right side
    cx0, cy0 = right('WACK0'), cy('WACK0')
    circ0t = mpatches.Arc((cx0, cy0), 1.6, 1.6, angle=0, theta1=270, theta2=90,
                          color='#C62828', lw=1.8, linestyle='--')
    ax_s.add_patch(circ0t)
    ax_s.text(cx0 + 1.5, cy0, 'timeout\nudt_send(sndpkt)\nstart_timer',
              ha='center', fontsize=7, color='#C62828')

    # WACK0 corrupt: bottom side
    cx0b, cy0b = cx('WACK0'), bot('WACK0')
    circ0c = mpatches.Arc((cx0b, cy0b), 1.4, 1.4, angle=0, theta1=180, theta2=360,
                          color='#C62828', lw=1.2, linestyle='--')
    ax_s.add_patch(circ0c)
    ax_s.text(cx0b, cy0b - 1.3, 'corrupt\n|| wrong ACK\nΛ',
              ha='center', fontsize=6.5, color='#C62828')

    # WACK1 timeout: left side
    cx1, cy1 = left('WACK1'), cy('WACK1')
    circ1t = mpatches.Arc((cx1, cy1), 1.6, 1.6, angle=0, theta1=90, theta2=270,
                          color='#C62828', lw=1.8, linestyle='--')
    ax_s.add_patch(circ1t)
    ax_s.text(cx1 - 1.5, cy1, 'timeout\nudt_send(sndpkt)\nstart_timer',
              ha='center', fontsize=7, color='#C62828')

    # WACK1 corrupt: top side
    cx1b, cy1b = cx('WACK1'), top('WACK1')
    circ1c = mpatches.Arc((cx1b, cy1b), 1.4, 1.4, angle=0, theta1=0, theta2=180,
                          color='#C62828', lw=1.2, linestyle='--')
    ax_s.add_patch(circ1c)
    ax_s.text(cx1b, cy1b + 1.3, 'corrupt\n|| wrong ACK\nΛ',
              ha='center', fontsize=6.5, color='#C62828')

    # ── Receiver FSM ──
    ax_r.set_xlim(0, 14)
    ax_r.set_ylim(*YLIM)
    ax_r.axis('off')
    ax_r.set_title('接收方 FSM', fontsize=13, fontweight='bold', pad=12)

    # States: vertically centered in same range as sender
    R = {
        'WR0': (4.5, 5.5),
        'WR1': (4.5, 2),
    }
    labels_r = {
        'WR0': '等待\n0 号\n来自下层',
        'WR1': '等待\n1 号\n来自下层',
    }
    for name, (x, y) in R.items():
        rect = FancyBboxPatch((x, y), BW, BH, boxstyle="round,pad=0.1",
                              facecolor='#FFF3E0', edgecolor='#E65100', linewidth=1.5)
        ax_r.add_patch(rect)
        ax_r.text(x + BW/2, y + BH/2, labels_r[name],
                  ha='center', va='center', fontsize=9, fontweight='bold')

    def rcx(name): return R[name][0] + BW/2
    def rcy(name): return R[name][1] + BH/2
    def rleft(name): return R[name][0]
    def rtop(name): return R[name][1] + BH
    def rbot(name): return R[name][1]

    # ── Receiver transitions ──
    # WR0 → WR1 (down): seq0 correct, send ACK0
    ax_r.annotate('', xy=(rcx('WR1'), rtop('WR1')), xytext=(rcx('WR0'), rbot('WR0')),
                  arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.8))
    ax_r.text(rcx('WR0')+0.9, (rbot('WR0')+rtop('WR1'))/2 + 0.3,
              'rdt_rcv(rcvpkt)\n&& notcorrupt\n&& has_seq0()\nextract, deliver\nudt_send(ACK0)',
              ha='center', fontsize=7, color='#2E7D32')

    # WR1 → WR0 (up): seq1 correct, send ACK1
    ax_r.annotate('', xy=(rcx('WR0'), rbot('WR0')), xytext=(rcx('WR1'), rtop('WR1')),
                  arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.8))
    ax_r.text(rcx('WR0')-2.0, (rbot('WR0')+rtop('WR1'))/2 - 0.3,
              'rdt_rcv(rcvpkt)\n&& notcorrupt\n&& has_seq1()\nextract, deliver\nudt_send(ACK1)',
              ha='center', fontsize=7, color='#2E7D32')

    # ── Receiver self-loops (left side: theta1=90, theta2=270) ──
    # WR0: loop on LEFT side
    rcx0, rcy0 = rleft('WR0'), rcy('WR0')
    rcirc0 = mpatches.Arc((rcx0, rcy0), 1.6, 1.6, angle=0, theta1=90, theta2=270,
                          color='#C62828', lw=1.8, linestyle='--')
    ax_r.add_patch(rcirc0)
    ax_r.text(rcx0 - 1.5, rcy0, 'corrupt\n|| has_seq1()\nudt_send(ACK1)',
              ha='center', fontsize=7, color='#C62828')

    # WR1: loop on LEFT side
    rcx1, rcy1 = rleft('WR1'), rcy('WR1')
    rcirc1 = mpatches.Arc((rcx1, rcy1), 1.6, 1.6, angle=0, theta1=90, theta2=270,
                          color='#C62828', lw=1.8, linestyle='--')
    ax_r.add_patch(rcirc1)
    ax_r.text(rcx1 - 1.5, rcy1, 'corrupt\n|| has_seq0()\nudt_send(ACK0)',
              ha='center', fontsize=7, color='#C62828')

    # Legend
    ax_r.text(10.5, 9, '符号说明', fontsize=9, fontweight='bold')
    ax_r.text(10.5, 8.2, '── 事件/动作', fontsize=8, color='#333')
    ax_r.text(10.5, 7.6, '- - 超时/差错', fontsize=8, color='#C62828')
    ax_r.text(10.5, 7.0, '── 正确接收', fontsize=8, color='#2E7D32')
    ax_r.text(10.5, 6.4, 'Λ  无动作', fontsize=8, color='#C62828')

    plt.tight_layout()
    save(fig, 'rdt_fsm.png')


# ── 27. Switch Self-Learning Process ─────────────────────────────────────
def draw_switch_self_learning():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('交换机自学习过程', fontsize=14, fontweight='bold', pad=15)

    # Draw switch in center
    sw_x = 6
    for i in range(8):
        ax.plot([sw_x - 0.6, sw_x + 0.6], [i * 1.2 + 0.3, i * 1.2 + 0.3], '#1565C0', linewidth=1.5)

    # Hosts on left and right
    hosts_left = [('A', '0C:11:22:33:44:01'), ('B', '0C:11:22:33:44:02')]
    hosts_right = [('C', '0C:11:22:33:44:03'), ('D', '0C:11:22:33:44:04')]

    for i, (name, mac) in enumerate(hosts_left):
        x, y = 1.5, 7 - i * 2
        rect = FancyBboxPatch((x - 0.8, y - 0.5), 2.0, 1.0, boxstyle="round,pad=0.05",
                              facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1)
        ax.add_patch(rect)
        ax.text(x + 0.2, y + 0.15, f'{name}', ha='center', fontsize=10, fontweight='bold')
        ax.text(x + 0.2, y - 0.25, mac, ha='center', fontsize=6.5, color='#555')

    for i, (name, mac) in enumerate(hosts_right):
        x, y = 10.5, 7 - i * 2
        rect = FancyBboxPatch((x - 0.8, y - 0.5), 2.0, 1.0, boxstyle="round,pad=0.05",
                              facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1)
        ax.add_patch(rect)
        ax.text(x + 0.2, y + 0.15, f'{name}', ha='center', fontsize=10, fontweight='bold')
        ax.text(x + 0.2, y - 0.25, mac, ha='center', fontsize=6.5, color='#555')

    # MAC address table (right side of figure)
    table_x, table_y = 8.5, 2.0
    ax.text(table_x, table_y, 'MAC 地址表（初始为空）', fontsize=9, fontweight='bold', color='#1565C0')
    # Table rows with borders
    rows_data = [
        ('MAC 地址', '接口', 'TTL'),
    ]
    for i, (mac, port, ttl) in enumerate(rows_data):
        y = table_y - 0.5 - i * 0.45
        ax.text(table_x - 0.5, y, mac, fontsize=8, fontweight='bold', color='#555')
        ax.text(table_x + 2.3, y, port, fontsize=8, fontweight='bold', color='#555')
        ax.text(table_x + 3.8, y, ttl, fontsize=8, fontweight='bold', color='#555')
    ax.text(table_x + 1.25, table_y - 0.95, '(空)', fontsize=8, color='#999')

    # Frame flow arrows with step labels
    # Step 1: A sends frame to C
    ax.annotate('', xy=(5.4, 6.6), xytext=(3.5, 7),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2))
    # Label at the link
    ax.text(4.2, 7.3, '帧: A→C\ndst=C, src=A',
            ha='center', fontsize=8, color='#C62828', fontweight='bold')

    # Step 2: Switch learns A on left port (interface 1)
    ax.annotate('学', xy=(6.2, 7.2), xytext=(7.2, 8.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5),
                fontsize=9, color='#1565C0', fontweight='bold')
    ax.text(7.8, 8.8, '① 学习：A→接口1', fontsize=8, color='#1565C0', fontweight='bold')

    # Step 3: Switch doesn't know C, floods to all except incoming port
    ax.annotate('', xy=(10.5, 7), xytext=(6.6, 6.6),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2))
    # Flood to D
    ax.annotate('', xy=(10.5, 5), xytext=(6.6, 6.0),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2))
    # Flood to B
    ax.annotate('', xy=(3.5, 5), xytext=(5.4, 5.4),
                arrowprops=dict(arrowstyle='->', color='#FF6F00', lw=2))

    ax.text(7.2, 6.0, '② MAC表中无C\n→ 泛洪到所有其他端口',
            ha='center', fontsize=8, color='#FF6F00', fontweight='bold')

    # Updated table after learning
    table2_y = table_y
    ax.text(table_x, table2_y + 1.2, '学习后更新：', fontsize=8, color='#1565C0', fontweight='bold')
    ax.text(table_x - 0.5, table2_y + 0.7, '0C:11:22:33:44:01 (A)', fontsize=7.5, color='#333')
    ax.text(table_x + 2.3, table2_y + 0.7, '1', fontsize=7.5, color='#333')
    ax.text(table_x + 3.8, table2_y + 0.7, '60s', fontsize=7.5, color='#333')

    # Step 4: C replies to A
    ax.annotate('', xy=(5.4, 5.4), xytext=(10.5, 5),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(8.2, 4.7, '帧: C→A (响应)\ndst=A, src=C',
            ha='center', fontsize=8, color='#2E7D32', fontweight='bold')

    # Step 5: Switch learns C and forwards to A only
    ax.annotate('', xy=(3.5, 4), xytext=(5.4, 4.8),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))

    ax.text(7.2, 4.3, '③ 学习C→接口2\n④ 查表知A在接口1\n→ 只向接口1转发',
            ha='center', fontsize=8, color='#2E7D32', fontweight='bold')

    # Updated table
    ax.text(table_x, table2_y - 1.0, '再次更新：', fontsize=8, color='#1565C0', fontweight='bold')
    ax.text(table_x - 0.5, table2_y - 1.5, '0C:11:22:33:44:01 (A)', fontsize=7.5, color='#333')
    ax.text(table_x + 2.3, table2_y - 1.5, '1', fontsize=7.5, color='#333')
    ax.text(table_x + 3.8, table2_y - 1.5, '55s', fontsize=7.5, color='#333')
    ax.text(table_x - 0.5, table2_y - 2.0, '0C:11:22:33:44:03 (C)', fontsize=7.5, color='#333')
    ax.text(table_x + 2.3, table2_y - 2.0, '2', fontsize=7.5, color='#333')
    ax.text(table_x + 3.8, table2_y - 2.0, '60s', fontsize=7.5, color='#333')

    save(fig, 'switch_self_learning.png')


# ── 28. Nodal Delay Anatomy ──────────────────────────────────────────────
def draw_nodal_delay():
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('节点时延分解：路由器内部四种时延的位置', fontsize=14, fontweight='bold', pad=15)

    # Router body
    router_bg = FancyBboxPatch((1, 1.5), 12, 4.5, boxstyle="round,pad=0.2",
                                facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=1.5)
    ax.add_patch(router_bg)
    ax.text(7, 5.7, '路由器内部', fontsize=10, color='#607D8B', ha='center', fontweight='bold')

    # Input port
    input_rect = FancyBboxPatch((1.5, 2.5), 2.5, 2.5, boxstyle="round,pad=0.1",
                                 facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(input_rect)
    ax.text(2.75, 4.3, '输入端口', fontsize=10, fontweight='bold', ha='center')
    ax.text(2.75, 3.8, 'CRC 校验\n最长前缀匹配\nTTL/检验和更新', fontsize=7.5, color='#333', ha='center')

    # Queue
    queue_rect = FancyBboxPatch((4.5, 2.5), 2.0, 2.5, boxstyle="round,pad=0.1",
                                 facecolor='#FFE0B2', edgecolor='#E65100', linewidth=1.5)
    ax.add_patch(queue_rect)
    ax.text(5.5, 4.3, '队列\n(缓冲区)', fontsize=10, fontweight='bold', ha='center')
    # Draw small packets in queue
    for j in range(5):
        pk = FancyBboxPatch((4.7 + j * 0.35, 3.1), 0.3, 0.4, boxstyle="round,pad=0.02",
                             facecolor='#FF8A65', edgecolor='#BF360C', linewidth=0.5)
        ax.add_patch(pk)

    # Switching fabric
    fab_rect = FancyBboxPatch((7.0, 2.5), 2.0, 2.5, boxstyle="round,pad=0.1",
                               facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=1.5)
    ax.add_patch(fab_rect)
    ax.text(8.0, 4.3, '交换结构', fontsize=10, fontweight='bold', ha='center')
    ax.text(8.0, 3.8, 'via 内存/\n总线/Crossbar', fontsize=7.5, color='#333', ha='center')

    # Output port
    out_rect = FancyBboxPatch((9.5, 2.5), 2.5, 2.5, boxstyle="round,pad=0.1",
                               facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(out_rect)
    ax.text(10.75, 4.3, '输出端口', fontsize=10, fontweight='bold', ha='center')
    ax.text(10.75, 3.8, '排队(输出队列)\n链路层封装\n物理层发送', fontsize=7.5, color='#333', ha='center')

    # Incoming link
    ax.annotate('', xy=(1, 3.75), xytext=(0, 3.75),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2.5))
    ax.text(0.5, 4.1, '到达\n分组', ha='center', fontsize=8, color='#333')

    # Outgoing link
    ax.annotate('', xy=(13, 3.75), xytext=(12.5, 3.75),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2.5))
    ax.text(13, 4.1, '离开\n分组', ha='center', fontsize=8, color='#333')

    # Delay labels with brackets
    delay_labels = [
        (1.5, 1.3, 4.0, 1.3, '处理时延\n$d_{proc}$\n(μs级)', '#1565C0'),
        (4.5, 1.3, 6.5, 1.3, '排队时延\n$d_{queue}$\n(μs~ms级)', '#E65100'),
        (7.0, 1.3, 9.0, 1.3, '传输时延\n$d_{trans}=L/R$\n(μs~ms级)', '#7B1FA2'),
        (9.5, 1.3, 12.0, 1.3, '传播时延\n$d_{prop}=d/s$\n(ms级)', '#2E7D32'),
    ]

    for x0, y0, x1, y1, label, color in delay_labels:
        ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle='<->', color=color, lw=2))
        cx = (x0 + x1) / 2
        ax.text(cx, y0 - 0.1, label, ha='center', va='top', fontsize=8.5,
                color=color, fontweight='bold')

    # Total formula
    ax.text(7, 0.4, r'$d_{nodal} = d_{proc} + d_{queue} + d_{trans} + d_{prop}$',
            ha='center', fontsize=12, color='#333', fontweight='bold')

    save(fig, 'nodal_delay.png')


# ── 29. P2P vs C/S Distribution Time ─────────────────────────────────────
def draw_p2p_scaling():
    fig, ax = plt.subplots(figsize=(10, 7))

    # Parameters
    F = 1.0       # file size (normalized)
    us = 20.0     # server upload rate
    dmin = 2.0    # min download rate
    u_peer = 1.0  # upload rate per peer

    N_vals = np.arange(1, 101)
    D_cs = np.maximum(N_vals * F / us, F / dmin)
    D_p2p = np.maximum(np.maximum(F / us, F / dmin),
                       N_vals * F / (us + N_vals * u_peer))

    ax.plot(N_vals, D_cs, '#C62828', linewidth=2.5, label='客户-服务器 (C/S)')
    ax.plot(N_vals, D_p2p, '#1565C0', linewidth=2.5, label='P2P')

    ax.set_xlabel('对等方数量 N', fontsize=12)
    ax.set_ylabel('最小分发时间 $D$ (归一化单位)', fontsize=12)
    ax.set_title('P2P 与客户-服务器分发时间对比', fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 6)

    # Annotation
    ax.annotate('C/S: $D \\propto N$\n线性增长，服务器瓶颈',
                xy=(80, D_cs[79]), xytext=(65, 4.5),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.5),
                fontsize=9, color='#C62828', fontweight='bold')

    ax.annotate('P2P: 自扩展性\n每个新对等方\n也是新的上传者',
                xy=(80, D_p2p[79]), xytext=(55, 1.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5),
                fontsize=9, color='#1565C0', fontweight='bold')

    plt.tight_layout()
    save(fig, 'p2p_scaling.png')


# ── 30. DASH Adaptive Bitrate Timeline ───────────────────────────────────
def draw_dash_adaptation():
    fig, ax1 = plt.subplots(figsize=(14, 6))

    t = np.linspace(0, 60, 300)
    # Simulated available bandwidth: baseline + sinusoidal variation + noise
    np.random.seed(42)
    bw = 6.5 + 3.5 * np.sin(2 * np.pi * t / 30) + np.random.normal(0, 1.0, len(t))
    bw = np.maximum(bw, 0.5)

    ax1.fill_between(t, 0, bw, alpha=0.15, color='#1565C0')
    ax1.plot(t, bw, '#1565C0', linewidth=2, label='可用带宽')
    ax1.set_ylabel('带宽 (Mbps)', fontsize=12, color='#1565C0')
    ax1.tick_params(axis='y', labelcolor='#1565C0')
    ax1.set_xlabel('时间 (秒)', fontsize=12)
    ax1.set_ylim(0, 13)

    # Bitrate levels (video versions)
    bitrates = [1.5, 3.0, 5.0, 8.0, 11.0]
    labels = ['240p\n(1.5M)', '480p\n(3.0M)', '720p\n(5.0M)', '1080p\n(8.0M)', '1440p\n(11.0M)']
    colors = ['#FF8A65', '#FFB74D', '#FFF176', '#AED581', '#64B5F6']

    for br, label, color in zip(bitrates, labels, colors):
        ax1.axhline(y=br, color=color, linestyle='--', linewidth=1, alpha=0.5)
        ax1.text(60.5, br, label, fontsize=7, color=color, va='center', fontweight='bold')

    # Simulate DASH chunk selection
    chunk_dur = 2  # seconds per chunk
    chunk_times = np.arange(0, 60, chunk_dur)
    selected = []
    for ct in chunk_times:
        idx = np.searchsorted(t, ct)
        available = bw[idx]
        # Select highest bitrate below available bandwidth (with safety margin 0.8)
        best = bitrates[0]
        for br in bitrates:
            if br <= available * 0.85:
                best = br
        selected.append(best)

    # Plot as step function
    ax2 = ax1.twinx()
    for i in range(len(chunk_times) - 1):
        x0, x1 = chunk_times[i], chunk_times[i + 1]
        y = selected[i]
        color_idx = bitrates.index(y)
        ax2.fill_between([x0, x1], 0, 1, color=colors[color_idx], alpha=0.5)

    ax2.set_ylim(0, 5)
    ax2.set_yticks([])
    ax2.set_ylabel('DASH 选择的码率版本', fontsize=12, color='#333', fontweight='bold')

    ax1.set_title('DASH 自适应码率切换', fontsize=14, fontweight='bold')

    # Legend for adaptation behavior
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#1565C0', lw=2, label='实测可用带宽'),
        Line2D([0], [0], marker='s', color='w', markerfacecolor='#AED581', markersize=12, label='DASH chunk 选择'),
    ]
    ax1.legend(handles=legend_elements, fontsize=10, loc='upper right')

    # Annotation
    ax1.annotate('带宽下降\n切换低码率',
                 xy=(17, bw[np.searchsorted(t, 17)]),
                 xytext=(10, 10),
                 arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.5),
                 fontsize=9, color='#C62828', fontweight='bold')

    ax1.annotate('带宽恢复\n切换高码率',
                 xy=(34, bw[np.searchsorted(t, 34)]),
                 xytext=(40, 10),
                 arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5),
                 fontsize=9, color='#2E7D32', fontweight='bold')

    plt.tight_layout()
    save(fig, 'dash_adaptation.png')


# ── 31. Hidden Terminal Problem ─────────────────────────────────────────
def draw_hidden_terminal():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('隐藏终端问题', fontsize=14, fontweight='bold', y=1.01)

    # Left: physical layout
    ax1.set_xlim(0, 14)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    ax1.set_title('物理布局', fontsize=12, fontweight='bold')

    # Nodes A, B, C
    # A and C are both within B's range, but A and C are not within each other's range
    a_circle = plt.Circle((3, 6), 2.2, facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5, alpha=0.3)
    ax1.add_patch(a_circle)
    ax1.text(3, 8.5, "A 的通信范围", ha='center', fontsize=8, color='#1565C0')

    ax1.text(3, 6, 'A', ha='center', fontsize=16, fontweight='bold', color='#1565C0')

    b_circle = plt.Circle((7, 6), 2.5, facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5, alpha=0.3)
    ax1.add_patch(b_circle)
    ax1.text(7, 8.8, "B 的通信范围", ha='center', fontsize=8, color='#2E7D32')
    ax1.text(7, 6, 'B', ha='center', fontsize=16, fontweight='bold', color='#2E7D32')

    c_circle = plt.Circle((11, 6), 2.2, facecolor='#FFE0B2', edgecolor='#E65100', linewidth=1.5, alpha=0.3)
    ax1.add_patch(c_circle)
    ax1.text(11, 8.5, "C 的通信范围", ha='center', fontsize=8, color='#E65100')
    ax1.text(11, 6, 'C', ha='center', fontsize=16, fontweight='bold', color='#E65100')

    # Dashed line between A and B, B and C (showing they can hear each other)
    ax1.plot([4.2, 5.8], [6, 6], 'k-', linewidth=1.5)
    ax1.plot([8.2, 9.8], [6, 6], 'k-', linewidth=1.5)

    # Cross between A and C (cannot hear)
    ax1.plot([4.5, 9.5], [5.2, 5.2], 'k--', linewidth=1, alpha=0.5)
    ax1.annotate('', xy=(5.5, 5.0), xytext=(8.5, 5.0),
                arrowprops=dict(arrowstyle='<->', color='#C62828', lw=1.2, linestyle='--'))
    ax1.text(7, 4.6, 'A 和 C 彼此隐藏\n(不在通信范围内)', ha='center', fontsize=8, color='#C62828')

    # Right: timing diagram
    ax2.set_xlim(0, 14)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    ax2.set_title('时间线：A 和 C 同时向 B 发送', fontsize=12, fontweight='bold')

    # Nodes on left
    ax2.plot([1, 1], [2, 9], '#1565C0', linewidth=2)
    ax2.plot([5, 5], [2, 9], '#2E7D32', linewidth=2)
    ax2.plot([9, 9], [2, 9], '#E65100', linewidth=2)
    ax2.text(1, 9.5, '节点 A', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    ax2.text(5, 9.5, '节点 B', ha='center', fontsize=10, fontweight='bold', color='#2E7D32')
    ax2.text(9, 9.5, '节点 C', ha='center', fontsize=10, fontweight='bold', color='#E65100')

    # A sends to B
    ax2.barh(7.5, 3.0, left=2, height=0.8, color='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax2.text(3.5, 7.9, '数据传输', ha='center', fontsize=9, fontweight='bold', color='#1565C0')
    ax2.annotate('', xy=(2, 7.9), xytext=(1.3, 7.9),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))

    # C also sends to B (during A's transmission)
    ax2.barh(5.5, 3.0, left=3.5, height=0.8, color='#FFE0B2', edgecolor='#E65100', linewidth=1.5)
    ax2.text(5.0, 5.9, '数据传输', ha='center', fontsize=9, fontweight='bold', color='#E65100')
    ax2.annotate('', xy=(3.5, 5.9), xytext=(8.7, 5.9),
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=2))

    # Collision at B
    ax2.barh(3.5, 3.0, left=3.5, height=0.8, color='#FFCDD2', edgecolor='#C62828', linewidth=1.5)
    ax2.text(5.0, 3.9, '碰撞！', ha='center', fontsize=9, fontweight='bold', color='#C62828')
    ax2.annotate('', xy=(2, 3.9), xytext=(1.3, 3.9),
                arrowprops=dict(arrowstyle='->', color='#BBDEFB', lw=1, alpha=0.4))
    ax2.annotate('', xy=(3.5, 3.9), xytext=(8.7, 3.9),
                arrowprops=dict(arrowstyle='->', color='#FFE0B2', lw=1, alpha=0.4))

    # Summary text
    ax2.text(7, 1.5, 'A 检测不到 C 的传输 → 以为信道空闲\nC 检测不到 A 的传输 → 以为信道空闲\n→ 两者同时发送 → B 处碰撞',
            ha='center', fontsize=9, color='#C62828', fontweight='bold')

    plt.tight_layout()
    save(fig, 'hidden_terminal.png')


# ── 32. CSMA/CA RTS/CTS Exchange ───────────────────────────────────────
def draw_csma_ca_rts_cts():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('CSMA/CA：RTS/CTS 交换过程', fontsize=14, fontweight='bold', pad=15)

    # Nodes
    ax.plot([2, 2], [0.5, 7.5], '#1565C0', linewidth=2)
    ax.plot([8, 8], [0.5, 7.5], '#2E7D32', linewidth=2)
    ax.plot([14, 14], [0.5, 7.5], '#E65100', linewidth=2)
    ax.text(2, 7.8, '发送方', ha='center', fontsize=11, fontweight='bold', color='#1565C0')
    ax.text(8, 7.8, '接收方', ha='center', fontsize=11, fontweight='bold', color='#2E7D32')
    ax.text(14, 7.8, '其他站点\n(含隐藏终端)', ha='center', fontsize=9, fontweight='bold', color='#E65100')

    # Time flows downward
    # DIFS wait
    ax.barh(1.5, 2, left=2, height=0.6, color='#E0E0E0', edgecolor='#999', linewidth=1)
    ax.text(3, 1.8, 'DIFS + 退避', fontsize=8, color='#555', fontweight='bold')

    # RTS
    ax.annotate('', xy=(7.8, 2.8), xytext=(2.2, 2.8),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(5, 3.1, 'RTS', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    ax.text(5, 2.5, '(包含 Duration = SIFS+CTS+SIFS+DATA+SIFS+ACK)',
            ha='center', fontsize=7, color='#555')

    # RTS received by others → set NAV
    ax.annotate('', xy=(14, 2.8), xytext=(8.2, 2.8),
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=1.2, alpha=0.7))
    # NAV bar for "other stations"
    ax.barh(3.2, 9.2, left=2.4, height=0.6, color='#FFCDD2', edgecolor='#C62828', linewidth=0.8, alpha=0.5, zorder=0)
    ax.text(7, 3.5, 'NAV (静默)', fontsize=8, color='#C62828', fontweight='bold')

    # SIFS
    ax.text(8.3, 3.6, 'SIFS', fontsize=7, color='#555')

    # CTS
    ax.annotate('', xy=(2.2, 4.1), xytext=(7.8, 4.1),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(5, 4.4, 'CTS', ha='center', fontsize=10, fontweight='bold', color='#2E7D32')

    # SIFS
    ax.text(8.3, 5.0, 'SIFS', fontsize=7, color='#555')

    # DATA
    ax.annotate('', xy=(7.8, 5.5), xytext=(2.2, 5.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=3))
    ax.text(5, 5.8, 'DATA (数据帧)', ha='center', fontsize=10, fontweight='bold', color='#1565C0')

    # SIFS
    ax.text(8.3, 6.3, 'SIFS', fontsize=7, color='#555')

    # ACK
    ax.annotate('', xy=(2.2, 6.7), xytext=(7.8, 6.7),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(5, 7.0, 'ACK', ha='center', fontsize=10, fontweight='bold', color='#2E7D32')

    # Labels on the left
    ax.text(0.3, 2.8, '①', fontsize=12, fontweight='bold', color='#1565C0', va='center')
    ax.text(0.3, 4.1, '②', fontsize=12, fontweight='bold', color='#2E7D32', va='center')
    ax.text(0.3, 5.5, '③', fontsize=12, fontweight='bold', color='#1565C0', va='center')
    ax.text(0.3, 6.7, '④', fontsize=12, fontweight='bold', color='#2E7D32', va='center')

    # Time axis
    ax.annotate('', xy=(2, 0.3), xytext=(2, 7.3),
                arrowprops=dict(arrowstyle='<->', color='#333', lw=1))
    ax.text(1.5, 3.8, '时间', fontsize=8, color='#333', rotation=90, va='center')

    save(fig, 'csma_ca_rts_cts.png')


# ── 33. 4G LTE Architecture ────────────────────────────────────────────
def draw_lte_architecture():
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('4G LTE 体系结构', fontsize=14, fontweight='bold', pad=15)

    # UE
    ue = FancyBboxPatch((1, 4), 2.5, 1.8, boxstyle="round,pad=0.1",
                        facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(ue)
    ax.text(2.25, 5.25, 'UE\n(用户设备)', ha='center', fontsize=10, fontweight='bold')

    # eNodeB
    enb = FancyBboxPatch((5.5, 3.5), 2.5, 3.0, boxstyle="round,pad=0.1",
                          facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(enb)
    ax.text(6.75, 5.5, 'eNodeB\n(基站)', ha='center', fontsize=10, fontweight='bold')
    ax.text(6.75, 4.2, '无线资源管理\n调度, 切换', ha='center', fontsize=7.5, color='#555')

    # E-UTRAN label
    ax.text(4.25, 6.8, 'E-UTRAN', ha='center', fontsize=9, fontweight='bold', color='#2E7D32')

    # S-GW
    sgw = FancyBboxPatch((10, 5.5), 2.5, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.5)
    ax.add_patch(sgw)
    ax.text(11.25, 6.9, 'S-GW', ha='center', fontsize=10, fontweight='bold')
    ax.text(11.25, 6.0, 'Serving\nGateway', ha='center', fontsize=8, color='#555')

    # P-GW
    pgw = FancyBboxPatch((13.5, 5.5), 2.5, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#FFE0B2', edgecolor='#E65100', linewidth=1.5)
    ax.add_patch(pgw)
    ax.text(14.75, 6.9, 'P-GW', ha='center', fontsize=10, fontweight='bold')
    ax.text(14.75, 6.0, 'PDN\nGateway', ha='center', fontsize=8, color='#555')

    # MME
    mme = FancyBboxPatch((10, 2), 2.5, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=1.5)
    ax.add_patch(mme)
    ax.text(11.25, 3.4, 'MME', ha='center', fontsize=10, fontweight='bold')
    ax.text(11.25, 2.5, 'Mobility\nManagement\nEntity', ha='center', fontsize=7.5, color='#555')

    # HSS
    hss = FancyBboxPatch((13.5, 2), 2.5, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=1.5)
    ax.add_patch(hss)
    ax.text(14.75, 3.4, 'HSS', ha='center', fontsize=10, fontweight='bold')
    ax.text(14.75, 2.5, 'Home\nSubscriber\nServer', ha='center', fontsize=7.5, color='#555')

    # Internet
    internet = FancyBboxPatch((13.5, 8.5), 2.5, 1.2, boxstyle="round,pad=0.05",
                              facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=1.5)
    ax.add_patch(internet)
    ax.text(14.75, 9.1, 'Internet', ha='center', fontsize=10, fontweight='bold')

    # EPC label
    ax.text(12.25, 1.3, 'EPC (Evolved Packet Core)', ha='center', fontsize=9, fontweight='bold', color='#7B1FA2')

    # Connections (User Plane)
    # UE→eNodeB (LTE-Uu)
    ax.annotate('', xy=(5.5, 5.5), xytext=(3.5, 5.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2, linestyle='-'))
    ax.text(4.3, 5.8, 'LTE-Uu\n(用户+控制)', fontsize=7, color='#1565C0', ha='center')

    # eNodeB→S-GW (S1-U)
    ax.annotate('', xy=(10, 6.5), xytext=(8, 5.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(9.0, 6.3, 'S1-U', fontsize=7, color='#1565C0')

    # S-GW→P-GW
    ax.annotate('', xy=(13.5, 6.5), xytext=(12.5, 6.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(13, 6.8, 'GTP\n隧道', fontsize=7, color='#1565C0', ha='center')

    # P-GW→Internet
    ax.annotate('', xy=(14.75, 8.5), xytext=(14.75, 7.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(15.1, 8.0, 'SGi', fontsize=7, color='#1565C0')

    # Control Plane
    # eNodeB→MME (S1-MME)
    ax.annotate('', xy=(10, 3.0), xytext=(7.5, 4.0),
                arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2, linestyle='--'))
    ax.text(8.5, 3.2, 'S1-MME\n(控制)', fontsize=7, color='#7B1FA2')

    # MME→HSS
    ax.annotate('', xy=(13.5, 3.0), xytext=(12.5, 3.0),
                arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2, linestyle='--'))
    ax.text(13, 3.3, 'S6a', fontsize=7, color='#7B1FA2')

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color='#1565C0', lw=2, label='用户平面 (数据)'),
        Line2D([0], [0], color='#7B1FA2', lw=2, linestyle='--', label='控制平面 (信令)'),
    ]
    ax.legend(handles=legend_elements, fontsize=10, loc='lower left')

    save(fig, 'lte_architecture.png')


# ── 34. Mobile IP Indirect Routing ────────────────────────────────────
def draw_mobile_ip():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('移动 IP：间接路由（三角形路由）', fontsize=14, fontweight='bold', pad=15)

    # Home Network
    home_bg = FancyBboxPatch((0.5, 5.5), 5, 3, boxstyle="round,pad=0.1",
                              facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.5, alpha=0.6)
    ax.add_patch(home_bg)
    ax.text(3, 8.1, '归属网络 (Home Network)', ha='center', fontsize=10, fontweight='bold', color='#2E7D32')

    # HA
    ha = FancyBboxPatch((1.5, 6.0), 2.5, 1.5, boxstyle="round,pad=0.1",
                         facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(ha)
    ax.text(2.75, 6.9, '归属代理\n(HA)', ha='center', fontsize=10, fontweight='bold')
    ax.text(2.75, 6.2, '永久地址', ha='center', fontsize=8, color='#555')

    # Foreign Network
    for_bg = FancyBboxPatch((10, 1.5), 5.5, 4.5, boxstyle="round,pad=0.1",
                             facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.5, alpha=0.6)
    ax.add_patch(for_bg)
    ax.text(12.75, 5.6, '外地网络 (Foreign Network)', ha='center', fontsize=10, fontweight='bold', color='#1565C0')

    # FA
    fa = FancyBboxPatch((11, 3.5), 2.5, 1.5, boxstyle="round,pad=0.1",
                         facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(fa)
    ax.text(12.25, 4.4, '外地代理\n(FA)', ha='center', fontsize=10, fontweight='bold')

    # Mobile Node
    mn = FancyBboxPatch((11, 2.0), 2.5, 1.0, boxstyle="round,pad=0.05",
                         facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(mn)
    ax.text(12.25, 2.5, '移动节点 (MN)', ha='center', fontsize=10, fontweight='bold')

    # Correspondent
    corr = FancyBboxPatch((0.5, 1.0), 3.0, 1.5, boxstyle="round,pad=0.1",
                           facecolor='#F3E5F5', edgecolor='#7B1FA2', linewidth=1.5)
    ax.add_patch(corr)
    ax.text(2, 2.0, '通信对端\n(Correspondent)', ha='center', fontsize=10, fontweight='bold')
    ax.text(2, 1.3, 'Permanent Address', ha='center', fontsize=7, color='#555')

    # Arrow 1: Correspondent → HA (data sent to permanent address)
    ax.annotate('', xy=(1.8, 5.8), xytext=(1.8, 2.5),
                arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=2.5))
    ax.text(0.6, 4.1, '① 发送到\n永久地址', ha='center', fontsize=9, color='#7B1FA2', fontweight='bold')

    # Arrow 2: HA tunnels to FA (CoA)
    ax.annotate('', xy=(10.8, 4.2), xytext=(4.0, 6.4),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2.5))
    ax.text(7.2, 5.7, '② 隧道封装\n发往 CoA', ha='center', fontsize=9, color='#2E7D32', fontweight='bold')

    # Arrow 3: FA delivers to MN
    ax.annotate('', xy=(11.5, 2.6), xytext=(11.5, 3.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(11.0, 3.0, '③ 解封装\n交付', ha='center', fontsize=8, color='#1565C0')

    # Direct path from MN to CN (bypass HA)
    ax.annotate('', xy=(3.3, 2.0), xytext=(12, 2.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2, linestyle='--'))
    ax.text(7.5, 2.9, 'MN → CN 直接发送（不经 HA）', ha='center', fontsize=8, color='#1565C0')

    # Triangle route annotation
    ax.annotate('三角形路由', xy=(6, 3.5), xytext=(3, 5.0),
                fontsize=10, color='#C62828', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFCDD2', alpha=0.8))

    save(fig, 'mobile_ip.png')


# ── 35. 802.11 Frame Structure ─────────────────────────────────────────
def draw_wifi_frame():
    fig, ax = plt.subplots(figsize=(16, 7))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('802.11 数据帧结构', fontsize=14, fontweight='bold', pad=20)

    fields = [
        ("帧控制\nFrame Control", 0, 2, 7, 1, '#BBDEFB'),
        ("持续时间/ID\nDuration/ID", 2, 4, 7, 1, '#B3E5FC'),
        ("地址 1\n(RA)", 4, 10, 7, 1, '#C8E6C9'),
        ("地址 2\n(TA)", 10, 16, 7, 1, '#C8E6C9'),
        ("地址 3\n", 16, 22, 7, 1, '#C8E6C9'),
        ("序号控制\nSeq Ctrl", 22, 24, 7, 1, '#FFF9C4'),
        ("地址 4\n(可选)", 24, 30, 7, 1, '#E0E0E0'),
        ("帧主体\nFrame Body (0–2312 B)", 0, 32, 5.5, 1.5, '#FFCDD2'),
        ("CRC (4 B)", 0, 32, 4, 1, '#FFE0B2'),
    ]

    for name, x0, x1, y0, h, color in fields:
        rect = FancyBboxPatch((x0, y0 - 0.5), x1 - x0, h,
                              boxstyle="round,pad=0.05", facecolor=color,
                              edgecolor='#333', linewidth=0.8)
        ax.add_patch(rect)
        cx = (x0 + x1) / 2
        cy = y0 - 0.5 + h / 2
        fs = 8 if len(name) > 12 else 9
        ax.text(cx, cy, name, ha='center', va='center', fontsize=fs, fontweight='normal')

    # Byte ruler
    for i in range(9):
        ax.text(i * 4, 6.3, f'{i*4}', ha='center', fontsize=6, color='gray')
    ax.text(16, 7.8, '← 首部 (30 B 典型) →', ha='center', fontsize=9, color='#555')

    # Frame Control breakdown below
    ax.text(1, 3.2, '帧控制字段 (2B) 展开：', fontsize=8, fontweight='bold', color='#333')
    fc_bits = [
        ('协议\n版本\n2b', 0, 0.8),
        ('类型\n2b', 0.8, 1.6),
        ('子类型\n4b', 1.6, 2.8),
        ('To\nDS\n1b', 2.8, 3.2),
        ('From\nDS\n1b', 3.2, 3.6),
        ('更多\n分片\n1b', 3.6, 4.0),
        ('重传\n1b', 4.0, 4.4),
        ('功率\n管理\n1b', 4.4, 4.8),
        ('更多\n数据\n1b', 4.8, 5.2),
        ('WEP\n1b', 5.2, 5.6),
        ('顺序\n1b', 5.6, 6.0),
    ]
    scale = 5
    x0 = 0
    for label, xb0, xb1 in fc_bits:
        rect = FancyBboxPatch((x0 + xb0 * scale, 2.4), (xb1 - xb0) * scale, 0.8,
                              boxstyle="round,pad=0.02", facecolor='#E3F2FD',
                              edgecolor='#1565C0', linewidth=0.5)
        ax.add_patch(rect)
        ax.text(x0 + (xb0 + xb1) / 2 * scale, 2.8, label, ha='center', va='center', fontsize=5.5)

    # Address usage table
    ax.text(14, 3.2, '地址字段含义 (To DS / From DS)：', fontsize=8, fontweight='bold', color='#333')
    addr_text = (
        'To DS  From DS    Addr1     Addr2    Addr3     Addr4\n'
        '  0       0        DA        SA      BSSID       —\n'
        '  1       0       AP MAC    STA MAC  Dst MAC     —\n'
        '  0       1       Dst MAC   AP MAC   Src MAC     —\n'
        '  1       1       Dst AP    Src AP   Dst STA   Src STA'
    )
    ax.text(14, 2.7, addr_text, fontsize=6.5, color='#333', fontfamily='monospace')

    save(fig, 'wifi_frame.png')


# ── 36. WiFi BSS Architecture ──────────────────────────────────────────
def draw_wifi_bss():
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('WiFi 基本服务集 (BSS) 架构', fontsize=14, fontweight='bold', pad=15)

    # Wired network
    ax.plot([2, 12], [8.5, 8.5], '#607D8B', linewidth=3)
    ax.text(7, 9.0, '有线以太网 (Distribution System)', ha='center', fontsize=10, fontweight='bold', color='#607D8B')

    # Router
    router = FancyBboxPatch((5.5, 7.8), 3, 1.2, boxstyle="round,pad=0.1",
                            facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=1.5)
    ax.add_patch(router)
    ax.text(7, 8.4, '网关/路由器\n(通往外网)', ha='center', fontsize=9, fontweight='bold')

    # AP
    ap_x, ap_y = 7, 6.5
    ap = FancyBboxPatch((ap_x - 1.8, ap_y - 0.8), 3.6, 1.6, boxstyle="round,pad=0.1",
                         facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(ap)
    ax.text(ap_x, ap_y + 0.3, '接入点 AP\n(Access Point)', ha='center', fontsize=10, fontweight='bold')
    ax.text(ap_x, ap_y - 0.5, 'SSID: MyWiFi', ha='center', fontsize=8, color='#555')

    # Link from AP to wired network
    ax.plot([7, 7], [7.3, 7.8], '#333', linewidth=2)
    ax.text(7.5, 7.55, '以太网', fontsize=7, color='#555', rotation=90, va='center')

    # Wireless range circle
    bss_circle = plt.Circle((ap_x, ap_y), 3.5, facecolor='#E8F5E9', edgecolor='#2E7D32',
                             linewidth=1.5, linestyle='--', alpha=0.4)
    ax.add_patch(bss_circle)
    ax.text(ap_x, ap_y - 3.8, 'BSS 覆盖范围', ha='center', fontsize=8, color='#2E7D32', fontweight='bold')

    # STAs
    stas = [
        (3.8, 5.5, 'STA 1\n笔记本电脑'),
        (9.5, 5.2, 'STA 2\n智能手机'),
        (5.5, 3.5, 'STA 3\n平板电脑'),
        (8.5, 4.0, 'STA 4\nIoT 传感器'),
    ]
    for x, y, label in stas:
        sta = FancyBboxPatch((x - 0.9, y - 0.5), 1.8, 1.0, boxstyle="round,pad=0.05",
                              facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.2)
        ax.add_patch(sta)
        ax.text(x, y, label, ha='center', fontsize=8, fontweight='bold')

    # Wireless links (dashed)
    for x, y, _ in stas:
        ax.plot([ap_x, x], [ap_y, y], '#1565C0', linewidth=0.8, linestyle=':', alpha=0.6)

    # Beacon annotation
    ax.annotate('信标帧\n(Beacon)\n每100ms广播', xy=(ap_x + 1.5, ap_y - 0.2),
                xytext=(ap_x + 2.8, ap_y + 1.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5),
                fontsize=7.5, color='#1565C0', fontweight='bold')

    # Another BSS in range
    ax.text(1.5, 7.0, '相邻 BSS\n(信道不同)', ha='center', fontsize=7, color='#999')

    # Portals
    ax.text(8.5, 9.3, '门户 (Portal)\n连接外网', fontsize=7, color='#607D8B', ha='center')

    save(fig, 'wifi_bss.png')


# ── 37. CIDR Subnet Comparison ─────────────────────────────────────────
def draw_cidr_subnet():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('CIDR 子网划分对比：/16, /24, /25, /26, /28', fontsize=14, fontweight='bold', pad=15)

    subnets = [
        ('/16', 16, '子网数: $2^{0}=1$\n主机数: $2^{16}−2=65534$', '#BBDEFB'),
        ('/24', 24, '子网数: $2^{8}=256$\n主机数: $2^{8}−2=254$', '#C8E6C9'),
        ('/25', 25, '子网数: $2^{9}=512$\n主机数: $2^{7}−2=126$', '#FFF9C4'),
        ('/26', 26, '子网数: $2^{10}=1024$\n主机数: $2^{6}−2=62$', '#FFE0B2'),
        ('/28', 28, '子网数: $2^{12}=4096$\n主机数: $2^{4}−2=14$', '#FFCDD2'),
    ]

    for i, (label, prefix, desc, color) in enumerate(subnets):
        y = 6.8 - i * 1.3
        # Network part
        rect_net = FancyBboxPatch((0, y - 0.5), prefix, 1.0,
                                   boxstyle="round,pad=0.05", facecolor=color,
                                   edgecolor='#333', linewidth=1)
        ax.add_patch(rect_net)
        # Host part
        rect_host = FancyBboxPatch((prefix, y - 0.5), 32 - prefix, 1.0,
                                    boxstyle="round,pad=0.05", facecolor='#ECEFF1',
                                    edgecolor='#333', linewidth=1)
        ax.add_patch(rect_host)

        # Labels
        ax.text(prefix / 2, y, '网络前缀', ha='center', va='center', fontsize=8, fontweight='bold', color='#333')
        ax.text(prefix + (32 - prefix) / 2, y, '主机号', ha='center', va='center', fontsize=8, color='#666')
        ax.text(-0.5, y, label, ha='center', va='center', fontsize=11, fontweight='bold', color='#333')
        ax.text(32.5, y, desc, ha='left', va='center', fontsize=7.5, color='#555')

    # Column labels
    ax.text(16, 7.6, '← 32 比特 IP 地址空间 →', ha='center', fontsize=10, fontstyle='italic', color='#555')
    # Byte markers
    for i in range(5):
        x = i * 8
        ax.plot([x, x], [0.3, 7.3], 'k--', linewidth=0.3, alpha=0.3)

    save(fig, 'cidr_subnet.png')


# ── 38. Web Request Protocol Stack Panorama ────────────────────────────
def draw_web_request_panorama():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')
    ax.set_title('Web 请求的一天：协议栈全景', fontsize=14, fontweight='bold', pad=15)

    # Steps and their protocols
    steps = [
        (1, 'DHCP\n获取 IP', ('链路层\n(以太网/ARP)', '网络层\n(IP/广播)', '运输层\n(UDP)', '应用层\n(DHCP)'), ['#C8E6C9', '#BBDEFB', '#FFF9C4', '#FFCDD2']),
        (2, 'ARP\n获取 MAC', ('以太网', 'ARP'), ['#C8E6C9', '#E1BEE7']),
        (3, 'DNS\n解析域名', ('以太网', 'IP', 'UDP', 'DNS'), ['#C8E6C9', '#BBDEFB', '#FFF9C4', '#FFCDD2']),
        (4, 'OSPF\n域内路由', ('以太网', 'IP', 'OSPF'), ['#C8E6C9', '#BBDEFB', '#E1BEE7']),
        (5, 'TCP\n三次握手', ('以太网', 'IP', 'TCP'), ['#C8E6C9', '#BBDEFB', '#B3E5FC']),
        (6, 'HTTP\nGET 请求', ('以太网', 'IP', 'TCP', 'HTTP'), ['#C8E6C9', '#BBDEFB', '#B3E5FC', '#FFCDD2']),
    ]

    for i, (num, title, layers, colors) in enumerate(steps):
        x = 1.0 + i * 3.2
        # Title box
        title_box = FancyBboxPatch((x, 9.5), 2.5, 1.2, boxstyle="round,pad=0.1",
                                    facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=1.5)
        ax.add_patch(title_box)
        ax.text(x + 1.25, 10.3, f'{num}. {title}', ha='center', va='center', fontsize=9, fontweight='bold')

        # Layer stack
        for j, (layer, color) in enumerate(zip(layers, colors)):
            y = 8.5 - j * 1.4
            rect = FancyBboxPatch((x, y), 2.5, 1.2, boxstyle="round,pad=0.05",
                                   facecolor=color, edgecolor='#333', linewidth=0.8)
            ax.add_patch(rect)
            ax.text(x + 1.25, y + 0.6, layer, ha='center', va='center', fontsize=7.5, fontweight='bold')

        # Arrow to next
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + 2.7, 10.1), xytext=(x + 2.9, 10.1),
                        arrowprops=dict(arrowstyle='->', color='#607D8B', lw=2))

    # Bottom timeline
    ax.plot([1.5, 19], [2.5, 2.5], '#333', linewidth=1.5)
    ax.text(10.5, 2.0, '时间', ha='center', fontsize=10, fontweight='bold', color='#333')

    # Encapsulation illustration
    ax.text(10.5, 1.2, '每一阶段：上层数据逐层添加首部（封装）发送 → 接收端逐层剥离首部（解封装）→ 最终交付应用层',
            ha='center', fontsize=9, color='#555')

    save(fig, 'web_request_panorama.png')


# ── 39. TDM vs FDM vs CDMA Comparison ──────────────────────────────────
def draw_tdm_fdm_cdma():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 7))
    fig.suptitle('三种信道划分协议对比', fontsize=14, fontweight='bold', y=1.01)

    # TDM
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_title('TDM（时分复用）', fontsize=12, fontweight='bold', color='#1565C0')
    ax1.set_xlabel('时间 →', fontsize=10)
    ax1.set_ylabel('频率', fontsize=10)
    ax1.set_yticks([])
    colors_tdm = ['#BBDEFB', '#C8E6C9', '#FFE0B2', '#F8BBD0']
    for frame in range(3):
        for slot in range(4):
            ax1.barh(5, 0.9, left=frame * 3.5 + slot * 0.85, height=1.5,
                     color=colors_tdm[slot], edgecolor='#333', linewidth=0.5)
            ax1.text(frame * 3.5 + slot * 0.85 + 0.4, 5, f'{slot+1}',
                    ha='center', va='center', fontsize=7, fontweight='bold')
    ax1.text(5, 7.5, '时隙轮转\n每个用户轮流占用整个频率', ha='center', fontsize=9, color='#333')

    # FDM
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.set_title('FDM（频分复用）', fontsize=12, fontweight='bold', color='#2E7D32')
    ax2.set_xlabel('时间 →', fontsize=10)
    ax2.set_ylabel('频率 ↑', fontsize=10)
    ax2.set_yticks([])
    colors_fdm = ['#BBDEFB', '#C8E6C9', '#FFE0B2', '#F8BBD0']
    for ch in range(4):
        ax2.fill_between([0, 9], ch * 1.5 + 1, ch * 1.5 + 2.2,
                          color=colors_fdm[ch], edgecolor='#333', linewidth=0.8, alpha=0.7)
        ax2.text(5.5, ch * 1.5 + 1.6, f'频段 {ch+1}', ha='center', va='center', fontsize=8, fontweight='bold')
    ax2.text(5, 8.5, '频率划分\n每个用户独占一个频段', ha='center', fontsize=9, color='#333')

    # CDMA
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.set_title('CDMA（码分多址）', fontsize=12, fontweight='bold', color='#E65100')
    ax3.set_xlabel('时间 →', fontsize=10)
    ax3.set_ylabel('频率', fontsize=10)
    ax3.set_yticks([])
    ax3.fill_between([0, 9], 1, 7, color='#FFF3E0', edgecolor='#E65100', linewidth=1.5, alpha=0.5)
    # Overlapping signals with different codes
    codes = [('+1-1+1-1', '#1565C0'), ('+1+1-1-1', '#2E7D32'),
             ('+1-1-1+1', '#C62828'), ('-1+1+1-1', '#7B1FA2')]
    for i, (code, color) in enumerate(codes):
        ax3.text(5, 6 - i * 1.2, f'编码 {i+1}: {code}', ha='center', fontsize=9,
                fontweight='bold', color=color)
    ax3.text(5, 1.0, '所有用户同时同频\n通过正交编码区分', ha='center', fontsize=9, color='#333')

    plt.tight_layout()
    save(fig, 'tdm_fdm_cdma.png')


# ── 40. Fat-Tree Topology ──────────────────────────────────────────────
def draw_fat_tree():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('数据中心 Fat-Tree (Leaf-Spine) 拓扑', fontsize=14, fontweight='bold', pad=15)

    # Border Routers
    for i, x in enumerate([6, 10]):
        br = FancyBboxPatch((x - 0.8, 8.8), 1.6, 0.8, boxstyle="round,pad=0.05",
                             facecolor='#ECEFF1', edgecolor='#607D8B', linewidth=1.5)
        ax.add_patch(br)
        ax.text(x, 9.2, f'边界路由器 {i+1}', ha='center', fontsize=7.5, fontweight='bold')

    # Internet label
    ax.annotate('', xy=(7.6, 9.6), xytext=(6.4, 9.6),
                arrowprops=dict(arrowstyle='<->', color='#607D8B', lw=2))
    ax.text(7, 9.85, 'Internet', ha='center', fontsize=9, fontweight='bold', color='#607D8B')
    ax.plot([8, 8], [9.6, 8.8], '#607D8B', linewidth=2)
    ax.plot([8, 8], [9.6, 8.8], '#607D8B', linewidth=2)

    # Spine layer
    spine_switches = [3, 7, 11]
    ax.text(8, 7.8, '脊骨层 (Spine Layer)', ha='center', fontsize=9, fontweight='bold', color='#7B1FA2')
    for x in spine_switches:
        sp = FancyBboxPatch((x - 0.6, 6.5), 1.8, 0.9, boxstyle="round,pad=0.05",
                              facecolor='#E1BEE7', edgecolor='#7B1FA2', linewidth=1.5)
        ax.add_patch(sp)
        ax.text(x + 0.3, 6.95, f'脊骨 {spine_switches.index(x) + 1}', ha='center', fontsize=8, fontweight='bold')

        # Connect to border routers
        for br_x in [6, 10]:
            ax.plot([x + 0.3, br_x], [6.5, 8.8], '#7B1FA2', linewidth=1.0, alpha=0.5)

    # Leaf layer
    leaf_switches = [1.5, 4, 6.5, 9, 11.5, 14]
    ax.text(8, 5.5, '叶子层 (Leaf / ToR)', ha='center', fontsize=9, fontweight='bold', color='#2E7D32')
    for i, x in enumerate(leaf_switches):
        leaf = FancyBboxPatch((x - 0.7, 4.0), 1.8, 0.9, boxstyle="round,pad=0.05",
                               facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
        ax.add_patch(leaf)
        ax.text(x + 0.2, 4.45, f'叶子 {i+1}', ha='center', fontsize=7.5, fontweight='bold')

        # Connect each leaf to ALL spine switches (fat-tree defining feature)
        for sx in spine_switches:
            ax.plot([x + 0.2, sx + 0.3], [4.0, 6.5], '#2E7D32', linewidth=0.8, alpha=0.4)

    # Hosts
    hosts_per_leaf = 3
    for i, lx in enumerate(leaf_switches):
        for j in range(hosts_per_leaf):
            hx = lx - 0.4 + j * 0.5
            hy = 2.2 - j * 0.2
            ax.plot([lx + 0.2, hx], [4.0, hy], '#1565C0', linewidth=0.8, alpha=0.6)
            host = FancyBboxPatch((hx - 0.2, hy - 0.3), 0.4, 0.5, boxstyle="round,pad=0.02",
                                   facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=0.8)
            ax.add_patch(host)

    ax.text(8, 1.2, '主机层 (Hosts)', ha='center', fontsize=9, fontweight='bold', color='#1565C0')

    # Annotations
    ax.annotate('每个叶子连接到\n所有脊骨交换机', xy=(7, 5.5), xytext=(3, 7.0),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5),
                fontsize=7.5, color='#2E7D32', fontweight='bold')

    ax.annotate('东西向流量\n(经脊骨层)', xy=(8, 5.2), xytext=(12, 7.0),
                arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=1.5),
                fontsize=7.5, color='#7B1FA2', fontweight='bold')

    save(fig, 'fat_tree.png')


# ── 41. OpenFlow Flow Table ────────────────────────────────────────────
def draw_openflow():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_title('OpenFlow 流表：匹配加动作 (Match + Action)', fontsize=14, fontweight='bold', pad=15)

    # Incoming packet
    pkt_in = FancyBboxPatch((0.5, 6), 3, 1.5, boxstyle="round,pad=0.1",
                             facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(pkt_in)
    ax.text(2, 7.1, '到达分组', ha='center', fontsize=10, fontweight='bold', color='#1565C0')
    ax.text(2, 6.4, 'MAC/IP/TCP 首部字段值', ha='center', fontsize=7, color='#555')

    # Flow Table
    table_x, table_y = 5, 3
    table_bg = FancyBboxPatch((table_x, table_y), 7, 5, boxstyle="round,pad=0.1",
                               facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.5)
    ax.add_patch(table_bg)
    ax.text(8.5, 7.7, 'OpenFlow 流表 (Flow Table)', ha='center', fontsize=11, fontweight='bold', color='#333')

    # Table header
    cols = [('入端口', 5.5, 6.8), ('以太网\nsrc/dst\n类型/VLAN', 6.8, 8.4),
            ('IP\nsrc/dst\n协议/TOS', 8.4, 10), ('TCP/UDP\nsrc/dst\n端口', 10, 11.5)]
    for label, x0, x1 in cols:
        ax.plot([x0, x0], [6.7, 5.3], '#333', linewidth=0.5)
        ax.text((x0 + x1) / 2, 6.35, label, ha='center', fontsize=7, fontweight='bold', color='#333')
    ax.plot([5.5, 11.5], [6.7, 6.7], '#333', linewidth=0.8)
    ax.plot([5.5, 11.5], [5.3, 5.3], '#333', linewidth=0.8)

    # Table rows (match entries)
    rows = [
        ('1', '10.3.*.*', '10.2.*.*', '→ Port 4'),
        ('*', '10.3.*.*', '*', '→ Drop'),
        ('2', '*', '10.1.0.3', '→ Port 2'),
        ('*', '*', '10.2.0.4', '→ Port 3'),
    ]
    for i, (port, src, dst, action) in enumerate(rows):
        y = 5.0 - i * 0.5
        if i % 2 == 0:
            ax.fill_between([5.5, 11.5], y, y + 0.5, color='#FFF8E1', alpha=0.5)
        ax.text(6.0, y + 0.25, port, fontsize=8, color='#333')
        ax.text(7.6, y + 0.25, src, fontsize=8, color='#333')
        ax.text(9.2, y + 0.25, dst, fontsize=8, color='#333')
        ax.text(11.0, y + 0.25, action, fontsize=8, fontweight='bold', color='#1565C0')

    # Match fields labels
    ax.text(2, 4.5, '匹配\n12 个\n首部字段', ha='center', fontsize=9, fontweight='bold', color='#F9A825')

    # Action output
    actions_box = FancyBboxPatch((13, 3.5), 2.5, 3, boxstyle="round,pad=0.1",
                                  facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(actions_box)
    ax.text(14.25, 6.1, '动作', ha='center', fontsize=11, fontweight='bold', color='#2E7D32')
    actions = ['转发到端口', '丢弃 (Drop)', '重写首部', '发送到控制器']
    for i, a in enumerate(actions):
        ax.text(14.25, 5.4 - i * 0.5, f'• {a}', fontsize=8, color='#333')

    # Arrows
    ax.annotate('', xy=(5, 6.3), xytext=(3.5, 6.3),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.annotate('', xy=(13, 5.5), xytext=(12, 5.5),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))

    # Priority note
    ax.text(8.5, 2.5, '多条匹配 → 最高优先级条目生效（硬件 TCAM 实现）',
            ha='center', fontsize=9, color='#555')

    save(fig, 'openflow_flow_table.png')


# ── 42. MPLS Label Operations ───────────────────────────────────────────
def draw_mpls_operations():
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('MPLS 标签操作：Push → Swap → Pop', fontsize=14, fontweight='bold', pad=15)

    # Three routers
    routers = [
        (3, 4, '入口 LSR\n(Ingress)', 'Push\n插入标签 L1', '#C8E6C9'),
        (9, 4, '中间 LSR\n(Transit)', 'Swap\nL1→L2', '#FFF9C4'),
        (15, 4, '出口 LSR\n(Egress)', 'Pop\n移除标签', '#FFCDD2'),
    ]

    for x, y, label, op, color in routers:
        router = FancyBboxPatch((x - 1.5, y - 0.8), 3.0, 2.0, boxstyle="round,pad=0.1",
                                 facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(router)
        ax.text(x, y + 0.4, label, ha='center', fontsize=9, fontweight='bold')
        ax.text(x, y - 0.5, op, ha='center', fontsize=8, color='#555')

    # Links
    ax.annotate('', xy=(7.5, 4), xytext=(4.5, 4),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.annotate('', xy=(13.5, 4), xytext=(10.5, 4),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    # Packets at each stage
    # Before entering MPLS domain
    pkt0 = FancyBboxPatch((0.3, 6.2), 2.4, 1.2, boxstyle="round,pad=0.05",
                           facecolor='#BBDEFB', edgecolor='#333', linewidth=1)
    ax.add_patch(pkt0)
    ax.text(1.5, 7.0, 'IP 数据报', fontsize=8, fontweight='bold', color='#333')
    ax.text(1.5, 6.5, 'IP Hdr | Payload', fontsize=7, fontfamily='monospace')

    # After Push
    pkt1 = FancyBboxPatch((5, 6.2), 3.2, 1.2, boxstyle="round,pad=0.05",
                           facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(pkt1)
    ax.text(6.6, 7.0, 'L1 | IP 数据报', fontsize=8, fontweight='bold', color='#2E7D32')
    ax.text(6.6, 6.5, 'L1 | IP Hdr | Payload', fontsize=7, fontfamily='monospace')

    # After Swap
    pkt2 = FancyBboxPatch((10.5, 6.2), 3.2, 1.2, boxstyle="round,pad=0.05",
                           facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.5)
    ax.add_patch(pkt2)
    ax.text(12.1, 7.0, 'L2 | IP 数据报', fontsize=8, fontweight='bold', color='#F9A825')
    ax.text(12.1, 6.5, 'L2 | IP Hdr | Payload', fontsize=7, fontfamily='monospace')

    # After Pop
    pkt3 = FancyBboxPatch((15.2, 6.2), 2.4, 1.2, boxstyle="round,pad=0.05",
                           facecolor='#FFCDD2', edgecolor='#C62828', linewidth=1.5)
    ax.add_patch(pkt3)
    ax.text(16.4, 7.0, 'IP 数据报', fontsize=8, fontweight='bold', color='#333')
    ax.text(16.4, 6.5, 'IP Hdr | Payload', fontsize=7, fontfamily='monospace')

    # Frame structure below
    ax.text(9, 2.5, 'MPLS 标签帧结构 ("垫层 2.5")：', fontsize=9, fontweight='bold', ha='center')
    flds = [('以太网\n首部', '#BBDEFB'), ('MPLS\n首部\n(4B/标签)', '#FFE0B2'),
            ('IP 数据报', '#C8E6C9'), ('CRC', '#F8BBD0')]
    x0 = 3
    for label, color in flds:
        w = len(label.split('\n')[0]) * 0.4 + 1.5
        rect = FancyBboxPatch((x0, 0.8), w, 1.2, boxstyle="round,pad=0.05",
                               facecolor=color, edgecolor='#333', linewidth=0.8)
        ax.add_patch(rect)
        ax.text(x0 + w / 2, 1.4, label, ha='center', fontsize=7.5, fontweight='bold')
        x0 += w + 0.1

    # MPLS header breakdown
    ax.text(7, 1.5, 'Label (20b) + TC (3b) + S (1b) + TTL (8b)', fontsize=7,
            fontfamily='monospace', ha='center', color='#555')

    save(fig, 'mpls_operations.png')


# ── 43. CRC Modulo-2 Division ──────────────────────────────────────────
def draw_crc_division():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('CRC 校验：多项式模 2 除法', fontsize=14, fontweight='bold', pad=15)

    # Setup: D = 101110, G = 1001 (x^3+1), r = 3
    ax.text(1, 9.5, '发送方计算 CRC 校验比特', fontsize=11, fontweight='bold', color='#1565C0')
    ax.text(1, 9.0, r'数据 $D = 101110$, 生成多项式 $G = 1001$ ($x^3+1$, $r=3$)',
            fontsize=9.5, fontfamily='monospace')

    # Step: D << r = 101110000
    ax.text(1, 8.2, r'① $D \ll r$ = 101110000 (左移 $r=3$ 位，附加 0)', fontsize=9, fontfamily='monospace')

    # Long division (modulo-2) — shown as polynomial long division visual
    # I'll draw it as formatted text lines
    division_lines = [
        "                    101011",
        "           ┌──────────────────",
        "    1001   │ 101110000",
        "            ⊕ 1001",
        "           ─────────",
        "               01010",
        "              ⊕ 0000  (模2: 0⊕0=0)",
        "              ─────────",
        "                1010",
        "               ⊕ 1001",
        "              ─────────",
        "                 01100",
        "                ⊕ 0000",
        "                ─────────",
        "                  1100",
        "                 ⊕ 1001",
        "                ─────────",
        "                   1010  ← 余数 R = 101",
        "                  ⊕ 1001",
        "                  ─────────",
        "                    011  ← 最终余数 = 011",
    ]

    for i, line in enumerate(division_lines):
        ax.text(1, 7.7 - i * 0.32, line, fontsize=7.5, fontfamily='monospace', color='#333')

    # Result
    ax.text(1, 2.5, r'② 余数 $R = 011$', fontsize=9, fontfamily='monospace', color='#C62828', fontweight='bold')
    ax.text(1, 2.1, r'③ 发送方发送：$D \ll r \oplus R = 101110011$', fontsize=9, fontfamily='monospace', color='#1565C0', fontweight='bold')

    # Right side: CRC concept
    ax.text(10, 9.5, '接收方验证', fontsize=11, fontweight='bold', color='#2E7D32')
    ax.text(10, 9.0, r'接收方用 G 除收到的整个比特串', fontsize=9)
    ax.text(10, 8.5, r'$(D \ll r) \oplus R$', fontsize=9, fontfamily='monospace')
    ax.text(10, 7.8, '若余数为 0：无差错', fontsize=9, color='#2E7D32', fontweight='bold')
    ax.text(10, 7.3, '若余数非 0：检测到差错', fontsize=9, color='#C62828', fontweight='bold')

    # Common CRC polynomials
    ax.text(10, 6.3, '常见 CRC 生成多项式：', fontsize=9, fontweight='bold')
    crc_polys = [
        'CRC-8:    $x^8+x^2+x+1$',
        'CRC-16:   $x^{16}+x^{15}+x^2+1$',
        'CRC-CCITT:$x^{16}+x^{12}+x^5+1$',
        'CRC-32:   $x^{32}+x^{26}+x^{23}+x^{22}$',
        '              $+x^{16}+x^{12}+x^{11}+$',
        '              $x^{10}+x^8+x^7+x^5+x^4$',
        '              $+x^2+x+1$',
    ]
    for i, poly in enumerate(crc_polys):
        ax.text(10, 5.8 - i * 0.45, poly, fontsize=8, fontfamily='monospace', color='#555')

    # Modulo-2 rules
    ax.text(10, 3.3, '模 2 运算规则：', fontsize=9, fontweight='bold')
    ax.text(10, 2.8, '加法/减法 = XOR (无进位/借位)', fontsize=8, color='#555')
    ax.text(10, 2.4, '0⊕0=0  0⊕1=1  1⊕0=1  1⊕1=0', fontsize=8, fontfamily='monospace', color='#555')
    ax.text(10, 1.9, '乘法: AND  除法: XOR + 移位', fontsize=8, color='#555')

    save(fig, 'crc_division.png')


# ── 49. RSA Public Key Encryption ─────────────────────────────────────────
def draw_rsa_overview():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('RSA 公开密钥加密流程', fontsize=14, fontweight='bold', pad=15)

    # Alice side
    ax.text(2, 5.3, 'Alice', ha='center', fontsize=12, fontweight='bold', color='#1565C0')
    box1 = FancyBboxPatch((0.5, 3.8), 3, 1.0, boxstyle="round,pad=0.08",
                          facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(box1)
    ax.text(2, 4.3, '明文 $m$', ha='center', fontsize=10, fontfamily='monospace')

    # Arrow
    ax.annotate('', xy=(4.0, 4.3), xytext=(3.6, 4.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # Encryption box
    box2 = FancyBboxPatch((4.0, 3.8), 2.2, 1.0, boxstyle="round,pad=0.08",
                          facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.5)
    ax.add_patch(box2)
    ax.text(5.1, 4.45, '$c = m^e$ mod $n$', ha='center', fontsize=9, fontfamily='monospace', fontweight='bold')
    ax.text(5.1, 4.0, '加密', ha='center', fontsize=8, color='#555')

    # Public key input
    ax.annotate('Bob 的公钥\n$(n, e)$', xy=(5.1, 4.9), xytext=(5.1, 5.7),
                ha='center', fontsize=8, color='#E65100',
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=1))

    # Arrow to ciphertext
    ax.annotate('', xy=(7.0, 4.3), xytext=(6.2, 4.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # Ciphertext in transit
    ax.text(8.3, 4.3, '密文 $c$ (经网络传输)', ha='center', fontsize=9, color='#C62828',
            bbox=dict(boxstyle='round', facecolor='#FFCDD2', edgecolor='#C62828', alpha=0.7))

    # Arrow to decryption
    ax.annotate('', xy=(10.5, 4.3), xytext=(9.2, 4.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    # Decryption box
    box3 = FancyBboxPatch((10.5, 3.8), 2.2, 1.0, boxstyle="round,pad=0.08",
                          facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(box3)
    ax.text(11.6, 4.45, '$m = c^d$ mod $n$', ha='center', fontsize=9, fontfamily='monospace', fontweight='bold')
    ax.text(11.6, 4.0, '解密', ha='center', fontsize=8, color='#555')

    # Private key input
    ax.annotate('Bob 的私钥\n$(n, d)$', xy=(11.6, 4.9), xytext=(11.6, 5.7),
                ha='center', fontsize=8, color='#2E7D32',
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1))

    # Bob side
    ax.text(11.6, 5.3, 'Bob', ha='center', fontsize=12, fontweight='bold', color='#2E7D32')

    # Arrow to plaintext
    ax.annotate('', xy=(13.3, 4.3), xytext=(12.7, 4.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
    ax.text(13.8, 4.3, '明文 $m$', ha='center', fontsize=10, fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#C8E6C9', edgecolor='#2E7D32'))

    # Key generation steps at bottom
    ax.text(7, 2.5, '密钥生成 (Bob):', fontsize=10, fontweight='bold', ha='center')
    steps = '① 选大素数 p, q → ② n = pq, z = (p−1)(q−1) → ③ 选 e 与 z 互素 → ④ 求 d 使 ed mod z = 1'
    ax.text(7, 2.0, steps, ha='center', fontsize=8.5, fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', edgecolor='#999'))

    # Trudy at bottom
    ax.text(8.3, 1.3, 'Trudy 可截获密文 c 和公钥 (n, e)，但无法从 n 分解出 p, q → 无法计算 d', ha='center',
            fontsize=8, color='#C62828')

    # Box around the whole flow
    rect = FancyBboxPatch((0.2, 3.4), 14.1, 2.2, boxstyle="round,pad=0.1",
                          facecolor='none', edgecolor='#999', linewidth=1, linestyle='--')
    ax.add_patch(rect)

    save(fig, 'rsa_overview.png')


# ── 50. Digital Signature Process ──────────────────────────────────────────
def draw_digital_signature():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle('数字签名：签名与验证', fontsize=14, fontweight='bold', y=0.98)

    # ── Signing (left) ──
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Alice 签名', fontsize=12, fontweight='bold', color='#1565C0')

    # Message
    box = FancyBboxPatch((0.5, 5.3), 3, 0.8, boxstyle="round,pad=0.06",
                         facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.2)
    ax.add_patch(box)
    ax.text(2, 5.7, '消息 $m$', ha='center', fontsize=10, fontfamily='monospace')

    # Hash arrow
    ax.annotate('', xy=(2, 5.0), xytext=(2, 5.3),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2))

    # Hash
    box = FancyBboxPatch((0.5, 4.2), 3, 0.8, boxstyle="round,pad=0.06",
                         facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.2)
    ax.add_patch(box)
    ax.text(2, 4.6, '$H(m)$ (哈希摘要)', ha='center', fontsize=9)

    # Sign arrow
    ax.annotate('', xy=(2, 4.2), xytext=(2, 3.9),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2))

    # Sign with private key
    box = FancyBboxPatch((0.5, 3.1), 3, 0.8, boxstyle="round,pad=0.06",
                         facecolor='#FFCDD2', edgecolor='#C62828', linewidth=1.5)
    ax.add_patch(box)
    ax.text(2, 3.5, '$K_A^-(H(m))$', ha='center', fontsize=10, fontfamily='monospace', fontweight='bold')
    ax.text(2, 3.2, '签名 (用私钥加密哈希)', ha='center', fontsize=8, color='#555')

    # Private key label
    ax.annotate('Alice 的私钥 $K_A^-$', xy=(4.5, 3.5), fontsize=8, color='#C62828',
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=1))

    # Send
    ax.annotate('', xy=(4, 5.5), xytext=(3.5, 5.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.text(6, 5.5, '发送 $(m, K_A^-(H(m)))$', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='#E3F2FD', edgecolor='#1565C0'))

    # ── Verification (right) ──
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('Bob 验证', fontsize=12, fontweight='bold', color='#2E7D32')

    # Received
    ax.text(5, 6.3, '收到 $(m, \\text{signature})$', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='#E3F2FD', edgecolor='#1565C0'))

    # Two paths
    ax.text(2, 5.5, '消息 $m$', ha='center', fontsize=9)
    ax.annotate('', xy=(2, 5.2), xytext=(2, 5.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1))
    box = FancyBboxPatch((0.5, 4.6), 3, 0.6, boxstyle="round,pad=0.06",
                         facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.2)
    ax.add_patch(box)
    ax.text(2, 4.9, '$H(m)$', ha='center', fontsize=10, fontfamily='monospace')

    ax.text(8, 5.5, '签名', ha='center', fontsize=9)
    ax.annotate('', xy=(8, 5.2), xytext=(8, 5.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1))
    box = FancyBboxPatch((6.5, 4.6), 3, 0.6, boxstyle="round,pad=0.06",
                         facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(box)
    ax.text(8, 4.9, '$K_A^+(\\text{sig})$', ha='center', fontsize=10, fontfamily='monospace')
    ax.text(8, 4.3, '(用公钥解密)', ha='center', fontsize=8, color='#555')

    # Alice's public key
    ax.annotate("Alice 的公钥 $K_A^+$", xy=(9.5, 4.9), fontsize=8, color='#2E7D32',
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1))

    # Compare
    ax.annotate('', xy=(5, 4.9), xytext=(3.5, 4.9),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2))
    ax.annotate('', xy=(5, 4.9), xytext=(6.5, 4.9),
                arrowprops=dict(arrowstyle='->', color='#333', lw=1.2))

    box = FancyBboxPatch((3.5, 3.5), 3, 0.8, boxstyle="round,pad=0.08",
                         facecolor='#E8EAF6', edgecolor='#283593', linewidth=1.5)
    ax.add_patch(box)
    ax.text(5, 3.9, '比较是否相等？', ha='center', fontsize=10, fontweight='bold')

    # Result
    ax.text(5, 2.7, '匹配 → 消息完整且来自 Alice', ha='center', fontsize=10, color='#2E7D32', fontweight='bold')
    ax.text(5, 2.2, '不匹配 → 被篡改或冒充', ha='center', fontsize=9, color='#C62828')

    save(fig, 'digital_signature.png')


# ── 51. ap4.0 Nonce Authentication ────────────────────────────────────────
def draw_ap4_auth():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    ax.set_title('ap4.0：基于 Nonce 的端点认证', fontsize=13, fontweight='bold', pad=15)

    # Alice
    ax.text(1, 5.5, 'Alice', ha='center', fontsize=12, fontweight='bold', color='#1565C0')
    # Bob
    ax.text(7, 5.5, 'Bob', ha='center', fontsize=12, fontweight='bold', color='#2E7D32')

    # Shared key
    ax.text(4, 6.2, '共享密钥 $K_{A-B}$', ha='center', fontsize=9, color='#555',
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', edgecolor='#999'))

    # Step 1
    ax.annotate('', xy=(6.5, 4.9), xytext=(1.5, 4.9),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.text(4, 5.1, '① "I am Alice"', ha='center', fontsize=10)

    # Step 2
    ax.annotate('', xy=(1.5, 4.3), xytext=(6.5, 4.3),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5))
    ax.text(4, 4.5, '② Nonce $R$ (一次性随机数)', ha='center', fontsize=10, color='#E65100')

    # Step 3
    ax.annotate('', xy=(6.5, 3.5), xytext=(1.5, 3.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.text(4, 3.7, '③ $K_{A-B}(R)$ (加密 Nonce)', ha='center', fontsize=10, fontfamily='monospace')

    # Verification
    box = FancyBboxPatch((5.5, 2.5), 2.3, 0.7, boxstyle="round,pad=0.06",
                         facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(box)
    ax.text(6.65, 2.85, "Bob 解密验证:", ha='center', fontsize=9, fontweight='bold')
    ax.text(6.65, 2.6, "$K_{A-B}(K_{A-B}(R)) = R ?$", ha='center', fontsize=9, fontfamily='monospace')

    # Trudy attack
    ax.text(1, 2.0, 'Trudy 截获了 $K_{A-B}(R)$', ha='center', fontsize=8, color='#C62828')
    ax.text(1, 1.6, '但下次会话 Bob 发送', ha='center', fontsize=8, color='#C62828')
    ax.text(1, 1.2, "新的 Nonce $R'$，重放失效", ha='center', fontsize=8, color='#C62828', fontweight='bold')

    # Connect Trudy to the message path
    rect = FancyBboxPatch((0.3, 0.5), 7.4, 2.0, boxstyle="round,pad=0.08",
                          facecolor='#FFEBEE', edgecolor='#C62828', linewidth=1.2, linestyle='--')
    ax.add_patch(rect)
    ax.text(4, 2.15, '⚠ Trudy (嗅探 & 重放攻击) ⚠', ha='center', fontsize=8, color='#C62828')

    save(fig, 'ap4_auth.png')


# ── 52. IPsec ESP Tunnel Mode ─────────────────────────────────────────────
def draw_ipsec_tunnel():
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('IPsec ESP 隧道模式数据报结构', fontsize=13, fontweight='bold', pad=15)

    y = 7.5
    # New IP header
    rect = FancyBboxPatch((1, y), 12, 0.55, boxstyle="round,pad=0.05",
                          facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7, y + 0.28, '新 IP 首部（源=隧道入口, 目的=隧道出口）', ha='center', fontsize=9)
    ax.text(12.2, y + 0.28, '→ 明文', fontsize=8, color='#2E7D32')

    y -= 0.65
    # ESP Header
    rect = FancyBboxPatch((1, y), 12, 0.55, boxstyle="round,pad=0.05",
                          facecolor='#FFF9C4', edgecolor='#F9A825', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7, y + 0.28, 'ESP 首部（SPI + 序号）', ha='center', fontsize=9)
    ax.text(12.2, y + 0.28, '→ 明文', fontsize=8, color='#2E7D32')

    y -= 0.65
    # Original IP header (encrypted)
    rect = FancyBboxPatch((2, y), 10, 0.55, boxstyle="round,pad=0.05",
                          facecolor='#E1BEE7', edgecolor='#6A1B9A', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7, y + 0.28, '原始 IP 首部（加密）', ha='center', fontsize=9)
    ax.text(12.2, y + 0.28, '→ 密文', fontsize=8, color='#C62828')

    y -= 0.65
    # Original IP payload (encrypted)
    rect = FancyBboxPatch((2, y), 10, 0.55, boxstyle="round,pad=0.05",
                          facecolor='#E1BEE7', edgecolor='#6A1B9A', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7, y + 0.28, '原始 IP 载荷（TCP/UDP 报文段，加密）', ha='center', fontsize=9)
    ax.text(12.2, y + 0.28, '→ 密文', fontsize=8, color='#C62828')

    y -= 0.65
    # ESP Trailer
    rect = FancyBboxPatch((2, y), 10, 0.55, boxstyle="round,pad=0.05",
                          facecolor='#FFCCBC', edgecolor='#BF360C', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7, y + 0.28, 'ESP Trailer（填充 + 下一首部标识）', ha='center', fontsize=9)
    ax.text(12.2, y + 0.28, '→ 密文', fontsize=8, color='#C62828')

    y -= 0.75
    # ESP Auth (MAC)
    rect = FancyBboxPatch((1, y), 12, 0.55, boxstyle="round,pad=0.05",
                          facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7, y + 0.28, 'ESP Auth（MAC — 对 ESP 首部 + 载荷 + Trailer 的认证）', ha='center', fontsize=9)
    ax.text(12.2, y + 0.28, '→ 明文', fontsize=8, color='#2E7D32')

    y -= 0.65
    # ESP coverage annotation on right
    ax.annotate('',
                xy=(0.3, 4.5), xytext=(0.3, 7.8),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1))

    ax.annotate('',
                xy=(0.3, 2.6), xytext=(0.3, 4.5),
                arrowprops=dict(arrowstyle='->', color='#999', lw=1))

    ax.text(0.2, 7.0, '认证\n范围', ha='center', fontsize=8, color='#555', rotation=90, va='center')
    ax.text(0.2, 3.5, '加密\n范围', ha='center', fontsize=8, color='#555', rotation=90, va='center')

    # Legend
    ax.text(7, 0.8, '隧道模式：整个原始 IP 数据报（首部+载荷）被加密后封装在新的 IP 数据报中。中间路由器仅见隧道端点地址。',
            ha='center', fontsize=8, color='#555',
            bbox=dict(boxstyle='round', facecolor='#FAFAFA', edgecolor='#CCC'))

    save(fig, 'ipsec_tunnel.png')


# ── 53. 802.11i 4-Way Handshake ────────────────────────────────────────────
def draw_wpa2_handshake():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('802.11i / WPA2 四步握手', fontsize=13, fontweight='bold', pad=15)

    # Supplicant & Authenticator
    ax.text(1.5, 7.5, '主机\n(Supplicant)', ha='center', fontsize=11, fontweight='bold', color='#1565C0')
    ax.text(6.5, 7.5, 'AP\n(Authenticator)', ha='center', fontsize=11, fontweight='bold', color='#2E7D32')

    # PMK known
    ax.text(4, 4.8, '双方均已持有 PMK', ha='center', fontsize=9, color='#555',
            bbox=dict(boxstyle='round', facecolor='#F5F5F5', edgecolor='#999'))

    # Step 1
    ax.annotate('', xy=(5.8, 4.2), xytext=(2.2, 4.2),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5))
    ax.text(4, 4.45, '① ANonce (AP 生成的随机数)', ha='center', fontsize=10, color='#E65100')

    # Step 2
    ax.annotate('', xy=(2.2, 3.4), xytext=(5.8, 3.4),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.text(4, 3.65, '② SNonce (主机生成的随机数) + MIC', ha='center', fontsize=10, color='#E65100')

    # Step 3
    ax.annotate('', xy=(5.8, 2.6), xytext=(2.2, 2.6),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.5))
    ax.text(4, 2.85, '③ MIC + GTK (加密)', ha='center', fontsize=10, color='#E65100')

    # Step 4
    ax.annotate('', xy=(2.2, 1.8), xytext=(5.8, 1.8),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.text(4, 2.05, '④ ACK (确认)', ha='center', fontsize=10, color='#E65100')

    # Key derivation box
    box = FancyBboxPatch((0.5, 0.3), 7, 1.2, boxstyle="round,pad=0.08",
                         facecolor='#E8EAF6', edgecolor='#283593', linewidth=1.5)
    ax.add_patch(box)
    ax.text(4, 1.3, '密钥推导：PMK + ANonce + SNonce → PTK', ha='center', fontsize=10, fontfamily='monospace', fontweight='bold')
    ax.text(4, 0.8, 'PTK → KCK (MIC密钥) | KEK (加密GTK用) | TK (数据加密)', ha='center', fontsize=9)
    ax.text(4, 0.45, 'GTK (Group Temporal Key) 用于广播/多播帧', ha='center', fontsize=8, color='#555')

    # MIC note
    ax.text(1.5, 5.2, 'MIC (Message Integrity Code)\n保护握手消息不被篡改', ha='center', fontsize=8, color='#555',
            bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F9A825'))

    save(fig, 'wpa2_handshake.png')


# ── 54. RTP Header Format ─────────────────────────────────────────────────
def draw_rtp_header():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('RTP 首部格式（12 字节固定部分）', fontsize=14, fontweight='bold', pad=20)

    fields = [
        ("V=2 (2)", 0, 2, 5, 0.5, '#E3F2FD'),
        ("P (1)", 2, 3, 5, 0.5, '#E3F2FD'),
        ("X (1)", 3, 4, 5, 0.5, '#E3F2FD'),
        ("CC (4)", 4, 8, 5, 0.5, '#E3F2FD'),
        ("M (1)", 8, 9, 5, 0.5, '#FFF9C4'),
        ("载荷类型 PT (7 bit)", 9, 16, 5, 0.5, '#FFF9C4'),
        ("序号 Sequence Number (16 bit)", 16, 32, 5, 0.5, '#C8E6C9'),
        ("时间戳 Timestamp (32 bit)", 0, 32, 4, 0.7, '#BBDEFB'),
        ("SSRC 同步源标识符 (32 bit)", 0, 32, 3, 0.7, '#FFCCBC'),
        ("CSRC 贡献源标识符列表 (0–15 × 32 bit)", 0, 32, 2, 0.7, '#ECEFF1'),
    ]

    for label, x0, x1, row, h, color in fields:
        w = x1 - x0
        rect = FancyBboxPatch((x0, row), w, h, boxstyle="round,pad=0.04",
                              facecolor=color, edgecolor='#333', linewidth=1.2)
        ax.add_patch(rect)
        ax.text((x0 + x1) / 2, row + h / 2, label, ha='center', va='center', fontsize=8)

    # Annotations
    ax.text(20, 5.5, '0                   1                   2                   3', fontsize=7, fontfamily='monospace',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    ax.text(0.5, 5.7, '字节 0–3', fontsize=7, color='#555')
    ax.text(0.5, 4.7, '字节 4–7', fontsize=7, color='#555')
    ax.text(0.5, 3.7, '字节 8–11', fontsize=7, color='#555')
    ax.text(0.5, 2.7, '字节 12+', fontsize=7, color='#555')

    ax.text(16, 1.5, 'RTP 运行在 UDP 之上，为实时媒体提供序号（检测丢包/重排序）和时间戳（去抖动播放）', ha='center',
            fontsize=9, color='#555', bbox=dict(boxstyle='round', facecolor='#FAFAFA', edgecolor='#CCC'))

    save(fig, 'rtp_header.png')


# ── 55. SIP Call Flow ─────────────────────────────────────────────────────
def draw_sip_call_flow():
    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    ax.set_title('SIP 呼叫建立流程', fontsize=13, fontweight='bold', pad=15)

    # Entities
    entities = [('Alice', 1.5), ('Proxy\natlanta', 4.5), ('Proxy\nbiloxi', 7.5), ('Bob', 10.5)]
    for name, x in entities:
        ax.text(x, 8.2, name, ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='#E3F2FD', edgecolor='#1565C0'))
        ax.axvline(x=x, ymin=0.08, ymax=0.92, linestyle='--', color='#CCC', lw=0.8)

    y = 7.8
    dy = 0.7
    messages = [
        ('INVITE', 1.5, 4.5, '#1565C0'),
        ('INVITE', 4.5, 7.5, '#1565C0'),
        ('INVITE', 7.5, 10.5, '#1565C0'),
        ('100 Trying', 4.5, 1.5, '#999'),
        ('100 Trying', 7.5, 4.5, '#999'),
        ('180 Ringing', 10.5, 7.5, '#999'),
        ('180 Ringing', 7.5, 4.5, '#999'),
        ('180 Ringing', 4.5, 1.5, '#999'),
        ('200 OK', 10.5, 7.5, '#2E7D32'),
        ('200 OK', 7.5, 4.5, '#2E7D32'),
        ('200 OK', 4.5, 1.5, '#2E7D32'),
        ('ACK (端到端)', 1.5, 10.5, '#FF6F00'),
    ]

    y_positions = [7.8, 7.1, 6.4, 5.9, 5.5, 5.1, 4.7, 4.3, 3.9, 3.5, 3.1, 2.7]
    for i, (msg, x1, x2, color) in enumerate(messages):
        yy = y_positions[i]
        ax.annotate('', xy=(x2, yy), xytext=(x1, yy),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.3))
        ha = 'center' if msg in ('ACK (端到端)',) else 'center'
        mx = (x1 + x2) / 2
        ax.text(mx, yy + 0.15, msg, ha='center', fontsize=8, color=color, fontweight='bold')

    # RTP direct media
    ax.text(6, 2.0, 'RTP 媒体流（UDP 端点直连，不经过代理）', ha='center', fontsize=9, color='#E65100', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#FFF3E0', edgecolor='#E65100'))

    # Session end
    ax.annotate('', xy=(10.5, 1.3), xytext=(1.5, 1.3),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.3))
    ax.text(6, 1.55, 'BYE', ha='center', fontsize=8, color='#C62828', fontweight='bold')
    ax.annotate('', xy=(1.5, 0.8), xytext=(10.5, 0.8),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1.3))
    ax.text(6, 1.05, '200 OK', ha='center', fontsize=8, color='#2E7D32', fontweight='bold')

    ax.text(6, 0.3, '• INVITE 通过代理链路由  • 后续 SIP 消息可端到端  • RTP 媒体永远是端到端', ha='center',
            fontsize=8, color='#555')

    save(fig, 'sip_call_flow.png')


# ── 56. Leaky Bucket vs Token Bucket ──────────────────────────────────────
def draw_leaky_vs_token_bucket():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('流量整形：漏桶 vs 令牌桶', fontsize=13, fontweight='bold', y=0.98)

    # Leaky Bucket
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('漏桶 (Leaky Bucket)', fontsize=11, fontweight='bold')

    # Draw bucket
    bucket = FancyBboxPatch((3, 2), 4, 3.5, boxstyle="round,pad=0.1",
                            facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(bucket)
    ax.text(5, 5.5, '缓冲区 (队列)', ha='center', fontsize=9)
    ax.text(5, 5.1, '输入 → 突发', ha='center', fontsize=8, color='#C62828')

    # Arrow in
    ax.annotate('', xy=(5, 6.5), xytext=(5, 7.5),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2))
    ax.text(5, 7.0, '分组到达\n(速率波动)', ha='center', fontsize=8, color='#C62828')

    # Arrow out
    ax.annotate('', xy=(9, 3.5), xytext=(7, 3.5),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(9.5, 3.5, '恒定速率\n输出', ha='center', fontsize=8, color='#2E7D32')

    ax.text(5, 0.8, '无论输入如何波动\n输出始终恒定速率 r', ha='center', fontsize=9, color='#555')

    # Token Bucket
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('令牌桶 (Token Bucket)', fontsize=11, fontweight='bold')

    # Draw bucket
    bucket = FancyBboxPatch((3, 2), 4, 3.5, boxstyle="round,pad=0.1",
                            facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(bucket)
    ax.text(5, 5.5, '桶容量 b', ha='center', fontsize=9)
    ax.text(5, 5.1, '(最多容纳 b 个令牌)', ha='center', fontsize=7, color='#555')

    # Tokens entering
    ax.annotate('', xy=(5, 6.5), xytext=(5, 7.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(5, 7.0, '令牌到达 (速率 r)', ha='center', fontsize=8, color='#1565C0')

    # Packets arriving
    ax.annotate('', xy=(5.5, 4.5), xytext=(5.5, 3.5),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=1.5))

    # Out
    ax.annotate('', xy=(9, 3.5), xytext=(7, 3.5),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(9.5, 3.5, '需令牌\n才可输出', ha='center', fontsize=8, color='#2E7D32')

    ax.text(5, 0.8, '参数 (r, b)：平均速率 r\n允许最大突发 b', ha='center', fontsize=9, color='#555')

    # Comparison box
    ax.text(5, 0.2, '任意时间 t 内送出数 ≤ rt + b', ha='center', fontsize=9, fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='#FFF9C4', edgecolor='#F9A825'))

    save(fig, 'leaky_vs_token_bucket.png')


# ── 57. Diffserv Architecture ──────────────────────────────────────────────
def draw_diffserv():
    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('Diffserv 体系结构：边缘分类标记 + 核心按 PHB 转发', fontsize=13, fontweight='bold', pad=15)

    # Edge routers
    for x, label, color in [(2.5, '入口边缘路由器\n分类 + 标记 DSCP', '#BBDEFB'),
                              (11.5, '出口边缘路由器\n可能重塑流量', '#BBDEFB')]:
        rect = FancyBboxPatch((x - 1.8, 2.8), 3.6, 1.4, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#1565C0', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, 3.5, label, ha='center', fontsize=9)

    # Core routers in middle
    rect = FancyBboxPatch((5.5, 2.8), 4.2, 1.4, boxstyle="round,pad=0.1",
                          facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(7.6, 3.5, '核心路由器\n仅检查 DSCP → 应用 PHB\n(不维护每流状态)', ha='center', fontsize=9)

    # Arrows between routers
    ax.annotate('', xy=(5.2, 3.5), xytext=(4.3, 3.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.annotate('', xy=(10, 3.5), xytext=(9.7, 3.5),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))

    # Ingress/egress labels
    ax.text(0.3, 3.5, '进入\nDS 域', ha='center', fontsize=8, color='#555')
    ax.text(13.7, 3.5, '离开\nDS 域', ha='center', fontsize=8, color='#555')

    # PHB table below
    ax.text(7, 2.2, 'DSCP → PHB 映射', ha='center', fontsize=10, fontweight='bold')

    phb_data = [
        ('EF (Expedited Forwarding)', 'VoIP：极低延迟/抖动/丢包', '#FFCCBC'),
        ('AF4x (Assured, 高优先级)', '流媒体/视频会议', '#FFF9C4'),
        ('AF1x (Assured, 低优先级)', '关键业务数据', '#C8E6C9'),
        ('BE (Best Effort 000000)', '普通数据 (Web, FTP, Email)', '#ECEFF1'),
    ]

    for i, (phb, use, color) in enumerate(phb_data):
        yy = 1.7 - i * 0.35
        rect = FancyBboxPatch((2, yy), 5, 0.3, boxstyle="round,pad=0.03",
                              facecolor=color, edgecolor='#999', linewidth=1)
        ax.add_patch(rect)
        ax.text(4.5, yy + 0.15, phb, ha='center', fontsize=8, fontweight='bold')
        ax.text(9.5, yy + 0.15, use, ha='center', fontsize=8, color='#555')

    save(fig, 'diffserv_architecture.png')


# ── 49. TLS 1.3 Handshake ────────────────────────────────────────────────
def draw_tls_handshake():
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('TLS 1.3 握手（1-RTT）', fontsize=14, fontweight='bold', pad=15)

    client_x, server_x = 2, 8
    ax.plot([client_x, client_x], [0.5, 9.5], '#1565C0', linewidth=2)
    ax.plot([server_x, server_x], [0.5, 9.5], '#C62828', linewidth=2)
    ax.text(client_x, 9.8, '客户端', ha='center', fontsize=11, fontweight='bold', color='#1565C0')
    ax.text(server_x, 9.8, '服务器', ha='center', fontsize=11, fontweight='bold', color='#C62828')

    # Phase 1: ClientHello
    ax.annotate('', xy=(server_x, 3.5), xytext=(client_x, 2.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(5, 2.2, 'ClientHello\n(支持的密码套件、密钥共享、SNI)', ha='center', fontsize=8, color='#1565C0')

    # Phase 2: ServerHello + extensions
    ax.annotate('', xy=(client_x, 5.5), xytext=(server_x, 4.5),
                arrowprops=dict(arrowstyle='->', color='#C62828', lw=2))
    ax.text(5, 4.2, 'ServerHello\n(选定的密码套件、密钥共享)\n+ 证书 + 证书验证 + Finished', ha='center', fontsize=8, color='#C62828')

    # Phase 3: Client Finished
    ax.annotate('', xy=(server_x, 7.5), xytext=(client_x, 6.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2))
    ax.text(5, 6.2, 'Finished\n(认证 + 加密就绪)', ha='center', fontsize=8, color='#1565C0')

    # Phase annotations
    ax.text(0.3, 3.0, '密钥\n协商', ha='center', fontsize=7, color='#888')
    ax.text(0.3, 5.0, '服务器\n认证', ha='center', fontsize=7, color='#888')
    ax.text(0.3, 7.0, '握手\n完成', ha='center', fontsize=7, color='#888')

    # Application data after handshake
    ax.annotate('', xy=(server_x, 8.8), xytext=(client_x, 8.3),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(5, 7.9, '应用数据（加密）', ha='center', fontsize=8, color='#2E7D32', fontweight='bold')

    # RTT bracket
    ax.annotate('', xy=(1.2, 3.5), xytext=(1.2, 8.5),
                arrowprops=dict(arrowstyle='<->', color='#888', lw=1, linestyle='dashed'))
    ax.text(0.5, 6, '1-RTT\n握手', ha='center', fontsize=9, color='#888', fontstyle='italic')

    save(fig, 'tls_handshake.png')


# ── 50. ARP Query/Response ───────────────────────────────────────────────
def draw_arp_process():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('ARP：地址解析协议查询与响应', fontsize=14, fontweight='bold', pad=15)

    # Source and destination nodes
    src_x, dest_x = 2, 8
    ax.plot([src_x, src_x], [0.5, 6.5], '#1565C0', linewidth=2)
    ax.plot([dest_x, dest_x], [0.5, 6.5], '#C62828', linewidth=2)

    # Node labels with addresses
    ax.text(src_x, 6.8, '主机 A\nIP: 192.168.1.5\nMAC: AA-AA-AA-AA-AA', ha='center', fontsize=8, fontweight='bold', color='#1565C0')
    ax.text(dest_x, 6.8, '主机 B\nIP: 192.168.1.10\nMAC: BB-BB-BB-BB-BB', ha='center', fontsize=8, fontweight='bold', color='#C62828')

    # ARP Query (broadcast)
    ax.annotate('', xy=(dest_x, 4), xytext=(src_x, 3),
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=2))
    ax.text(5, 2.5, 'ARP 查询（广播）\n"192.168.1.10 的 MAC 地址是什么？"\n目的 MAC: FF-FF-FF-FF-FF-FF', ha='center', fontsize=8, color='#E65100')

    # Broadcast shower
    ax.annotate('', xy=(7, 4.5), xytext=(5.5, 3.8),
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=1, alpha=0.3))
    ax.annotate('', xy=(3, 4.5), xytext=(4.5, 3.8),
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=1, alpha=0.3))
    ax.text(7.5, 4.2, '其他主机\n忽略', ha='center', fontsize=6, color='#aaa')
    ax.text(2.5, 4.2, '其他主机\n忽略', ha='center', fontsize=6, color='#aaa')

    # ARP Response (unicast)
    ax.annotate('', xy=(src_x, 5.5), xytext=(dest_x, 5),
                arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=2))
    ax.text(5, 5.8, 'ARP 响应（单播）\n"我的 MAC 是 BB-BB-BB-BB-BB"\n目的 MAC: AA-AA-AA-AA-AA', ha='center', fontsize=8, color='#2E7D32')

    # ARP table annotation
    ax.text(src_x, 1.2, 'ARP 表更新：\n192.168.1.10 →\nBB-BB-BB-BB-BB\n(TTL: 20 min)', ha='center', fontsize=7, color='#1565C0', style='italic')

    save(fig, 'arp_process.png')


# ── 51. HTTP Message Format ──────────────────────────────────────────────
def draw_http_message_format():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('HTTP 请求与响应报文格式', fontsize=14, fontweight='bold', pad=20)

    # ── Request (left side) ──
    ax.text(3, 7.5, 'HTTP 请求报文', ha='center', fontsize=12, fontweight='bold', color='#1565C0')

    req_parts = [
        ('请求行 (Request Line)', 'GET /index.html HTTP/1.1\r\n', '#BBDEFB'),
        ('首部行 (Header Lines)', 'Host: www.example.com\r\nConnection: keep-alive\r\n...', '#E3F2FD'),
        ('空行 (CRLF)', '\r\n', '#E0E0E0'),
        ('报文主体 (Message Body)', '（GET/HEAD 通常为空；POST 在此携带表单数据）', '#F5F5F5'),
    ]

    yy = 6.5
    for name, example, color in req_parts:
        rect = FancyBboxPatch((0.3, yy - 0.7), 6, 0.9, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='#1565C0', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(0.6, yy - 0.05, name, fontsize=8, fontweight='bold', color='#1565C0')
        ax.text(0.6, yy - 0.45, example, fontsize=7, color='#333', family='monospace')
        yy -= 1.2

    # ── Response (right side) ──
    ax.text(10.5, 7.5, 'HTTP 响应报文', ha='center', fontsize=12, fontweight='bold', color='#C62828')

    resp_parts = [
        ('状态行 (Status Line)', 'HTTP/1.1 200 OK\r\n', '#FFCDD2'),
        ('首部行 (Header Lines)', 'Content-Type: text/html\r\nContent-Length: 1234\r\n...', '#FFEBEE'),
        ('空行 (CRLF)', '\r\n', '#E0E0E0'),
        ('报文主体 (Message Body)', '<html>...<body>...实际的 HTML 内容...</body></html>', '#F5F5F5'),
    ]

    yy = 6.5
    for name, example, color in resp_parts:
        rect = FancyBboxPatch((7.5, yy - 0.7), 6, 0.9, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='#C62828', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(7.8, yy - 0.05, name, fontsize=8, fontweight='bold', color='#C62828')
        ax.text(7.8, yy - 0.45, example, fontsize=7, color='#333', family='monospace')
        yy -= 1.2

    # Common status codes at bottom
    ax.text(7, 1, '常见状态码：200 OK | 301 Moved Permanently | 304 Not Modified | 400 Bad Request | 404 Not Found | 505 HTTP Version Not Supported', ha='center', fontsize=8, color='#888')

    save(fig, 'http_message_format.png')


# ── 52. PGP Secure Email Flow ────────────────────────────────────────────
def draw_pgp_flow():
    fig, ax = plt.subplots(figsize=(11, 8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('PGP 安全电子邮件：加密 + 签名流程', fontsize=14, fontweight='bold', pad=15)

    # Alice side
    alice_x, bob_x = 1.5, 7.5
    ax.text(alice_x, 9.5, 'Alice（发送方）', ha='center', fontsize=11, fontweight='bold', color='#1565C0')
    ax.text(bob_x, 9.5, 'Bob（接收方）', ha='center', fontsize=11, fontweight='bold', color='#C62828')

    # Step 1: Hash + Sign
    rect = FancyBboxPatch((0.3, 7.0), 2.4, 1.8, boxstyle="round,pad=0.1",
                          facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(rect)
    ax.text(1.5, 8.5, '① 哈希 + 签名', ha='center', fontsize=8, fontweight='bold', color='#1565C0')
    ax.text(1.5, 8.1, 'm → H(m)\n用 $K_A^-$ 签名\n→ {$K_A^-$(H(m))}', ha='center', fontsize=7, color='#333')

    # Step 2: Symmetric encrypt
    rect = FancyBboxPatch((0.3, 4.3), 2.4, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(rect)
    ax.text(1.5, 5.9, '② 对称加密', ha='center', fontsize=8, fontweight='bold', color='#1565C0')
    ax.text(1.5, 5.4, 'm + 签名 →\n用会话密钥 $K_s$\n加密整个包\n→ $K_s$(m, 签名)', ha='center', fontsize=7, color='#333')

    # Step 3: Encrypt Ks with public key
    rect = FancyBboxPatch((0.3, 1.8), 2.4, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(rect)
    ax.text(1.5, 3.3, '③ 加密 $K_s$', ha='center', fontsize=8, fontweight='bold', color='#2E7D32')
    ax.text(1.5, 2.8, '用 Bob 的公钥\n$K_B^+$ 加密 $K_s$\n→ $K_B^+$(K_s)', ha='center', fontsize=7, color='#333')

    # Arrow from Alice to Bob
    ax.annotate('', xy=(7, 5.2), xytext=(3, 5.2),
                arrowprops=dict(arrowstyle='->', color='#333', lw=2))
    ax.text(5, 5.8, '发送：$K_B^+$(K_s) || K_s$(m, 签名)', ha='center', fontsize=7, color='#333')

    # Bob side: Step 1 - Decrypt Ks
    rect = FancyBboxPatch((7.5, 7.0), 3.2, 1.8, boxstyle="round,pad=0.1",
                          facecolor='#C8E6C9', edgecolor='#C62828', linewidth=2)
    ax.add_patch(rect)
    ax.text(9.1, 8.5, '① 解密 $K_s$', ha='center', fontsize=8, fontweight='bold', color='#C62828')
    ax.text(9.1, 8.1, '用 Bob 的私钥\n$K_B^-$ 解密\n→ 得到 $K_s$', ha='center', fontsize=7, color='#333')

    # Bob side: Step 2 - Decrypt message
    rect = FancyBboxPatch((7.5, 4.3), 3.2, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#FFCDD2', edgecolor='#C62828', linewidth=2)
    ax.add_patch(rect)
    ax.text(9.1, 5.9, '② 对称解密', ha='center', fontsize=8, fontweight='bold', color='#C62828')
    ax.text(9.1, 5.4, '用 $K_s$ 解密\n$K_s$(m, 签名)\n→ 得到 m + 签名', ha='center', fontsize=7, color='#333')

    # Bob side: Step 3 - Verify signature
    rect = FancyBboxPatch((7.5, 1.8), 3.2, 2.0, boxstyle="round,pad=0.1",
                          facecolor='#E3F2FD', edgecolor='#C62828', linewidth=2)
    ax.add_patch(rect)
    ax.text(9.1, 3.3, '③ 验证签名', ha='center', fontsize=8, fontweight='bold', color='#C62828')
    ax.text(9.1, 2.8, '用 Alice 的公钥\n$K_A^+$ 验证签名\nH(m) ?= $K_A^+$(签名)', ha='center', fontsize=7, color='#333')

    save(fig, 'pgp_flow.png')


# ── 53. POP3 vs IMAP Comparison ──────────────────────────────────────────
def draw_pop3_imap():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('POP3 与 IMAP 邮件访问协议对比', fontsize=14, fontweight='bold', pad=15)

    # ── POP3 (left) ──
    ax.text(3, 6.7, 'POP3（TCP 110）— "下载后删除"', ha='center', fontsize=11, fontweight='bold', color='#1565C0')

    # Mail server
    rect = FancyBboxPatch((0.8, 4.5), 3.5, 1.8, boxstyle="round,pad=0.1",
                          facecolor='#BBDEFB', edgecolor='#1565C0', linewidth=2)
    ax.add_patch(rect)
    ax.text(2.55, 5.8, '邮件服务器\n(邮件存储)', ha='center', fontsize=9, fontweight='bold')

    # Clients
    for x_pos, label in [(0.2, 'PC'), (2.4, '手机'), (4.6, '笔记本')]:
        rect = FancyBboxPatch((x_pos, 1.5), 1.5, 1.2, boxstyle="round,pad=0.08",
                              facecolor='#E3F2FD', edgecolor='#1565C0', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x_pos + 0.75, 2.1, label, ha='center', fontsize=8)

    # Download arrows (all from server to client)
    ax.annotate('', xy=(0.95, 2.7), xytext=(2.55, 4.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.annotate('', xy=(3.15, 2.7), xytext=(2.55, 4.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))
    ax.annotate('', xy=(5.35, 2.7), xytext=(2.55, 4.5),
                arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.5))

    ax.text(2.55, 3.6, '下载 + 删除', ha='center', fontsize=7, color='#1565C0')

    # Problems notes
    ax.text(0.2, 0.5, '⚠ 多设备不同步\n⚠ 风险：本地丢失', ha='left', fontsize=7, color='#C62828')

    # ── IMAP (right) ──
    ax.text(9, 6.7, 'IMAP（TCP 143）— "服务器端管理"', ha='center', fontsize=11, fontweight='bold', color='#2E7D32')

    # Mail server
    rect = FancyBboxPatch((7, 4.5), 3.5, 1.8, boxstyle="round,pad=0.1",
                          facecolor='#C8E6C9', edgecolor='#2E7D32', linewidth=2)
    ax.add_patch(rect)
    ax.text(8.75, 5.8, '邮件服务器\n(文件夹/状态)', ha='center', fontsize=9, fontweight='bold')

    # Clients
    for x_pos, label in [(6.4, 'PC'), (8.6, '手机'), (10.8, '笔记本')]:
        rect = FancyBboxPatch((x_pos, 1.5), 1.5, 1.2, boxstyle="round,pad=0.08",
                              facecolor='#E8F5E9', edgecolor='#2E7D32', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x_pos + 0.75, 2.1, label, ha='center', fontsize=8)

    # Bidirectional arrows
    ax.annotate('', xy=(7.75, 2.7), xytext=(8.75, 4.5),
                arrowprops=dict(arrowstyle='<->', color='#2E7D32', lw=1.5))
    ax.annotate('', xy=(10, 2.7), xytext=(8.75, 4.5),
                arrowprops=dict(arrowstyle='<->', color='#2E7D32', lw=1.5))
    ax.annotate('', xy=(12, 2.7), xytext=(8.75, 4.5),
                arrowprops=dict(arrowstyle='<->', color='#2E7D32', lw=1.5))

    ax.text(9.5, 3.6, '同步/部分获取', ha='center', fontsize=7, color='#2E7D32')

    # Benefits notes
    ax.text(6.4, 0.5, '✓ 多设备同步\n✓ 服务器文件夹\n✓ 部分获取', ha='left', fontsize=7, color='#2E7D32')

    # Feature comparison table at bottom
    ax.text(6, 0.1, 'POP3：特许→事务→更新三阶段 | 邮件下载到本地后服务器删除 | IMAP：所有邮件保留在服务器 | 支持文件夹、搜索、部分获取', ha='center', fontsize=7, color='#888')

    save(fig, 'pop3_imap_comparison.png')


# ── STP Topology Diagram ───────────────────────────────────────────────
def draw_stp_topology():
    """4-switch redundant topology showing STP root bridge, port roles, and blocked port."""
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('STP 生成树端口角色', fontsize=14, fontweight='bold', pad=18)

    # Switch positions
    sw_pos = {
        'A': (6, 8.5),
        'B': (10, 5),
        'C': (6, 1.5),
        'D': (2, 5),
    }

    # Draw switches as rounded boxes
    for name, (x, y) in sw_pos.items():
        is_root = (name == 'A')
        fc = '#FFCDD2' if is_root else '#E3F2FD'
        ec = '#C62828' if is_root else '#1565C0'
        lw = 2.5 if is_root else 1.5
        rect = FancyBboxPatch((x - 1.1, y - 0.6), 2.2, 1.2,
                              boxstyle="round,pad=0.15", facecolor=fc,
                              edgecolor=ec, linewidth=lw)
        ax.add_patch(rect)
        label = f'交换机 {name}\n(根桥)' if is_root else f'交换机 {name}'
        ax.text(x, y, label, ha='center', va='center', fontsize=10,
                fontweight='bold' if is_root else 'normal',
                color='#C62828' if is_root else '#333')

    # Bridge ID info
    ax.text(6, 9.5, 'Bridge ID = 32768 + MAC (最小者为根桥)', ha='center', fontsize=9,
            color='#C62828', fontstyle='italic')

    # Links: (from, to, cost)
    links = [
        ('A', 'B', 4),
        ('B', 'C', 4),
        ('C', 'D', 19),
        ('D', 'A', 4),
        ('B', 'D', 19),  # cross link — will be blocked
    ]

    # Draw links
    for src, dst, cost in links:
        x1, y1 = sw_pos[src]
        x2, y2 = sw_pos[dst]
        blocked = (src == 'B' and dst == 'D')

        if blocked:
            color = '#E53935'
            lw = 1.2
            style = 'dashed'
        else:
            color = '#2E7D32'
            lw = 2.0
            style = 'solid'

        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, linestyle=style, zorder=0)

        # Cost label at midpoint
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # Offset perpendicular to link
        dx, dy = y2 - y1, -(x2 - x1)
        d = np.sqrt(dx**2 + dy**2)
        ox, oy = dx / d * 0.5, dy / d * 0.5
        ax.text(mx + ox, my + oy, f'开销 {cost}', fontsize=8, color=color,
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

    # Port role annotations: (switch, angle_deg, distance, text, color)
    annotations = [
        # A ports (all DP — root)
        ('A', 0, 'DP', '#2E7D32'),     # to B
        ('A', 270, 'DP', '#2E7D32'),   # to C
        ('A', 180, 'DP', '#2E7D32'),  # to D

        # B ports
        ('B', 180, 'RP', '#1565C0'),  # to A = Root Port
        ('B', 270, 'DP', '#2E7D32'),  # to C
        ('B', 180 + 45, 'BP', '#E53935'),  # to D = Blocked

        # C ports
        ('C', 90, 'RP', '#1565C0'),   # to A (via B)
        ('C', 180, 'ALT\n(BP)', '#E53935'),  # to D

        # D ports
        ('D', 90, 'RP', '#1565C0'),  # to A
        ('D', 270, 'DP', '#2E7D32'),  # to C
    ]

    # Map each annotation to the right position
    # (from, direction, role, color) with computed positions
    # Directions are approximate compass directions from each switch
    port_angles = {
        ('A', 'B'): 30, ('A', 'D'): 150, ('A', 'C'): -30,
        ('B', 'A'): 150, ('B', 'C'): -30, ('B', 'D'): 90,
        ('C', 'B'): 150, ('C', 'D'): 30,
        ('D', 'A'): -30, ('D', 'C'): 30, ('D', 'B'): -150,
    }
    port_roles = {
        ('A', 'B'): ('DP', '#2E7D32'), ('A', 'D'): ('DP', '#2E7D32'),
        ('A', 'C'): ('DP', '#2E7D32'),  # via B-c link
        ('B', 'A'): ('RP', '#1565C0'), ('B', 'C'): ('DP', '#2E7D32'),
        ('B', 'D'): ('BP', '#E53935'),
        ('C', 'B'): ('RP', '#1565C0'), ('C', 'D'): ('DP', '#2E7D32'),
        ('D', 'A'): ('RP', '#1565C0'), ('D', 'C'): ('DP', '#2E7D32'),
        ('D', 'B'): ('ALT', '#B71C1C'),
    }

    for (src, dst), (role, color) in port_roles.items():
        x1, y1 = sw_pos[src]
        x2, y2 = sw_pos[dst]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        dist = 1.35
        px = x1 + np.cos(np.radians(angle)) * dist
        py = y1 + np.sin(np.radians(angle)) * dist
        ax.text(px, py, role, fontsize=7, fontweight='bold', color=color,
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.12', facecolor='white',
                          edgecolor=color, linewidth=0.8, alpha=0.9))

    # Legend
    legend_items = [
        ('Root Port (RP)', '#1565C0'),
        ('Designated Port (DP)', '#2E7D32'),
        ('Blocked Port (BP)', '#E53935'),
    ]
    for i, (label, c) in enumerate(legend_items):
        ax.text(0.15, 1.1 - i * 0.35, label, fontsize=8, color=c, fontweight='bold',
                transform=ax.transAxes)

    # Note at bottom
    ax.text(6, 0.2, 'A 为根桥（Bridge ID 最小）| B-D 链路阻塞以消除环路 | 箭头指向根桥方向',
            ha='center', fontsize=8, color='#666')

    save(fig, 'stp_topology.png')


# ── RED/AQM Drop Probability Diagram ───────────────────────────────────
def draw_red_aqm():
    """RED three-region drop probability curve."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.05, 1.15)
    ax.set_xlabel('平均队列长度（占缓冲区百分比）', fontsize=11)
    ax.set_ylabel('丢弃/标记概率', fontsize=11)
    ax.set_title('RED（随机早期检测）— 三段式丢弃概率', fontsize=13, fontweight='bold')

    min_th = 30
    max_th = 70
    p_max = 0.1

    # Region 1: no drop
    x1 = np.linspace(0, min_th, 50)
    ax.plot(x1, np.zeros_like(x1), color='#2E7D32', lw=2.5)
    ax.fill_between(x1, 0, np.zeros_like(x1), alpha=0.08, color='#2E7D32')

    # Region 2: probabilistic drop
    x2 = np.linspace(min_th, max_th, 50)
    y2 = p_max * (x2 - min_th) / (max_th - min_th)
    ax.plot(x2, y2, color='#F57C00', lw=2.5)
    ax.fill_between(x2, 0, y2, alpha=0.1, color='#F57C00')

    # Region 3: full drop
    x3 = np.linspace(max_th, 100, 50)
    ax.plot(x3, np.ones_like(x3), color='#E53935', lw=2.5)
    ax.fill_between(x3, 0, 1, alpha=0.1, color='#E53935')

    # Threshold lines
    ax.axvline(x=min_th, color='#F57C00', linestyle='--', lw=1, alpha=0.6)
    ax.axvline(x=max_th, color='#E53935', linestyle='--', lw=1, alpha=0.6)
    ax.axhline(y=p_max, color='#888', linestyle=':', lw=0.8, alpha=0.5)

    # Annotations
    ax.text(min_th / 2, 0.5, '不标记/\n不丢弃', ha='center', fontsize=10, color='#2E7D32', fontweight='bold')
    ax.text((min_th + max_th) / 2, 0.65, f'概率标记/丢弃\n(p 线性增长 → {p_max})', ha='center', fontsize=9, color='#F57C00', fontweight='bold')
    ax.text(max_th + 15, 0.5, '全部标记/\n丢弃', ha='center', fontsize=10, color='#E53935', fontweight='bold')

    ax.annotate('min_th', xy=(min_th, 0), xytext=(min_th - 5, -0.13), fontsize=9, color='#F57C00',
                ha='center', arrowprops=dict(arrowstyle='->', color='#F57C00', lw=0.8))
    ax.annotate('max_th', xy=(max_th, 0), xytext=(max_th + 8, -0.13), fontsize=9, color='#E53935',
                ha='center', arrowprops=dict(arrowstyle='->', color='#E53935', lw=0.8))
    ax.annotate(f'pmax = {p_max}', xy=(75, 0.1), xytext=(75, 0.2), fontsize=8, color='#888',
                ha='center', arrowprops=dict(arrowstyle='->', color='#888', lw=0.6))

    ax.text(50, -0.24, 'EWMA 平均队列长度 → 避免瞬时波动触发误判', ha='center', fontsize=9, color='#555', fontstyle='italic')

    save(fig, 'red_aqm.png')


# ── OFDM vs OFDMA Diagram ─────────────────────────────────────────────
def draw_ofdm_ofdma():
    """OFDM (single-user) vs OFDMA (multi-user) time-frequency grid comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for ax, title, sublabel in [
        (ax1, 'OFDM（单用户）', '所有子载波在同一时刻服务于同一用户'),
        (ax2, 'OFDMA（多用户）', '子载波组（RU）在同一时刻分配给不同用户'),
    ]:
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.set_xlabel('时间（OFDM 符号）', fontsize=10)
        ax.set_ylabel('子载波', fontsize=10)
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 12)
        ax.set_yticks([])
        ax.set_xticks(range(8))
        ax.text(4, -0.8, sublabel, ha='center', fontsize=9, color='#555', fontstyle='italic')

    # OFDM: single user fills all subcarriers for all symbols
    colors_user = ['#BBDEFB']
    for t in range(8):
        for sc in range(12):
            rect = FancyBboxPatch((t, sc), 0.9, 0.9, boxstyle="round,pad=0.04",
                                  facecolor='#BBDEFB', edgecolor='#90CAF9', linewidth=0.4)
            ax1.add_patch(rect)
    ax1.text(4, 6, '用户 1', ha='center', va='center', fontsize=11, fontweight='bold', color='#1565C0')

    # OFDMA: different users get different RU blocks
    user_blocks = [
        (0, 0, 2, 8, '#BBDEFB', '用户 1'),
        (2, 0, 2, 4, '#FFCDD2', '用户 2'),
        (2, 4, 2, 4, '#C8E6C9', '用户 3'),
        (4, 0, 2, 6, '#FFF9C4', '用户 4'),
        (4, 6, 2, 3, '#E1BEE7', '用户 5'),
        (6, 0, 2, 5, '#FFE0B2', '用户 6'),
    ]
    for tx, sc0, tw, sh, color, label in user_blocks:
        for t in range(tx, tx + tw):
            for sc in range(sc0, sc0 + sh):
                rect = FancyBboxPatch((t, sc), 0.9, 0.9, boxstyle="round,pad=0.04",
                                      facecolor=color, edgecolor='#999', linewidth=0.3)
                ax2.add_patch(rect)
        cx = tx + tw / 2
        cy = sc0 + sh / 2
        fs = 8 if sh >= 4 else 7
        ax2.text(cx, cy, label, ha='center', va='center', fontsize=fs, fontweight='bold')

    # Arrow between
    fig.text(0.505, 0.5, '→', ha='center', va='center', fontsize=24, color='#F57C00', fontweight='bold')

    save(fig, 'ofdm_ofdma.png')


# ── MIMO Gains Diagram ─────────────────────────────────────────────────
def draw_mimo_gains():
    """Three MIMO gains: spatial multiplexing, diversity, beamforming."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.5))
    fig.suptitle('MIMO 的三种增益', fontsize=14, fontweight='bold', y=0.98)

    # 1. Spatial Multiplexing
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 8)
    ax1.axis('off')
    ax1.set_title('空间复用', fontsize=12, fontweight='bold', color='#1565C0')

    tx = FancyBboxPatch((0.5, 3), 2.5, 2, boxstyle="round,pad=0.12",
                         facecolor='#BBDEFB', edgecolor='#1565C0', lw=1.5)
    ax1.add_patch(tx)
    ax1.text(1.75, 4, '发送端\n(4天线)', ha='center', va='center', fontsize=9, fontweight='bold')
    rx = FancyBboxPatch((7, 3), 2.5, 2, boxstyle="round,pad=0.12",
                         facecolor='#C8E6C9', edgecolor='#2E7D32', lw=1.5)
    ax1.add_patch(rx)
    ax1.text(8.25, 4, '接收端\n(4天线)', ha='center', va='center', fontsize=9, fontweight='bold')

    for i, c in enumerate(['#E53935', '#F57C00', '#1565C0', '#2E7D32']):
        ax1.annotate('', xy=(7, 6.5 - i * 0.8), xytext=(3, 6.5 - i * 0.8),
                     arrowprops=dict(arrowstyle='->', color=c, lw=1.5))
        ax1.text(5, 6.55 - i * 0.8, f'流 {i+1}', fontsize=8, ha='center', color=c, fontweight='bold')
    ax1.text(5, 1.2, '不同数据流 × 不同空间路径', ha='center', fontsize=9, color='#555')

    # 2. Diversity
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 8)
    ax2.axis('off')
    ax2.set_title('分集', fontsize=12, fontweight='bold', color='#E65100')

    tx2 = FancyBboxPatch((0.5, 3), 2.5, 2, boxstyle="round,pad=0.12",
                          facecolor='#FFE0B2', edgecolor='#E65100', lw=1.5)
    ax2.add_patch(tx2)
    ax2.text(1.75, 4, '发送端\n(2天线)', ha='center', va='center', fontsize=9, fontweight='bold')
    rx2 = FancyBboxPatch((7, 3), 2.5, 2, boxstyle="round,pad=0.12",
                          facecolor='#C8E6C9', edgecolor='#2E7D32', lw=1.5)
    ax2.add_patch(rx2)
    ax2.text(8.25, 4, '接收端\n(2天线)', ha='center', va='center', fontsize=9, fontweight='bold')

    # Two paths carrying same data
    ax2.annotate('', xy=(7, 5.5), xytext=(3, 5.5),
                 arrowprops=dict(arrowstyle='->', color='#E65100', lw=1.5))
    ax2.annotate('', xy=(7, 3.0), xytext=(3, 3.0),
                 arrowprops=dict(arrowstyle='->', color='#E65100', lw=1.5, linestyle='dashed'))
    ax2.text(5, 5.8, '路径 A', fontsize=8, ha='center', color='#E65100', fontweight='bold')
    ax2.text(5, 2.7, '路径 B（备用）', fontsize=8, ha='center', color='#E65100', fontweight='bold')
    ax2.text(5, 1.2, '同数据 × 多路径 = 可靠性', ha='center', fontsize=9, color='#555')

    # 3. Beamforming
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 8)
    ax3.axis('off')
    ax3.set_title('波束成形', fontsize=12, fontweight='bold', color='#6A1B9A')

    tx3 = FancyBboxPatch((0.5, 3), 2.5, 2, boxstyle="round,pad=0.12",
                          facecolor='#E1BEE7', edgecolor='#6A1B9A', lw=1.5)
    ax3.add_patch(tx3)
    ax3.text(1.75, 4, '基站\n(多天线阵列)', ha='center', va='center', fontsize=9, fontweight='bold')

    # Draw beam cone — narrow beam pointing at target user
    for k in range(12):
        offset = (k - 5.5) * 0.05
        r = 6.2
        ax3.plot([3, 3 + r], [4.0 + offset, 3.8 + offset],
                 color='#6A1B9A', alpha=0.08, lw=2.5)

    # Target user at beam focus
    ax3.fill_between([7.5, 9.8], 2.8, 4.6, alpha=0.15, color='#6A1B9A')
    ux = FancyBboxPatch((8.2, 3.4), 1.3, 0.8, boxstyle="round,pad=0.08",
                         facecolor='#C8E6C9', edgecolor='#2E7D32', lw=1.2)
    ax3.add_patch(ux)
    ax3.text(8.85, 3.8, '目标\n用户', ha='center', va='center', fontsize=8, fontweight='bold')

    # Interferer — away from beam
    ax3.text(9.5, 6.2, '其他用户\n(零陷抑制)', ha='center', fontsize=8, color='#999')
    ax3.annotate('', xy=(9.2, 6.5), xytext=(3.5, 5.5),
                 arrowprops=dict(arrowstyle='->', color='#CCC', lw=0.8, linestyle='dotted'))

    ax3.text(5, 1.2, '相位调整 = 定向增强 + 零陷抑制', ha='center', fontsize=9, color='#555')

    save(fig, 'mimo_gains.png')


# ── Jitter Buffer Diagram ──────────────────────────────────────────────
def draw_jitter_buffer():
    """Jitter buffer — arrival vs playout timeline."""
    fig, ax = plt.subplots(figsize=(13, 5.5))
    ax.set_xlim(0, 16)
    ax.set_ylim(-0.5, 5)
    ax.set_xlabel('时间', fontsize=11)
    ax.set_title('去抖动缓冲区 — 到达 vs 播放时间线', fontsize=13, fontweight='bold')

    # Timeline
    ax.plot([0, 16], [0, 0], 'k-', lw=0.8)
    for i in range(17):
        ax.plot([i, i], [-0.1, 0.1], 'k-', lw=0.5)

    # Generation instants (fixed interval)
    gen_times = np.arange(1, 14, 2)
    for i, gt in enumerate(gen_times):
        ax.plot(gt, 0.3, 'o', color='#1565C0', markersize=6, zorder=5)
        ax.text(gt, 0.1, f'生成\n第{i+1}块', ha='center', fontsize=7, color='#1565C0')

    # Arrival instants (irregular — jittered)
    arrivals = [2.2, 4.8, 6.3, 8.0, 10.9, 12.2, 14.1]
    for i, at in enumerate(arrivals):
        ax.plot(at, 2.5, 's', color='#F57C00', markersize=7, zorder=5)
        jitter = at - gen_times[i] - 1.0  # excess delay beyond 1 unit
        ax.annotate('', xy=(at, 2.5), xytext=(gen_times[i], 0.5),
                    arrowprops=dict(arrowstyle='->', color='#F57C00', lw=0.8, alpha=0.6,
                                    connectionstyle='arc3,rad=0.2'))
        ax.text(at - 0.1, 2.15, f'+{jitter:.1f}', fontsize=7, color='#F57C00', ha='right')

    # Playout instants (fixed interval after fixed playout delay q)
    q = 2.2
    for i, gt in enumerate(gen_times):
        pt = gt + q
        ax.plot(pt, 4.2, 'D', color='#2E7D32', markersize=7, zorder=5)
        # Show block going from arrival to playout
        if arrivals[i] < pt:
            color = '#2E7D32'
            linestyle = '-'
        else:
            color = '#E53935'
            linestyle = '--'
            ax.plot([arrivals[i], pt], [2.5, 4.2], linestyle, color=color, lw=0.8, alpha=0.5)

    # Early/late annotations
    ax.text(11, 2.8, '块4迟到!\n(到达>播放时刻)\n→丢弃', fontsize=8, color='#E53935', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='#E53935', alpha=0.8))

    # Playout delay indicator
    ax.annotate('', xy=(1, 4.2), xytext=(1, 0.5),
                arrowprops=dict(arrowstyle='<->', color='#2E7D32', lw=1.5))
    ax.text(1.4, 2.5, f'播放延迟\nq = {q}', fontsize=9, color='#2E7D32', fontweight='bold',
            va='center')

    # Buffer fill label
    ax.fill_between([4, 7.5], 3.0, 3.8, alpha=0.12, color='#1565C0')
    ax.text(5.75, 3.4, '去抖动缓冲区\n(序号排序 + 时间戳定播)', ha='center', fontsize=9,
            color='#1565C0', fontweight='bold')

    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    save(fig, 'jitter_buffer.png')


# ── MIME Structure Diagram ─────────────────────────────────────────────
def draw_mime_structure():
    """MIME email message structure with multipart."""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('MIME 邮件报文结构（multipart/mixed）', fontsize=13, fontweight='bold', pad=15)

    y = 9.2
    # Standard headers
    headers = [('From:', '#E3F2FD'), ('To:', '#E3F2FD'), ('Subject:', '#E3F2FD')]
    for label, color in headers:
        rect = FancyBboxPatch((0.3, y - 0.35), 9.4, 0.7, boxstyle="round,pad=0.06",
                               facecolor=color, edgecolor='#90CAF9', lw=0.8)
        ax.add_patch(rect)
        ax.text(0.6, y, label, fontsize=9, va='center', fontfamily='monospace', fontweight='bold')
        y -= 0.85

    # MIME headers
    mime_h = [('MIME-Version: 1.0', '#FFF9C4'), ('Content-Type: multipart/mixed; boundary="BOUNDARY"', '#FFF9C4')]
    for label, color in mime_h:
        rect = FancyBboxPatch((0.3, y - 0.35), 9.4, 0.7, boxstyle="round,pad=0.06",
                               facecolor=color, edgecolor='#F9A825', lw=0.8)
        ax.add_patch(rect)
        ax.text(0.6, y, label, fontsize=8.5, va='center', fontfamily='monospace')
        y -= 0.85

    # Blank line
    ax.plot([0.3, 9.7], [y, y], 'k--', lw=0.5, alpha=0.3)

    # Part 1
    y -= 0.6
    ax.text(0.5, y, '--BOUNDARY', fontsize=7.5, fontfamily='monospace', color='#888')
    y -= 0.4
    rect1 = FancyBboxPatch((0.7, y - 1.0), 8.6, 1.2, boxstyle="round,pad=0.08",
                            facecolor='#E8F5E9', edgecolor='#66BB6A', lw=0.8)
    ax.add_patch(rect1)
    ax.text(0.9, y - 0.15, 'Content-Type: text/plain\n\nHello, this is the email body...',
            fontsize=8, fontfamily='monospace', va='top')
    ax.text(5.0, y - 0.85, '第一部分：纯文本正文', ha='center', fontsize=8, color='#2E7D32', fontweight='bold')

    # Part 2
    y -= 1.8
    ax.text(0.5, y, '--BOUNDARY', fontsize=7.5, fontfamily='monospace', color='#888')
    y -= 0.4
    rect2 = FancyBboxPatch((0.7, y - 1.0), 8.6, 1.2, boxstyle="round,pad=0.08",
                            facecolor='#E3F2FD', edgecolor='#42A5F5', lw=0.8)
    ax.add_patch(rect2)
    ax.text(0.9, y - 0.15, 'Content-Type: image/jpeg\nContent-Transfer-Encoding: base64\n\n/9j/4AAQSkZJRg...',
            fontsize=8, fontfamily='monospace', va='top')
    ax.text(5.0, y - 0.85, '第二部分：JPEG 图像附件（Base64 编码）', ha='center', fontsize=8, color='#1565C0', fontweight='bold')

    # Closing boundary
    y -= 1.8
    ax.text(0.5, y, '--BOUNDARY--', fontsize=7.5, fontfamily='monospace', color='#888')

    # Annotation: boundary separators
    ax.annotate('边界分隔符\n(boundary)', xy=(0.4, 5.5), xytext=(0.4, 3.5),
                fontsize=8, color='#888', ha='center',
                arrowprops=dict(arrowstyle='->', color='#CCC', lw=0.8, connectionstyle='arc3,rad=-0.3'))

    # Legend
    ax.text(0.3, 0.3, 'MIME 核心字段: MIME-Version | Content-Type | Content-Transfer-Encoding',
            fontsize=9, color='#555')

    save(fig, 'mime_structure.png')


# ── Subnet Concept Diagram ─────────────────────────────────────────────
def draw_subnet_concept():
    """Draw a network topology showing routers as subnet boundaries.

    Left: original topology with routers and colored subnet regions.
    Right: routers removed, showing each subnet as an isolated island.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

    for ax in [ax1, ax2]:
        ax.set_xlim(0, 18)
        ax.set_ylim(0, 8)
        ax.axis('off')

    ax1.set_title('原始网络拓扑', fontsize=13, fontweight='bold', pad=12)
    ax2.set_title('删除路由器后 → 三个孤岛 = 三个子网', fontsize=13, fontweight='bold', pad=12)

    # ── Helper functions ──
    def draw_host(ax, x, y, label, color='#BBDEFB'):
        """Draw a host as a small monitor-like rectangle."""
        rect = FancyBboxPatch((x - 0.45, y - 0.3), 0.9, 0.6,
                               boxstyle="round,pad=0.05", facecolor=color,
                               edgecolor='#333', linewidth=1)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=7.5, fontweight='bold')

    def draw_switch(ax, x, y, label='SW'):
        """Draw a switch as a rectangle."""
        rect = FancyBboxPatch((x - 0.35, y - 0.25), 0.7, 0.5,
                               boxstyle="round,pad=0.05", facecolor='#E0E0E0',
                               edgecolor='#333', linewidth=1)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=7, fontweight='bold')

    def draw_router(ax, x, y, label, active=True):
        """Draw a router as a taller rectangle."""
        face = '#FFCC80' if active else '#E0E0E0'
        edge = '#333' if active else '#AAA'
        alpha = 1.0 if active else 0.5
        rect = FancyBboxPatch((x - 0.5, y - 0.4), 1.0, 0.8,
                               boxstyle="round,pad=0.08", facecolor=face,
                               edgecolor=edge, linewidth=1.5, alpha=alpha)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color=('#333' if active else '#999'))

    def draw_link(ax, x1, y1, x2, y2, active=True):
        """Draw a horizontal link between two points."""
        color = '#555' if active else '#CCC'
        lw = 1.5 if active else 1.0
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, zorder=1)

    def draw_subnet_bg(ax, x1, x2, y1, y2, color, alpha=0.15):
        """Draw a colored region for a subnet."""
        rect = FancyBboxPatch((x1, y1), x2 - x1, y2 - y1,
                               boxstyle="round,pad=0.3", facecolor=color,
                               edgecolor=color, linewidth=1.5, linestyle='--',
                               alpha=alpha, zorder=0)
        ax.add_patch(rect)

    # ── Coordinates ──
    # Subnet regions
    s1_x1, s1_x2 = 0.5, 6.2
    s2_x1, s2_x2 = 6.2, 11.8
    s3_x1, s3_x2 = 11.8, 17.5

    host_y = 5.5
    sw_y = 3.5
    router_y = 3.5

    # ── Left panel: Original topology ──
    for ax, routers_active in [(ax1, True), (ax2, False)]:
        # Subnet backgrounds
        draw_subnet_bg(ax, s1_x1, s1_x2, 1.0, 7.0, '#1565C0')
        draw_subnet_bg(ax, s2_x1, s2_x2, 1.5, 5.5, '#EF6C00')
        draw_subnet_bg(ax, s3_x1, s3_x2, 1.0, 7.0, '#2E7D32')

        # Subnet labels at top
        if ax == ax1:
            ax.text(3.35, 6.7, '子网 1\n223.1.1.0/24', ha='center', fontsize=8,
                    fontweight='bold', color='#1565C0')
            ax.text(9.0, 5.2, '子网 2 (点对点)\n223.1.2.0/30', ha='center', fontsize=8,
                    fontweight='bold', color='#EF6C00')
            ax.text(14.65, 6.7, '子网 3\n223.1.3.0/24', ha='center', fontsize=8,
                    fontweight='bold', color='#2E7D32')
        else:
            ax.text(3.35, 6.7, '子网 1\n(孤岛)', ha='center', fontsize=8,
                    fontweight='bold', color='#1565C0')
            ax.text(9.0, 5.2, '子网 2\n(孤岛)', ha='center', fontsize=8,
                    fontweight='bold', color='#EF6C00')
            ax.text(14.65, 6.7, '子网 3\n(孤岛)', ha='center', fontsize=8,
                    fontweight='bold', color='#2E7D32')

        # Hosts in subnet 1
        draw_host(ax, 1.6, host_y, 'A')
        draw_host(ax, 2.8, host_y, 'B')
        draw_host(ax, 4.0, host_y, 'C')
        # Switch in subnet 1
        draw_switch(ax, 2.8, sw_y)
        # Bus topology: hosts → horizontal bus → switch
        bus_y = 4.3
        for hx in [1.6, 2.8, 4.0]:
            draw_link(ax, hx, host_y - 0.3, hx, bus_y, routers_active)
        draw_link(ax, 1.6, bus_y, 4.0, bus_y, routers_active)  # horizontal bus
        draw_link(ax, 2.8, bus_y, 2.8, sw_y + 0.25, routers_active)  # bus → switch

        # Router R1 (at subnet 1-2 boundary)
        draw_router(ax, 5.0, router_y, 'R1', routers_active)
        # Connect switch to R1
        draw_link(ax, 2.8 + 0.35, sw_y, 5.0 - 0.5, router_y, routers_active)

        # Router R2 (at subnet 2-3 boundary)
        draw_router(ax, 13.0, router_y, 'R2', routers_active)

        # Link between R1 and R2 (subnet 2)
        draw_link(ax, 5.0 + 0.5, router_y, 13.0 - 0.5, router_y, routers_active)

        # Interface dots on the link (make subnet 2 visible)
        for iface_x, iface_label in [(6.3, 'if0'), (11.7, 'if1')]:
            dot_color = '#EF6C00' if routers_active else '#CCC'
            ax.plot(iface_x, router_y, 'o', color=dot_color, markersize=6, zorder=3)
            if routers_active:
                ax.text(iface_x, router_y - 0.5, iface_label, ha='center', fontsize=6.5, color='#EF6C00')

        # Subnet 2 annotation on right panel
        if not routers_active:
            ax.text(9.0, 4.6, '（点对点链路\n  也是子网）', ha='center', fontsize=7.5,
                    color='#EF6C00', style='italic')

        # Switch in subnet 3
        draw_switch(ax, 15.2, sw_y)
        # Connect R2 to switch
        draw_link(ax, 13.0 + 0.5, router_y, 15.2 - 0.35, sw_y, routers_active)

        # Hosts in subnet 3
        draw_host(ax, 14.1, host_y, 'D')
        draw_host(ax, 16.3, host_y, 'E')
        # Bus topology: hosts → horizontal bus → switch
        for hx in [14.1, 16.3]:
            draw_link(ax, hx, host_y - 0.3, hx, bus_y, routers_active)
        draw_link(ax, 14.1, bus_y, 16.3, bus_y, routers_active)  # horizontal bus
        draw_link(ax, 15.2, bus_y, 15.2, sw_y + 0.25, routers_active)  # bus → switch

    # ── Annotation on right panel ──
    ax2.annotate('✕ 路由器被删除\n子网之间\n不再连通', xy=(9.0, 2.0),
                fontsize=9, ha='center', color='#D32F2F', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFEBEE', edgecolor='#D32F2F', alpha=0.9))

    # ── Bottom explanation ──
    fig.text(0.5, 0.02,
             '路由器连接不同的子网。删除所有路由器后，网络断开为互不相连的孤岛——每个孤岛就是一个子网。\n'
             '同一子网内的接口可直接通信（不经路由器）；跨越子网的通信必须经过路由器转发。',
             ha='center', fontsize=9.5, color='#555')

    save(fig, 'subnet_concept.png')


if __name__ == '__main__':
    print("Generating diagrams...")
    draw_ipv4_header()
    draw_tcp_handshake()
    draw_tcp_wave()
    draw_router_arch()
    draw_dhcp()
    draw_http_connections()
    draw_ip_fragmentation()
    draw_dijkstra()
    draw_ospf_areas()
    draw_bgp()
    draw_dns()
    draw_domain_hierarchy()
    draw_dns_delegation()
    draw_dns_query_types()
    draw_scheduling()
    draw_tcp_congestion_control()
    draw_tcp_header()
    draw_tcp_checksum_coverage()
    draw_udp_header()
    draw_udp_checksum_coverage()
    draw_ipv6_header()
    draw_encapsulation()
    draw_circuit_vs_packet()
    draw_nat_process()
    draw_gbn_vs_sr()
    draw_isp_hierarchy()
    draw_dv_routing()
    draw_sdn_architecture()
    draw_smtp_process()
    draw_ethernet_frame()
    draw_link_layer_hops()
    draw_vlan_isolation()
    draw_csma_cd()
    draw_store_forward_pipeline()
    draw_rdt_fsm()
    draw_switch_self_learning()
    draw_nodal_delay()
    draw_p2p_scaling()
    draw_dash_adaptation()
    draw_hidden_terminal()
    draw_csma_ca_rts_cts()
    draw_lte_architecture()
    draw_mobile_ip()
    draw_wifi_frame()
    draw_wifi_bss()
    draw_cidr_subnet()
    draw_subnet_concept()
    draw_web_request_panorama()
    draw_tdm_fdm_cdma()
    draw_fat_tree()
    draw_openflow()
    draw_mpls_operations()
    draw_crc_division()
    draw_rsa_overview()
    draw_digital_signature()
    draw_ap4_auth()
    draw_ipsec_tunnel()
    draw_wpa2_handshake()
    draw_rtp_header()
    draw_sip_call_flow()
    draw_leaky_vs_token_bucket()
    draw_diffserv()
    draw_tls_handshake()
    draw_arp_process()
    draw_http_message_format()
    draw_pgp_flow()
    draw_pop3_imap()
    draw_stp_topology()
    draw_red_aqm()
    draw_ofdm_ofdma()
    draw_mimo_gains()
    draw_jitter_buffer()
    draw_mime_structure()
    print(f"Done. All diagrams saved to {OUTPUT}")
