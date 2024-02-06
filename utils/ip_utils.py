import socket


def get_public_ip():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to a remote server
        s.connect(("8.8.8.8", 80))
        # Get the local IP address
        public_ip = s.getsockname()[0]
    except socket.error:
        public_ip = "Unable to retrieve public IP"

    finally:
        # Close the socket
        s.close()

    return public_ip
