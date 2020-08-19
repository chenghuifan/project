from socket import *

from multiprocessing import *

addr = ("0.0.0.0", 8888)


# def send_msg(chatroom_se, client_addr):
#     if client_addr:
#         while True:
#             data = input('>>')
#             for user in client_addr:
#                 chatroom_se.sendto(data.encode(), user)


def main():
    chatroom_se = socket(AF_INET, SOCK_DGRAM)
    chatroom_se.bind(addr)
    client_addr = {}
    while True:
        msg, client_add = chatroom_se.recvfrom(1024)
        if not msg:
            print((client_addr[client_add] + "退出聊天室".encode() + msg).decode())
            exiter = client_addr[client_add]
            chatroom_se.sendto("您已退出聊天室".encode(), client_add)
            del client_addr[client_add]
            for user in client_addr:
                chatroom_se.sendto(exiter + "退出聊天室".encode() + msg, user)
        else:
            if client_add not in client_addr:
                client_addr[client_add] = msg
                for user in client_addr:
                    chatroom_se.sendto(msg + "进入".encode(), user)
            else:
                print("收到" + client_addr[client_add].decode() + msg.decode())
                for user in client_addr:
                    chatroom_se.sendto(client_addr[client_add] + ":".encode() + msg, user)
        # p = Pool()
        # p.apply_async(func=send_msg, args=(chatroom_se, client_addr))
        # p.close()
        # p.join()


if __name__ == '__main__':
    main()
