import tkinter as tk
from tkinter import messagebox
import time
import random
class SpeedTypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speed Typing App")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_login_screen()

    def create_login_screen(self):
        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

    def login(self):
        # Здесь вы можете добавить логику для проверки авторизации
        # Например, проверьте соответствие введенных данных вашей базе данных

        # Пока что просто выв��дим сообщение
        messagebox.showinfo("Login", "Login successful!")
        self.show_training_page()

    def register(self):
        # Здесь вы можете добавить логику для регистрации нового пользователя
        # Например, сохраните введенные данные в вашей базе данных

        # Пока что просто выводим сообщение
        messagebox.showinfo("Register", "Registration successful!")
        self.show_training_page()

    def show_training_page(self):
        # Уничтожаем фрейм с экрана входа
        self.login_frame.destroy()

        # Создаем новый фрейм для страницы тренировки
        training_frame = tk.Frame(self.root, padx=20, pady=20)
        training_frame.pack()

        # Элементы интерфейса для страницы тренировки
        tk.Label(training_frame, text="Welcome to the Speed Typing Training Page!").grid(row=0, column=0, columnspan=2,
                                                                                         pady=10)

        tk.Label(training_frame, text="Select a difficulty level:").grid(row=1, column=0, columnspan=2, pady=5)

        difficulty_var = tk.StringVar()
        difficulty_var.set("Medium")  # Устанавливаем значение по умолчанию
        difficulty_options = ["Easy", "Medium", "Hard"]

        difficulty_menu = tk.OptionMenu(training_frame, difficulty_var, *difficulty_options)
        difficulty_menu.grid(row=2, column=0, columnspan=2, pady=5)

        start_button = tk.Button(training_frame, text="Start Training", command=self.start_training)
        start_button.grid(row=3, column=0, columnspan=2, pady=10)



    def start_training(self):

        # Создаем новое окно для тренировки
        self.training_window = tk.Toplevel(self.root)
        self.training_window.title("Speed Typing Training")

        # Загружаем случайный текст для тренировки
        exercise_text = self.get_random_text()

        # Добавляем элементы интерфейса для тренировки
        tk.Label(self.training_window, text="Type the following:").pack(pady=10)

        exercise_label = tk.Label(self.training_window, text=exercise_text, font=("Helvetica", 12), wraplength=400)
        exercise_label.pack()

        entry = tk.Entry(self.training_window)
        entry.pack(pady=10)

        start_time = time.time()

        def check_input():
            entered_text = entry.get()
            if entered_text == exercise_text:
                elapsed_time = time.time() - start_time
                messagebox.showinfo("Training", f"Training completed in {elapsed_time:.2f} seconds!")
                self.training_window.destroy()

        check_button = tk.Button(self.training_window, text="Check", command=check_input)
        check_button.pack(pady=10)

    def get_random_text(self):
        # Здесь вы можете реализовать логику для загрузки случайного текста
        # Например, создать список текстов и выбрать один случайным образом
        texts = ["The quick brown fox jumps over the lazy dog.", "Hello, World!", "Type faster for better results!"]
        return random.choice(texts)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTypingApp(root)
    root.mainloop()
    your_instance = SpeedTypingApp()
    # Добавляем кнопку "Start Training" в главное окно
    start_button = tk.Button(your_instance.main_frame, text="Start Training", command=your_instance.start_training)
    start_button.pack(pady=10)

    # Добавляем кнопку "Register" в главное окно
    register_button = tk.Button(your_instance.main_frame, text="Register", command=your_instance.register)
    register_button.pack(pady=10)

    # Добавляем поля для ввода имени пользователя и пароля
    username_entry = tk.Entry(your_instance.main_frame, textvariable=your_instance.username_var, placeholder="Username")
    username_entry.pack(pady=5)

    password_entry = tk.Entry(your_instance.main_frame, textvariable=your_instance.password_var, placeholder="Password",
                              show="*")
    password_entry.pack(pady=5)

    # Добавляем кнопку "Login" в окно регистрации
    login_button = tk.Button(your_instance.main_frame, text="Login", command=your_instance.login)
    login_button.pack(pady=10)

    # Запускаем основной цикл Tkinter
    your_instance.root.mainloop()
