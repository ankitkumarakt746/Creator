import os
import socket
import threading

localIP = ''
localPort = 5555
targetIP = ''
targetPort = localPort

def cleaner():
	if os.name == 'nt':
		os.system('cls')
	elif os.name == 'posix':
		os.system('firewall-cmd --add-port=' + str(localPort) + '/udp > /dev/null 2>&1')
		os.system('clear')

def get_localIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class rec():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def __init__(self):
		self._running = True
		self.s.bind((localIP, localPort))
	
	def stop(self):
		self._running = False

	def run(self):
		while self._running:
			x = self.s.recvfrom(1024)
			if x[0].decode() == 'tmnat':
				break
			os.system('tput setaf 2')
			print('\n' + x[1][0] + ': ' + x[0].decode())
			print('Reply- ')


while True:
	localIP = get_localIP()
	recObj = rec()
	t = threading.Thread(target = recObj.run)
	t.start()
	
	cleaner()
	os.system('tput setaf 1')
	print("********************************************")
	print("*                                          *")
	print("*         Welcome To Phoenix Chat          *")
	print("*                                          *")
	print("********************************************")
	print('\nYour ip: ', localIP)
	targetIP = input('Enter target IP: ')
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('\nPress 0 to exit.\n')
	while True:
		os.system('tput setaf 3')
		msg = input('\nYou: ')
		if msg == '0' or msg == 'q':
			os.system('firewall-cmd --remove-port=' + str(localPort) + '/udp > /dev/null 2>&1')
			recObj.stop()
			s.sendto('tmnat'.encode(), (localIP, localPort))
			os.system('tput setaf 7')
			cleaner()
			break
		else:
			s.sendto(msg.encode(), (targetIP, targetPort))
	break






















'''def reciever():
	r = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	r.bind((localIP, localPort))
	while True:
		x = r.recvfrom(1024)
		print(x[0][1] + ': ' + x[0].decode())'''


#x1 = threading.Thread(target=reciever)
	#x1.start()
