import sqlite3
import datetime
import os
import csv

DB_FILENAME = "tickets.db"

def get_db_connection():
    """Creates a fast, highly-concurrent SQLite connection."""
    conn = sqlite3.connect(DB_FILENAME, timeout=10) # 10s timeout prevents database is locked errors
    # Enable Write-Ahead Logging (WAL) for massive speed boost and concurrent read/writes
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            action TEXT NOT NULL,
            status TEXT NOT NULL,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_ticket(action, status, details=""):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO tickets (timestamp, action, status, details)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, action, status, details))
        conn.commit()
        ticket_id = cursor.lastrowid
        conn.close()
        return ticket_id
    except sqlite3.Error as e:
        # Silently fail or log to standard out if DB is totally locked, keeping app robust
        print(f"[DB Error]: {e}")
        return None

def get_all_tickets():
    if not os.path.exists(DB_FILENAME):
        return []
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, timestamp, action, status, details FROM tickets ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        
        tickets = []
        for row in rows:
            tickets.append({
                "ID": row[0],
                "Timestamp": row[1],
                "Action": row[2],
                "Status": row[3],
                "Details": row[4]
            })
        return tickets
    except sqlite3.Error:
        return []

def export_to_csv():
    tickets = get_all_tickets()
    if not tickets:
        return False, "No tickets to export."
        
    filename = f"tickets_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ID", "Timestamp", "Action", "Status", "Details"])
            writer.writeheader()
            for ticket in tickets:
                writer.writerow(ticket)
        return True, f"Successfully exported {len(tickets)} tickets to {filename}"
    except Exception as e:
        return False, f"Failed to export CSV: {str(e)}"

init_db()
