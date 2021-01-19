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
	ip = s.getsockname()[0]
	s.close()
	return ip

class rec():
	rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def __init__(self):
		self._running = True
		self.rs.bind((localIP, localPort))
	
	def stop(self):
		self._running = False

	def run(self):
		while self._running:
			x = self.rs.recvfrom(1024)
			if x[0].decode() == 'tmnat':
				self.rs.close()
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
	os.system('tput setaf 6')
	print('\nYour ip: ', localIP)
	os.system('tput setaf 4')
	targetIP = input('Enter target IP: ')
	ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('\nPress 0 to exit.\n')
	while True:
		os.system('tput setaf 3')
		msg = input('\nYou: ')
		if msg == '0' or msg == 'q':
			os.system('firewall-cmd --remove-port=' + str(localPort) + '/udp > /dev/null 2>&1')
			recObj.stop()
			ss.sendto('tmnat'.encode(), (localIP, localPort))
			ss.close()
			os.system('tput setaf 7')
			cleaner()
			break
		else:
			ss.sendto(msg.encode(), (targetIP, targetPort))
	break
	
