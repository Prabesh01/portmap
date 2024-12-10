import portmap.client.packets as packets
import threading
import ipaddress
import hashlib
import socket
import select
import sys
import os

# Variables
PACKET_BUFFER = 2048

class PortmapClient(packets.ProtocolHandler):
	class Connection:
		connectionID = 0
		downloadedBytes = 0
		uploadedBytes = 0

	def __init__(self, localPort):
		self.client = True

		self.localHost = "127.0.0.1"
		self.localPort = localPort
		self.connections = []
		self.connectionCounter = 0

		self.bindedAddress = None
		self.isConnected = False

		self.host = None
		self.port = None

		self.communicationKey = '0'

	def terminateConnection(self):
		self.socket.close()
		sys.exit()

	def forwardingThreadTCP(self, uid):
		# Make connection class
		connClass = self.Connection()
		connClass.connectionID = self.connectionCounter
		self.connectionCounter += 1
		self.connections.append(connClass)

		try:
			if ipaddress.ip_network(self.localHost).version == 6:
				localConn = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			else:
				localConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			try:
				localConn.connect((self.localHost, self.localPort))
			except:
				return

			# Connect to server
			conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			try:
				conn.connect((self.host, self.port))
			except:
				print("Connection to "+self.host+":"+str(self.port)+" failed")
				return

			# Send the mode and the UID
			conn.send(b"\x01"+uid)

			# Receive confirmation
			if conn.recv(1) != b"\x01":
				print("Forwarding socket failed.")
				return

			# Forward the connection between the two sockets
			socketList = [localConn, conn]
			shouldCloseSocket = False
			while not shouldCloseSocket:
				readSockets, writeSockets, errorSockets = select.select(socketList, [], socketList, 5000)
				if errorSockets or not readSockets:
					break
				for currentSocket in readSockets:
					oppositeSocket = socketList[1] if currentSocket == socketList[0] else socketList[0]

					data = currentSocket.recv(PACKET_BUFFER)
					if not data or data == b"":
						shouldCloseSocket = True
						break

					if currentSocket == localConn:
						connClass.downloadedBytes += len(data)
					else:
						connClass.uploadedBytes += len(data)

					oppositeSocket.sendall(data)
		except KeyboardInterrupt:
			os._exit(0)
		finally:
			self.connections.remove(connClass)

	def connect(self, host, port):
		try:
			# Resolve the domain
			try:
				host = socket.gethostbyname(host)
			except:
				# If it's not a domain, pass
				pass

			# Check the IP version
			if ipaddress.ip_network(host).version == 6:
				conn = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
			else:
				conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			print("Connecting to the server...")

			self.host = host
			self.port = port

			conn.settimeout(0.5)

			conn.connect((host, port))

			super().__init__(self.communicationKey, conn)
			self.socket = conn

			# Connect with mode 0
			self.socket.send(b"\x00")

			# Send handshake packet

			cHandshake = packets.CHandshakeRequest()
			cHandshake.encryptionKey = self.encryptionKey
			self.sendPacket(cHandshake)

			# Wait for server to send the proof of encryption request
			POERequest = self.recvPacket(packets.SPOERequest)

			# Send response of proof of encryption
			POEResponse = packets.CPOEResponse()
			POEResponse.proofOfEncryptionResult = hashlib.sha256(POERequest.proofOfEncryptionRequest).digest()
			self.sendPacket(POEResponse)

			# Get handshake response
			self.recvPacket(packets.SHandshakeResponse)

			print("Connection with server established successfully!")

			BindRequest = packets.CBindRequest()
			BindRequest.bindMode = 0
			BindRequest.ipVersion = 4
			self.sendPacket(BindRequest)

			BindResponse = self.recvPacket(packets.SBindResponse)

			self.bindedAddress = BindResponse.serverIP+":"+str(BindResponse.serverPort)
			self.isConnected = True

			# print(f"Any requests to {self.bindedAddress} will me mapped to port {self.localPort} on this computer.")
			print(f"[Sucess] Port Mapped: {self.bindedAddress} --> 127.0.0.1:{self.localPort}")
			while True:
				connectionPacket = self.recvPacket(packets.SConnection)
				threading.Thread(target=self.forwardingThreadTCP, args=(connectionPacket.uid,)).start()
			
		except Exception as e:
			print(e)
			os._exit(0)