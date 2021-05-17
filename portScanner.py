import socket
from IPy import IP
import concurrent
import concurrent.futures as cf
import termcolor

def scan_targets(target, ports):                   #scan when multiple targets are given and also in case of one ip
    if ',' in target:
        for ip_addr in target.split(','):
            scan(ip_addr.strip(' '), ports)
    else:
        scan(target, ports)

def scan(target, ports):                           #scan when only one ip is given
    converted_IP = check_IP(target)
    print('\n' + termcolor.colored(('[+] Scanning target --> ' + str(target)), 'yellow'))
    
    #this code is to make the scannng fast.
    executor = cf.ProcessPoolExecutor(10)
    futures = [executor.submit(scan_port, converted_IP, port) for port in range(1, (ports+1))]
    concurrent.futures.wait(futures)

def get_banner(s):
    return s.recv(1024)                     #this functions recieves the 1024 bytes information of the port

def check_IP(ip):
    try:
        IP(ip)
        return ip
    except ValueError:
        ip = socket.gethostbyname(ip)
        return ip

def scan_port(ipaddress,port):
    try:
        sock = socket.socket()              #this is socket descriptor(sock).
        sock.settimeout(0.5)                #this sets a time out interval for any one port
        sock.connect((ipaddress, port))
        try:
            banner = get_banner(sock)
            print(termcolor.colored('[+] Open Port ', 'green') + str(port) + ' : ' + str(banner.decode().strip('\n')))
        except:
            print(termcolor.colored('[+] Open Port ', 'green') + str(port))
    except: 
        pass

if __name__ == "__main__":                  #this will make sure that if this programm is ran as a main program then only this part get executed and not when this program is imported in some other programm.
    targets = input(termcolor.colored('[+] Enter the Target/s to scan (split multiple targtes with ,): ', 'blue'))
    ports = int(input(termcolor.colored('[+] Enter the no. of ports you want to scan (e.g. 200 for first 200 ports.): ', 'blue')))
    scan_targets(targets, ports)
