
import time
import psutil
from datetime import datetime, timedelta

# Lista procesów, które rozpraszają (można edytować)
DISTRACTIONS = ['discord.exe', 'tiktok.exe', 'spotify.exe', 'chrome.exe', 'steam.exe']

# Ustawienia sesji
focus_minutes = 25
break_minutes = 5
session_count = 0
log_file = "focus_report.txt"

def check_distractions():
    """Sprawdza, czy któryś z rozpraszaczy jest uruchomiony."""
    distractions_found = []
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() in DISTRACTIONS:
                distractions_found.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return distractions_found

def log_session(start_time, end_time, distractions):
    """Zapisuje sesję do pliku logów."""
    with open(log_file, "a") as f:
        f.write(f"Start: {start_time}, End: {end_time}, Duration: {end_time - start_time}\n")
        if distractions:
            f.write(f"Distractions Detected: {', '.join(distractions)}\n")
        else:
            f.write("No distractions detected.\n")
        f.write("-" * 40 + "\n")

def start_focus_timer():
    """Rozpoczyna jedną sesję skupienia."""
    global session_count
    session_count += 1
    print(f"\n--- Focus Session #{session_count} ---")
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=focus_minutes)

    for remaining in range(focus_minutes * 60, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_display = '{{:02d}}:{{:02d}}'.format(mins, secs)
        print(f'\rFocus Time Remaining: {{time_display}}', end='')
        time.sleep(1)

    print("\nSession complete! Checking for distractions...")
    distractions = check_distractions()
    if distractions:
        print("⚠️  Distractions detected:", ", ".join(distractions))
    else:
        print("✅ No distractions. Well done!")

    end_time = datetime.now()
    log_session(start_time, end_time, distractions)

def start_break_timer():
    """Rozpoczyna przerwę."""
    print(f"\n--- Break Time ({{break_minutes}} min) ---")
    for remaining in range(break_minutes * 60, 0, -1):
        mins, secs = divmod(remaining, 60)
        time_display = '{{:02d}}:{{:02d}}'.format(mins, secs)
        print(f'\rBreak Time Remaining: {{time_display}}', end='')
        time.sleep(1)
    print("\nBreak complete! Back to focus.")

def run_focus_guardian():
    """Główna pętla aplikacji."""
    print("📘 FocusGuardian Console v1.0")
    print("Monitoring distractions and keeping you focused.\n")
    try:
        while True:
            start_focus_timer()
            start_break_timer()
    except KeyboardInterrupt:
        print("\n👋 Exiting FocusGuardian. Stay productive!")

if __name__ == "__main__":
    run_focus_guardian()
