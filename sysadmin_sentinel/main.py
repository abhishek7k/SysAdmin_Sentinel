from colorama import init, Fore, Style, Back
from tabulate import tabulate
import diagnostics
import network
import remediation
import ticketing
import user_management
import sys
import os

# Initialize colorama for Windows colors
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print(Fore.CYAN + "="*60)
    print(Fore.CYAN + "      SysAdmin Sentinel - Advanced Technician Menu      ")
    print(Fore.CYAN + "="*60)
    
    # Check Admin Status softly for warning display
    admin_status = Fore.GREEN + "[Admin]" if remediation.is_admin() else Fore.YELLOW + "[User]"
    print(f" Privilege Level: {admin_status}")
    print(Fore.CYAN + "-"*60)
    
    print("1. " + Fore.GREEN + "System Diagnostics" + Style.RESET_ALL + " (CPU, RAM, Disk)")
    print("2. " + Fore.GREEN + "Network Troubleshooting" + Style.RESET_ALL + " (Ping, Ports, IP)")
    print("3. " + Fore.GREEN + "Remediation Tasks" + Style.RESET_ALL + " (Flush DNS, Clear Temp, Services)")
    print("4. " + Fore.GREEN + "User Management" + Style.RESET_ALL + " (Passwords, Local Users)")
    print("5. " + Fore.GREEN + "Ticketing System" + Style.RESET_ALL + " (History, CSV Export)")
    print("0. " + Fore.RED + "Exit" + Style.RESET_ALL)
    print(Fore.CYAN + "="*60)

def handle_diagnostics():
    clear_screen()
    print(Fore.YELLOW + "\n[*] Gathering System Information...")
    sys_info = diagnostics.get_system_info()
    print(f"OS: {sys_info['System']} {sys_info['Release']} ({sys_info['Machine']})")
    print(f"Hostname: {sys_info['Node Name']}")
    
    print(Fore.YELLOW + "\n[*] Gathering Hardware Information...")
    cpu_pct = diagnostics.get_cpu_info()
    
    # CPU Warning Logic
    if cpu_pct > 90:
        print(f"CPU Usage: " + Back.RED + Fore.WHITE + f"{cpu_pct}% [CRITICAL WARNING]" + Style.RESET_ALL)
    elif cpu_pct > 75:
        print(f"CPU Usage: " + Fore.YELLOW + f"{cpu_pct}% [WARNING: High Usage]" + Style.RESET_ALL)
    else:
        print(f"CPU Usage: {cpu_pct}%")
        
    mem = diagnostics.get_memory_info()
    # RAM Warning Logic
    if mem['Percentage'] > 90:
        print(f"Memory Usage: {mem['Used']} / {mem['Total']} (" + Back.RED + Fore.WHITE + f"{mem['Percentage']}% [CRITICAL]" + Style.RESET_ALL + ")")
    else:
        print(f"Memory Usage: {mem['Used']} / {mem['Total']} ({mem['Percentage']}%)")
    
    print(Fore.YELLOW + "\n[*] Gathering Disk Information...")
    disks = diagnostics.get_disk_info()
    disk_table = []
    
    for d in disks:
        disk_str = f"{d['Percentage']}%"
        if d['Percentage'] > 90 or d['Free_GB'] < 10:
            disk_str = Back.RED + Fore.WHITE + f"{d['Percentage']}% [LOW SPACE]" + Style.RESET_ALL
        
        disk_table.append([d['Device'], d['Used'], d['Total'], d['Free_Formatted'], disk_str])
        
    print(tabulate(disk_table, headers=["Drive", "Used", "Total", "Free Space", "Percentage"], tablefmt="grid"))
    
    ticketing.log_ticket("System Diagnostics", "Success", "Checked Hardware Stats.")
    input(Fore.CYAN + "\nPress Enter to return to the main menu...")

def handle_network():
    clear_screen()
    print(Fore.CYAN + "--- Network Troubleshooting ---")
    print("1. Get Local IP")
    print("2. Ping a Host (4 Packets)")
    print("3. Check an Open Port")
    print("0. Back")
    
    choice = input("Select an option: ")
    if choice == '1':
        ip = network.get_local_ip()
        print(f"\nLocal IP: {ip}")
        ticketing.log_ticket("Network - Get IP", "Success", f"IP: {ip}")
    elif choice == '2':
        host = input("Enter host to ping (e.g., google.com or 8.8.8.8): ")
        print(Fore.YELLOW + f"\nPinging {host}...")
        success, output = network.ping_host(host)
        
        # Highlight packet loss in the output if it's Windows format
        if "Lost =" in output:
            lines = output.split('\n')
            for line in lines:
                if "Lost =" in line or "loss" in line.lower():
                    print(Fore.CYAN + Style.BRIGHT + line + Style.RESET_ALL)
                else:
                    print(line)
        else:
            print(output)
            
        ticketing.log_ticket("Network - Ping", "Success" if success else "Failed", f"Target: {host}")
    elif choice == '3':
        host = input("Enter host/domain: ")
        port = input("Enter port (e.g., 443): ")
        if port.isdigit():
            print(Fore.YELLOW + f"\nChecking {host}:{port}...")
            is_open, ip_resolved = network.check_port(host, int(port))
            
            if ip_resolved != host and ip_resolved != "Could not resolve hostname.":
                print(f"Auto-Resolved Domain to IP: {Fore.CYAN}{ip_resolved}{Style.RESET_ALL}")
                
            if is_open:
                print(Fore.GREEN + f"Port {port} on {ip_resolved} is OPEN.")
            else:
                print(Fore.RED + f"Port {port} on {ip_resolved} is CLOSED or unreachable.")
            ticketing.log_ticket("Network - Port Check", "Success", f"Checked {host}:{port} ({ip_resolved}). Result: {'OPEN' if is_open else 'CLOSED'}")
        else:
            print(Fore.RED + "Invalid port.")
    
    if choice != '0':
        input(Fore.CYAN + "\nPress Enter to return to the main menu...")

