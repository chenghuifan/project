# from select import *
# from socket import *


# # 准备点IO
# # f = open('test.log')

# sockfd = socket()
# sockfd.bind(('0.0.0.0',8888))
# sockfd.listen(5)

# # sock = socket(AF_INET,SOCK_DGRAM)
# # sock.bind(('0.0.0.0',9999))

# sockfd.setblocking(False)



# # 生成poll
# p = poll()

# # 查找字典 与 register的IO对象时刻一直
# map = {sockfd.fileno():sockfd}
# p.register(sockfd,POLLOUT|POLLERR) # 关注

# while True:
#     events = p.poll()
#     for fd, event in events:
#         if fd == sockfd.fileno():
#             connfd, addr = map[sockfd.fileno()]
#             print("Connect from :", addr)
#             connfd.setblocking(False)
#             p.register(connfd, POLLIN) # 增加监听对象
#             map[connfd.fileno()] = connfd
#         elif event == POLLIN:
#             # 某个客户端发消息给我
#             data = map[fd].recv(1024).decode()
#             if not data:
#                 #  客户端退出
#                 p.unregister(fd)  # 移除监控
#                 map[fd].close()
#                 del map[fd]
#                 continue
#             print("收到:", data)
#             map[fd].send(b'ok')

"""
基于 POLL方法的 IO多路复用网络并发

"""
from socket import *
from select import *

# 创建好监听套接字
sockfd = socket()
sockfd.bind(('0.0.0.0', 8888))
sockfd.listen(5)

# 与非阻塞IO配合防止传输过程阻塞
sockfd.setblocking(False)

# 创建poll对象
p = poll()
# 准备IO进行监控 map字典用于查找IO对象,必须与register一致
map = {sockfd.fileno(): sockfd}
p.register(sockfd, POLLIN)

# 循环监控IO发生
while True:
    # 开始监控IO events-->[(fileno,event),(),]
    events = p.poll()
    # 伴随监控的IO的增多,就绪的IO情况也会复杂
    # 分类讨论 分两类  sockfd -- connfd
    for fd, event in events:
        # 有客户端连接
        if fd == sockfd.fileno():
            connfd, addr = map[fd].accept()
            print("Connect from", addr)
            connfd.setblocking(False)
            p.register(connfd, POLLIN)  # 增加监控
            map[connfd.fileno()] = connfd  # 维护字典
        elif event == POLLIN:
            # 某个客户端发消息给我
            data = map[fd].recv(1024).decode()
            if not data:
                #  客户端退出
                p.unregister(fd)  # 移除监控
                map[fd].close()
                del map[fd]
                continue
            print("收到:", data)
            map[fd].send(b'ok')


