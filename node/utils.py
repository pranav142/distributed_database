import socket


def is_valid_ip(ip: str):
        try:
            socket.inet_aton(ip) 
            return True
        except socket.error:
            return False