def handle_remediation():
    clear_screen()
    print(Fore.CYAN + "--- Remediation Tasks ---")
    if not remediation.is_admin():
        print(Fore.YELLOW + "⚠️ WARNING: You are not running as Administrator. Some tasks (Spooler) will fail.")
        
    print("1. Flush DNS Cache")
    print("2. Clear User Temp Files")
    print("3. Restart Print Spooler")
    print("0. Back")
    
    choice = input("Select an option: ")
    if choice == '1':
        print(Fore.YELLOW + "Flushing DNS...")
        success, output = remediation.flush_dns()
        print(output)
        ticketing.log_ticket("Remediation - Flush DNS", "Success" if success else "Failed")
    elif choice == '2':
        print(Fore.YELLOW + "Clearing Temp Files...")
        success, output = remediation.clear_temp_files()
        print(output)
        ticketing.log_ticket("Remediation - Clear Temp", "Success" if success else "Failed", output)
    elif choice == '3':
        print(Fore.YELLOW + "Restarting Print Spooler...")
        if not remediation.is_admin():
            print(Fore.RED + "Access Denied. You must right-click and Run as Administrator to manage services.")
        else:
            success, output = remediation.restart_print_spooler()
            if success:
                print(Fore.GREEN + "Print Spooler restarted successfully.")
            else:
                print(Fore.RED + output)
            ticketing.log_ticket("Remediation - Print Spooler", "Success" if success else "Failed", output)
        
    if choice != '0':
        input(Fore.CYAN + "\nPress Enter to return to the main menu...")

def handle_users():
    clear_screen()
    print(Fore.CYAN + "--- User Management ---")
    print("1. Generate Secure Password")
    print("2. List Local Windows Users")
    print("0. Back")
    
    choice = input("Select an option: ")
    if choice == '1':
        length_str = input("How many characters? (Default 12): ")
        length = 12
        if length_str.isdigit() and int(length_str) > 5:
            length = int(length_str)
        try:
            pwd = user_management.generate_password(length)
            print(Fore.GREEN + f"\nGenerated Password: {pwd}")
            ticketing.log_ticket("User Mgmt - Gen Password", "Success", f"Generated {length}-char password.")
        except Exception as e:
            print(Fore.RED + f"Error generating password: {e}")
    elif choice == '2':
        print(Fore.YELLOW + "\nFetching local users...")
        success, users = user_management.get_local_users()
        if success:
            user_table = []
            for u in users:
                # Colorize the Active/Disabled field
                status = Fore.GREEN + u['Enabled'] + Style.RESET_ALL if u['Enabled'].lower() == "true" else Fore.RED + u['Enabled'] + Style.RESET_ALL
                user_table.append([u['Name'], status])
            print(tabulate(user_table, headers=["Username", "Is Enabled"], tablefmt="grid"))
        else:
            print(Fore.RED + f"Error: {users}")
        ticketing.log_ticket("User Mgmt - List Users", "Success" if success else "Failed")
        
    if choice != '0':
        input(Fore.CYAN + "\nPress Enter to return to the main menu...")

def handle_tickets():
    clear_screen()
    print(Fore.CYAN + "--- Ticketing Logs ---")
    print("1. View Top 15 Latest Tickets")
    print("2. Export All Tickets to CSV")
    print("0. Back")
    
    choice = input("Select an option: ")
    if choice == '1':
        tickets = ticketing.get_all_tickets()
        if not tickets:
            print("No tickets logged yet.")
        else:
            t_table = [[t['ID'], t['Timestamp'], t['Action'], t['Status']] for t in tickets[:15]]
            print(tabulate(t_table, headers=["ID", "Timestamp", "Action", "Status"], tablefmt="grid"))
    elif choice == '2':
        success, msg = ticketing.export_to_csv()
        if success:
            print(Fore.GREEN + msg)
        else:
            print(Fore.RED + msg)

    if choice != '0':
        input(Fore.CYAN + "\nPress Enter to return to the main menu...")

def main():
    ticketing.log_ticket("System", "Info", "SysAdmin Sentinel started.")
    try:
        while True:
            clear_screen()
            display_menu()
            choice = input("Select an option: ")
            
            if choice == '1':
                handle_diagnostics()
            elif choice == '2':
                handle_network()
            elif choice == '3':
                handle_remediation()
            elif choice == '4':
                handle_users()
            elif choice == '5':
                handle_tickets()
            elif choice == '0':
                ticketing.log_ticket("System", "Info", "SysAdmin Sentinel exited.")
                print(Fore.GREEN + "Exiting SysAdmin Sentinel. Goodbye!")
                sys.exit(0)
            else:
                print(Fore.RED + "Invalid choice. Please try again.")
                input("Press Enter...")
    except KeyboardInterrupt:
        ticketing.log_ticket("System", "Info", "SysAdmin Sentinel interrupted by user.")
        print(Fore.YELLOW + "\n[!] Operation cancelled by user. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
