#!/usr/bin/python3 

import os
import socket
import threading

localIP = ''
localPort = 7555
targetIP = ''
targetPort = 7555


class Reciever:
    rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #AF_INET: Address Family, SOCK_DGRAM: UDP

    def __init__(self):
        self.rs.bind((localIP, localPort))

    def listen(self):
        while True:
            x = self.rs.recvfrom(1024)       #1024: Buffer Size
            if x[0].decode() == 'kill #7!':
                self.rs.close()
                break
            color('A')
            print("\n" + x[1][0] + ': ' + x[0].decode())
            color('E')
            print("Reply- ")


def clearSrc():
    os.system('clear' if os.name == 'posix' else 'cls')

def color(value):
    windowsToLinux = {"0": "0", "1": "4", "2": "2", "3": "6", "4": "1", "5": "5", "6": "3", "7": "7",
                "8": "0", "9": "4", "A": "2", "B": "6", "C": "1", "D": "5", "E": "3", "F": "7"}
    if os.name == "posix":
        os.system('tput setaf ' + windowsToLinux[value])
    else:
        os.system('color ' + value)


def initiate(status):
    if status:
        os.system('sudo firewall-cmd --add-port=' + str(localPort) + '/udp > /dev/null 2>&1; clear' if os.name == 'posix' else 'cls')
    else:
        os.system('firewall-cmd --remove-port=' + str(localPort) + '/udp > /dev/null 2>&1') if os.name == 'posix' else None


def getLocalIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #print(s.getsockname())       #O/P: ('0.0.0.0', 0)
    s.connect(("8.8.8.8", 80))    #Ephemeral Port will be assigned by OS randomly
    #print(s.getsockname())
    ip = s.getsockname()[0]
    s.close()
    return ip

while True:
    localIP = getLocalIP()
    reciever = Reciever()
    t = threading.Thread(target = reciever.listen)
    t.start()
    initiate(True)

    color('C')
    print("********************************************")
    print("*                                          *")
    print("*         Welcome To Phoenix Chat          *")
    print("*                                          *")
    print("********************************************")
    color('A')

    print("\nYour IP: ", localIP)
    color('B')
    targetIP = input('Enter target IP: ')
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('\nPress q to exit.\n')
    while True:
        color('E')
        msg = input("\nYou: ")
        if msg == 'q':
            ss.sendto('kill #7!'.encode(), (localIP, localPort))
            initiate(False)
            ss.close()
            color('F')
            clearSrc()
            break
        ss.sendto(msg.encode(), (targetIP, targetPort))
    break
clearSrc()


