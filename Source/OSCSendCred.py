import re
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
from pythonosc.udp_client import SimpleUDPClient

OSC_IP = "127.0.0.1"
OSC_PORT = 9000
DELAY_BETWEEN_MESSAGES = 0.0008
NUM_PRESETS = 4

ADDRESS_RE = re.compile(r'ADDRESS\(([^)]+)\)')
FLOAT_RE = re.compile(r'FLOAT\(([^)]+)\)')
BOOL_RE = re.compile(r'BOOL\(([^)]+)\)')

class OSCSenderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("OSC Send")
        self.master.geometry("900x250")
        self.master.resizable(True, False)

        self.style = ttk.Style()
        self.style.theme_use("winnative")

        self.presets = []
        self.build_interface()

    def build_interface(self):
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill="both", expand=True)

        title = ttk.Label(main_frame, text="🎛️ OSC Log Sender (Multi-Preset)", font=("Segoe UI", 12, "bold"))
        title.pack(anchor="w", pady=5)

        for i in range(NUM_PRESETS):
            self.create_preset_row(main_frame, i)

        # Add hyperlink at the bottom
        link_frame = ttk.Frame(self.master, padding=5)
        link_frame.pack(side="bottom", fill="x")

        link = tk.Label(link_frame, text="By Threevee. This software is free and will always be free", fg="blue", cursor="hand2", font=("Comic Sans MS", 13, "underline"))
        link.pack(side="right", anchor="se", padx=10)
        link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/threeveevr/OSCSend"))

    def create_preset_row(self, parent, index):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=4)

        label = ttk.Label(frame, text=f"Preset {index + 1}")
        label.pack(side=tk.LEFT)

        file_label = ttk.Label(frame, text="No file selected", width=40)
        file_label.pack(side=tk.LEFT, padx=(5, 5))

        browse = ttk.Button(frame, text="Browse", command=lambda: self.select_file(index))
        browse.pack(side=tk.LEFT)

        send = ttk.Button(frame, text="Send", command=lambda: self.start_sending(index))
        send.pack(side=tk.LEFT, padx=3)

        stop = ttk.Button(frame, text="Stop", command=lambda: self.stop_sending(index))
        stop.pack(side=tk.LEFT, padx=3)

        loop_var = tk.BooleanVar()
        loop = ttk.Checkbutton(frame, text="Loop", variable=loop_var)
        loop.pack(side=tk.LEFT, padx=3)

        progress = ttk.Progressbar(frame, orient="horizontal", length=150, mode="determinate")
        progress.pack(side=tk.LEFT, padx=(10, 0), fill="x", expand=False)

        self.presets.append({
            "file": None,
            "file_label": file_label,
            "sending": False,
            "thread": None,
            "loop": loop_var,
            "progress": progress
        })

    def select_file(self, index):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if path:
            self.presets[index]["file"] = path
            self.presets[index]["file_label"].config(text=path.split("/")[-1])

    def start_sending(self, index):
        preset = self.presets[index]
        if not preset["file"]:
            messagebox.showerror("Error", f"No file selected for Preset {index + 1}")
            return
        if preset["sending"]:
            return

        preset["sending"] = True
        preset["progress"]["value"] = 0
        preset["thread"] = threading.Thread(target=self.send_osc_from_log, args=(index,))
        preset["thread"].start()

    def stop_sending(self, index):
        self.presets[index]["sending"] = False

    def send_osc_from_log(self, index):
        preset = self.presets[index]
        client = SimpleUDPClient(OSC_IP, OSC_PORT)
        file_path = preset["file"]

        try:
            while preset["sending"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                total_lines = len(lines)
                sent_count = 0
                preset["progress"]["maximum"] = total_lines

                for line in lines:
                    if not preset["sending"]:
                        break

                    address_match = ADDRESS_RE.search(line)
                    if not address_match:
                        continue

                    address = address_match.group(1)
                    rest = line[address_match.end():]
                    float_matches = FLOAT_RE.findall(rest)
                    bool_matches = BOOL_RE.findall(rest)

                    values = []
                    if float_matches:
                        values = [float(val) for val in float_matches if self.is_float(val)]
                    elif bool_matches:
                        values = [self.parse_bool(val) for val in bool_matches if self.parse_bool(val) is not None]

                    if values:
                        payload = values[0] if len(values) == 1 else values
                        client.send_message(address, payload)

                    sent_count += 1
                    self.master.after(0, lambda i=index, s=sent_count: self.update_progress(i, s))
                    time.sleep(DELAY_BETWEEN_MESSAGES)

                if not preset["loop"].get():
                    break

            preset["sending"] = False
            self.master.after(0, lambda i=index: self.update_progress(i, 0))

        except Exception as e:
            preset["sending"] = False
            messagebox.showerror("Error", f"Error in Preset {index + 1}: {e}")

    def update_progress(self, index, value):
        self.presets[index]["progress"]["value"] = value

    def is_float(self, val):
        try:
            float(val)
            return True
        except ValueError:
            return False

    def parse_bool(self, val):
        v = val.strip().lower()
        if v in ("true", "1"):
            return True
        elif v in ("false", "0"):
            return False
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = OSCSenderGUI(root)
    root.mainloop()
