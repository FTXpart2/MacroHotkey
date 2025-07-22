import tkinter as tk
import keyboard
import threading
import time

pressing = False

def key_loop(key, interval):
    while pressing:
        keyboard.press_and_release(key)
        time.sleep(interval)

def start_pressing():
    global pressing
    key = key_entry.get().strip().lower()

    try:
        interval = float(interval_entry.get()) / 1000.0
    except ValueError:
        status_label.config(text="❌ Invalid interval!")
        return

    if not key:
        status_label.config(text="❌ Enter a key to press!")
        return

    pressing = True
    status_label.config(text=f"✅ Pressing '{key.upper()}' every {int(interval*1000)}ms")

    thread = threading.Thread(target=key_loop, args=(key, interval), daemon=True)
    thread.start()

def stop_pressing():
    global pressing
    pressing = False
    status_label.config(text="⏹️ Stopped")

def toggle_macro():
    global pressing
    if pressing:
        stop_pressing()
    else:
        start_pressing()

def listen_f6():
    while True:
        keyboard.wait('f6')
        root.after(0, toggle_macro)
        time.sleep(0.2)  # Prevent rapid toggling

listener_thread = threading.Thread(target=listen_f6, daemon=True)
listener_thread.start()

def on_close():
    stop_pressing()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Key Macro")
root.geometry("280x240")
root.resizable(False, False)

tk.Label(root, text="Key to Press:").pack(pady=(10, 0))
key_entry = tk.Entry(root)
key_entry.insert(0, "e")
key_entry.pack()

tk.Label(root, text="Interval (ms):").pack(pady=(10, 0))
interval_entry = tk.Entry(root)
interval_entry.insert(0, "100")
interval_entry.pack()

tk.Button(root, text="Start", bg="green", fg="white", command=start_pressing).pack(pady=(15, 5))
tk.Button(root, text="Stop", bg="red", fg="white", command=stop_pressing).pack(pady=(0, 10))

status_label = tk.Label(root, text="F6 to start/stop", fg="gray")
status_label.pack()

tk.Button(root, text="Exit", command=on_close).pack(pady=(5, 5))

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
