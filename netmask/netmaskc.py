from main import NetmaskClient
import argparse

def main():
	parser = argparse.ArgumentParser(description="Netmask client interface.")
	parser.add_argument("port", type=int, help="The port number.")
	
	args = parser.parse_args()

	server = NetmaskClient(args.port)
		
	server.connect('91.208.197.189', 1024)

if __name__ == "__main__":
	main()
