import string
import secrets
import subprocess
import platform

def generate_password(length=12):
    """Generates a secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 1):
            break
    return password

def get_local_users():
    """Retrieves a list of local users on Windows."""
    if platform.system().lower() != 'windows':
        return False, "This feature is currently only supported on Windows."
    
    try:
        command = ['powershell', '-Command', 'Get-LocalUser | Select-Object Name, Enabled | ConvertTo-Csv -NoTypeInformation']
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        
        lines = output.strip().split('\n')
        if len(lines) <= 1:
            return True, []
        
        users = []
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) >= 2:
                name = parts[0].strip('"')
                enabled = parts[1].strip('"')
                users.append({"Name": name, "Enabled": enabled})
        return True, users
    except Exception as e:
        return False, str(e)
