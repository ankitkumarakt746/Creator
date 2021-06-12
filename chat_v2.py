import os
import socket
import threading

localIP = ''
localPort = 5555
targetIP = ''
targetPort = localPort

class rec():
    rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def __init__(self):
        self._running=True
        self.rs.bind((localIP, localPort))
        
    def stop(self):
        self._running = False
        
    def run(self):
        while self._running:
            x = self.rs.recvfrom(1024)
            if x[0].decode() == 'tmnat':
                self.rs.close()
                break
            os.system('tput setaf 2' if os.name == 'posix' else 'color A')
            print('\n' + x[1][0] + ': ' + x[0].decode())
            print('Reply- ')


def clearSrc():
    os.system('clear' if os.name == 'posix' else 'cls')

def color(value):
    windowsToLinux = {"0": "0", "1": "4", "2": "2", "3": "6", "4": "1", "5": "5", "6": "3", "7": "7", 
                "8": "0", "9": "4", "A": "2", "B": "6", "C": "1", "D": "5", "E": "3", "F": "7"}
    if os.name == "posix":
        os.system('tput setaf ' + windowsToLinux[value])
    else:
        os.system('color ' + value)


def initiate():
    os.system('firewall-cmd --add-port=' + str(localPort) + '/udp > /dev/null 2>&1; clear' if os.name == 'posix' else 'cls')


def get_localIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))       #IP and Port no. to connect - google server
    #print(s.getsockname())          #Ephemeral Port will be assigned by OS randomly
    ip = s.getsockname()[0]
    s.close()
    return ip


while True:
    localIP = get_localIP()
    recObj = rec()
    t = threading.Thread(target = recObj.run)
    t.start()
    
    initiate()
    color('C')
    print("********************************************")
    print("*                                          *")
    print("*         Welcome To Phoenix Chat          *")
    print("*                                          *")
    print("********************************************")
    color('A')
    print('\nYour ip: ', localIP)
    color('B')
    targetIP = input('Enter target IP: ')
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('\nPress 0 to exit.\n')
    while True:
        color('E')
        msg = input('\nYou: ')
        if msg == '0' or msg == 'q':
            os.system('firewall-cmd --remove-port=' + str(localPort) + '/udp > /dev/null 2>&1') if os.name == 'posix' else None
            recObj.stop()
            ss.sendto('tmnat'.encode(), (localIP, localPort))
            ss.close()
            color('F')
            clearSrc()
            break
        else:
            ss.sendto(msg.encode(), (targetIP, targetPort))
    break
clearSrc()