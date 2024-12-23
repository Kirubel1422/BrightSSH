import paramiko

def ssh_command(ip, port, username, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip,port=port,username=username,password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('----OUTPUT----')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    import getpass
    ip = input('Enter IP address: ')
    port = int(input('Enter PORT: '))
    username = input('Enter Username: ')
    password = getpass.getpass("Enter password: ")

    ssh_command(ip=ip, port=port, username=username, passwd=password, cmd="id")
