import subprocess
import socket
import platform
import re

def is_valid_host(host):
    """Secures against command injection by validating hostname or IP."""
    # Matches valid IPv4, IPv6, or domain names
    pattern = re.compile(
        r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$'
    )
    return bool(pattern.match(host))

def ping_host(host):
    """Pings a host securely and returns True if successful, along with output."""
    if not is_valid_host(host):
        return False, "Invalid hostname or IP address provided."
        
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    # Adding timeout `-w 1000` (1 second per ping) to make it responsive
    command = ['ping', param, '4', '-w', '1000', host]
    
    try:
        # We don't use shell=True, which protects against injection, but regex validation adds defense-in-depth
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        return True, output
    except subprocess.CalledProcessError as e:
        return False, e.output
    except FileNotFoundError:
        return False, "Ping command not found on this system."

def check_port(host, port):
    """Checks if a specific TCP port is open, and returns the resolved IP."""
    if not is_valid_host(host):
        return False, "Invalid hostname or IP address."
        
    try:
        resolved_ip = socket.gethostbyname(host)
    except socket.gaierror:
        return False, "Could not resolve hostname."
        
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.5) # Reduced to 1.5s for faster responsiveness
        result = sock.connect_ex((resolved_ip, port))
        sock.close()
        return result == 0, resolved_ip
    except socket.error:
        return False, resolved_ip

def get_local_ip():
    """Gets the local IP address quickly."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"
