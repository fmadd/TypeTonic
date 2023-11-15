import tkinter as tk
import time
import threading
import random
from send_json import send_attempt


class TypeSpeedGUI:
    user_id = -1;

    def __init__(self):
        global warr, user_id
        warr = 0
        self.root = tk.Tk()
        self.root.title("TypeTonic")
        self.root.geometry("800x600")

        self.texts = open("text_test.txt", "r").read().split("\n")

        self.frame = tk.Frame(self.root)

        self.sample_label = tk.Label(self.frame, text=random.choice(self.texts), font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)

        self.speed_label = tk.Label(self.frame, text="Speed: \n0.00 CPS\n0.00 CPM\n0.0 Acc", font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset, font=("Helvetica", 24))
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False
        user_id = self.get_user_id()

        self.root.mainloop()

    def start(self, event):
        global warr
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        if not self.sample_label.cget('text').startswith(self.input_entry.get()):
            warr += 1
            print(warr, len(self.input_entry.get()))
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        if self.input_entry.get() == self.sample_label.cget('text').strip():
            self.running = False
            self.input_entry.config(fg="green")

    def get_user_id(self):
        return int(input('Номер пользователя: '))

    def time_thread(self):
        global user_id
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            lenght = len(self.input_entry.get())
            cps = lenght / self.counter
            cpm = cps * 60
            try:
                acc = max(0, 1 - warr / lenght) * 100
            except:
                acc = 0
        self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM \n{acc:.1f}% Acc")
        send_attempt(user_id, cps, cpm, acc)

    def reset(self):
        global warr
        warr = 0
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0.00 CPS\n0.0 CPM\n0.0 Acc")
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)


TypeSpeedGUI()
