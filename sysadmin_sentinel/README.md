# 🛡️ SysAdmin Sentinel

SysAdmin Sentinel is a robust, interactive Command-Line Interface (CLI) application developed in Python. It acts as an all-in-one centralized toolkit designed specifically for **L1 Help Desk Technicians, IT Support, and System Administrators**. 

By automating repetitive troubleshooting sequences, fetching critical diagnostics, and securely logging every action taken, SysAdmin Sentinel drastically reduces ticket resolution times.

---

## ✨ Core Features

1. **🖥️ Live System Diagnostics**
   * Automatically fetches OS, RAM, CPU, and Disk partitions.
   * Employs real-time logic to flag critical thresholds (e.g., > 90% CPU, < 10GB free disk space) with colored warnings.

   ![System Diagnostic](../Screenshots/1.%20system%20diagnostic.png)

2. **🌐 Network Troubleshooting**
   ![Network Troubleshooting](../Screenshots/2.%20network%20troubleshooting.png)
   * **Ping Sweeps**: Pings target domains with robust packet-loss analysis.
   * **Port Checking**: Verifies if specific TCP ports are open.
   * **Auto-Resolution**: Automatically transforms domains into IPv4 addresses prior to port scanning.
   * **Local Network**: Instantly reads your active local IP.
   
   ![Get IP](../Screenshots/2.%20get%20IP.png)

3. **🛠️ Automated Windows Remediation**
   ![Remediation Tasks](../Screenshots/3.%20Remediation%20tasks.png)
   * **Clear User `%TEMP%`**: Employs an ultra-fast `os.scandir` algorithm to wipe hidden temporary files safely.
     ![Clear Temp Files](../Screenshots/3.%20clear%20temp%20files.png)
   * **Flush DNS**: Resets the local DNS resolver cache to fix routing errors. 
   * **Service Restarts**: Reboots the `Print Spooler` (requires Administrator context).
   
4. **👥 User Management**
   * Parses active/disabled local Windows users using internal PowerShell hooks.
   * Includes a customizable, cryptographically secure password generator for resetting user passwords securely.

   ![User Management](../Screenshots/4.%20user%20management.png)

5. **🎫 Secure Ticketing Logs**
   ![Ticketing Logs](../Screenshots/5.%20ticketing%20logs.png)
   * Built on an internal SQLite database using Write-Ahead Logging (WAL) for concurrency.
   * Logs every single action a technician takes directly into `tickets.db`.
   * **Export Engine**: Allows the technician to press a button and instantly export their action logs into an audit-ready `.csv` file.

   ![Ticket Exported CSV](../Screenshots/5.%20ticket%20exported%20csv%20file.png)

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.8+**
* An active Windows environment (required for full remediation functionality).

### Instant Setup (Recommended)
This complete package contains a smart `start.bat` script. Simply run it from the terminal or double-click it. 
It will automatically:
1. Detect or create an isolated Python Virtual Environment (`venv`).
2. Install all external dependencies.
3. Launch the application securely.

```bat
.\start.bat
```

### Manual Setup
If you prefer configuring your environment manually, you can use `pip`:
```bash
pip install -r requirements.txt
python main.py
```

---

## 🏗️ Project Architecture
* `main.py` - The interactive, color-coded CLI interface connecting all modules.
* `diagnostics.py` - Interacts with system hardware arrays using `psutil`. Data is aggressively LRU-cached for instant loading.
* `network.py` - Handles socket logic, automatic DNS lookups, and secure subprocess pings via Strict Regex Validations.
* `remediation.py` - Touches OS levels, enforces `ctypes` admin-privilege checks, and handles direct file-system tasks safely.
* `user_management.py` - Hooks into Windows underlying PowerShell structures safely.
* `ticketing.py` - Fast, concurrency-protected SQLite engine with robust `.csv` writing capabilities.

---
*Developed as an all-in-one portfolio piece demonstrating Python's extreme utility in practical IT Support environments.*
