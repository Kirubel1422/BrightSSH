import sys
import os 
import paramiko
import socket
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOST_KEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == 'bright' and password == 'bright'):
            return paramiko.AUTH_SUCCESSFUL
    

if __name__ == '__main__':
    server_ip = '0.0.0.0'
    server_port = 123

    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc.bind((server_ip, server_port))
        soc.listen(100)
        print('[+] Listening on PORT %d' %server_port)

        client, addr = soc.accept()
    except Exception as E:
        print('[-] Listening failed')
        print(str(E))
        sys.exit(1)
    else:
        print(f'[+] Got connection from {addr[0]}:{addr[1]}')
    
    bh_session = paramiko.Transport(client)
    bh_session.add_server_key(HOST_KEY)
    server = Server()
    bh_session.start_server(server=server)

    chan = bh_session.accept(20)
    if chan is None:
        print('*** No Channel ***')
        sys.exit(1)
    
    print('[+] Authenticated')
    print(chan.recv(4096))

    chan.send('Welcome to bh session')
    try:
        while True:
            command = input('> ')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(4096)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting ...')
                bh_session.close()
                break
    except KeyboardInterrupt as e:
        print('exiting ...')
        bh_session.close()




