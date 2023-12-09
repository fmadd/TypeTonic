import tkinter as tk
import time
import threading
import random
from app_server import *


class TypeSpeedGUI:
    user_id = -1
    mistakes = dict({})
    war = 0
    mood = 'english_10k'
    login='admin'

    def __init__(self):
        print(self.mood)
        self.root = tk.Tk()
        self.root.title("TypeTonic")
        self.root.geometry("800x600")
        with open("text.txt", "r") as f:
            self.texts = f.read().split("\n")

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

        #user_id = self.get_user_id()
        #self.mood = self.get_mode()
        #print(self.mood, self.texts)

        self.root.mainloop()
        self.texts.close()

    def start(self, event):
        self.warr = 0
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        text_example = self.sample_label.cget('text')
        user_text = self.input_entry.get()
        if not text_example.startswith(user_text):
            self.warr += 1
            letter = text_example[min(len(text_example) - 1, len(user_text) - 1)]
            #print(self.warr, letter)
            if letter in self.mistakes:
                self.mistakes[letter] += 1
            else:
                self.mistakes[letter] = 1
                # print(mistakes, letter, mistakes[letter])
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        if self.input_entry.get() == self.sample_label.cget('text').strip():
            self.running = False
            self.input_entry.config(fg="green")

    '''
    def authenticate():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        # Проверка наличия пользователя в базе данных
        if entered_username in users and users[entered_username] == entered_password:
            message_label.config(text="Успешная аутентификация!")
        else:
            message_label.config(text="Неверное имя пользователя или пароль")

    def register():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        # Регистрация нового пользователя
        if entered_username not in users:
            users[entered_username] = entered_password
            message_label.config(text="Регистрация прошла успешно")
        else:
            message_label.config(text="Пользователь уже существует")
    '''

    def get_user_id(self):
        return int(input('Номер пользователя: '))

    def get_mode(self):
        st = input('режим: ')
        return st.split()
    def set_mode(self, lang, id): # устанавливает режим текста
        with open(f"{lang}_{id}.json", "r") as f:
            obj = f.read().loads()
            self.texts = obj["words"]

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            lenght = len(self.input_entry.get())
            len_out = len(self.sample_label.cget('text'))
            cps = lenght / self.counter
            cpm = cps * 60
            try:
                acc = max(0, 1 - self.warr / len_out) * 100
            except:
                acc = 0
        self.speed_label.config(text=f"Speed: \n{cps:.2f} CPS\n{cpm:.2f} CPM \n{acc:.1f}% Acc")
        #send_attempt(self.user_id, self.login, cps, cpm, acc, self.mistakes)

    def reset(self):
        self.warr = 0
        self.mistakes = dict({})
        self.running = False
        self.counter = 0
        self.speed_label.config(text="Speed: \n0.00 CPS\n0.0 CPM\n0.0 Acc")
        self.sample_label.config(text=random.choice(self.texts))
        self.input_entry.delete(0, tk.END)


#TypeSpeedGUI()
