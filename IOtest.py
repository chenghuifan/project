"""
    select 方法示例
"""
from select import select
from socket import *


f = open("test.log")
# rs, ws, xs = select()
sockfd = socket()
sockfd.bind(("0.0.0.0", 8888))
sockfd.listen(5)
sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(("0.0.0.0", 9999))
print("开始监听IO")
rs, ws, xs = select([f], [], [], 3)
print("rlist:", rs)
print("wlist:", ws)
print("xlist:", xs)

