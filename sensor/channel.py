import socket
import threading
import struct

class Channel:
	def __init__(self, client, ip_addr, port, listener):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.addr = (ip_addr, port)
		self.listener = listener
		
		self.outqueue = []
		self.outqueueLock = threading.Lock()
		
		self.inqueue = []
		self.inqueueLock = threading.Lock()
		
		self.connected = False
		
		if client:
			self.thread = threading.Thread(target=self._connect)
		else:
			self.thread = threading.Thread(target=self._listen)
		
		self.hthread = threading.Thread(target=self._handle)
		
		self.thread.start()
		self.hthread.start()
		
	def send(self, msg):
		if not self.connected:
			return
		with self.outqueueLock:
			self.outqueue.append(msg)
	
	def _connect(self):
		while True:
			try:
				print 'Trying to connect'
				self.sock.connect(self.addr)
				self.connected = True
				self._communicate(self.sock)
			except:
				pass
			finally:
				self.sock.close()
	def _listen(self):
		self.sock.bind(self.addr)
		self.sock.listen(1)
		while True:
			conn, client_addr = self.sock.accept()
			self.connected = True
			self._communicate(conn)
			
	def _communicate(self, conn):
		self.outqueue = []
		self.inqueue = []
		try:
			while True:
				self._send(conn)
				self._receive(conn)
		finally:
			conn.close()
			self.connected = False
			
	def _receive(self, conn):
		data = conn.recv(4)
		num = struct.unpack('!i', data)[0]
		msg = conn.recv(num)
		with self.inqueueLock:
			self.inqueue.append(msg)
		
	def _handle(self):
		while True:
			if not self.inqueue:
				continue
			with self.inqueueLock:
				msg = self.inqueue[0]
				self.inqueue = self.inqueue[1:]
			self.listener.handle(msg)
			
	def _send(self, conn):
		if not self.outqueue:
			return
		with self.outqueueLock:
			msg = self.outqueue[0]
			self.outqueue = self.outqueue[1:]
		num = struct.pack('!i', len(msg))
		conn.send(num)
		conn.send(msg)