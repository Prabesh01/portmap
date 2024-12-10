from portmap.client.main import PortmapClient
import argparse

def main():
	parser = argparse.ArgumentParser(description="Portmap client interface.")
	parser.add_argument("port", type=int, help="The port number.")
	
	args = parser.parse_args()

	server = PortmapClient(args.port)
		
	server.connect('91.208.197.189', 1024)

if __name__ == "__main__":
	main()
