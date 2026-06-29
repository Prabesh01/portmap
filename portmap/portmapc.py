from portmap.client.main import PortmapClient
import argparse

def main():
	parser = argparse.ArgumentParser(description="Portmap client interface.")
	parser.add_argument("port", type=int, help="The port number.")
	
	args = parser.parse_args()

	server = PortmapClient(args.port)
		
	server.connect('portmap.freeddns.org', 1024)

if __name__ == "__main__":
	main()
