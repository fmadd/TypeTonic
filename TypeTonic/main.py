import tkinter as tk
from tkinter import messagebox, ttk

import random
import threading
from app_server import *


class PersonalCabinet:
    '''
    Класс описывает взаимодействие со структурой личного кабинета пользователя
    '''

    def __init__(self, app):
        '''
        Создание базового объекта класса
        :param app: корень
        '''
        self.nickname = app.account['nickname']
        self.app = app
        self.app.root.title("TypeTonic")

    def clear(self):
        '''
        Очищение панели для новых виджетов
        '''
        for i in self.app.root.winfo_children():
            i.destroy()

    def clear_table(self):
        '''
        Очищение таблицы
        '''
        for i in self.app.root.winfo_children():
            st = str(i)
            if st.startswith('.!treeview'): i.destroy()

    def show_acc(self):
        '''
        Функция показывает пользователю набор кнопок личного кабинета
        :return:
        '''
        self.app.root.title("Личный кабинет")

        self.account_frame = tk.Frame(self.app.root, padx=90, pady=240)

        self.logout_button = tk.Button(self.account_frame, text="Выйти из аккаунта", command=self.logout, font=("Helvetica", 10))
        self.logout_button.grid(row=0, column=3, columnspan=1, pady=5)

        self.delete_account_button = tk.Button(self.account_frame, text="Удалить аккаунт", command=self.delete_account, font=("Helvetica", 10))
        self.delete_account_button.grid(row=1, column=3, columnspan=1, pady=5)

        self.top_users_button = tk.Button(self.account_frame, text="Топ пользователей", command=self.show_top_users, font=("Helvetica", 10))
        self.top_users_button.grid(row=1, column=1, columnspan=1, pady=5)

        self.dynamics_button = tk.Button(self.account_frame, text="Динамика пользователя", command=self.show_dynamics, font=("Helvetica", 10))
        self.dynamics_button.grid(row=0, column=0, columnspan=1, pady=5)

        self.last_attempts_button = tk.Button(self.account_frame, text="Последние попытки",
                                              command=self.show_last_attempts, font=("Helvetica", 10))
        self.last_attempts_button.grid(row=1, column=0, columnspan=1, pady=5)

        self.problematic_letters_button = tk.Button(self.account_frame, text="Проблемные буквы",
                                                    command=self.show_problematic_letters, font=("Helvetica", 10))
        self.problematic_letters_button.grid(row=0, column=2, columnspan=1, pady=5)

        self.top_problematic_letters_button = tk.Button(self.account_frame, text="Топ проблемных букв",
                                                        command=self.show_top_problematic_letters, font=("Helvetica", 10))
        self.top_problematic_letters_button.grid(row=1, column=2, columnspan=1, pady=5)

        self.weekly_rating_button = tk.Button(self.account_frame, text="Рейтинг за неделю",
                                              command=self.show_weekly_rating, font=("Helvetica", 10))
        self.weekly_rating_button.grid(row=0, column=1, columnspan=1, pady=5)

        self.training_panel_button = tk.Button(self.account_frame, text="Начать тренировку",
                                               command=self.show_training_panel, font=("Helvetica", 14))
        self.training_panel_button.grid(row=2, column=1, columnspan=2, pady=5)

        self.account_frame.pack()

    def logout(self):
        '''
        Выход из аккаунта пользователя
        '''
        self.app.db_service.log_out()
        self.app.show_login_panel()

    def delete_account(self):
        '''
        Удаление аккаунта пользователя из базы
        '''
        self.app.db_service.del_user()
        self.app.show_login_panel()
        message = f"Ваш аккаунт удален\n"
        messagebox.showinfo("Успех", message)

    def show_training_panel(self):
        '''
        Показать панель тренировок
        :return:
        '''
        self.app.show_training_mode_panel()

    def show_top_users(self):
        '''
        Показывает топ пользователей
        '''
        self.clear_table()
        tb = self.app.db_service.get_top_users_all()
        tb = json.loads(tb)
        attempts = tb['stat']
        table = ttk.Treeview(self.app.root)

        table['columns'] = ('login', 'cps', 'cpm', 'accuracy')
        table.heading('#0', text='Номер')
        table.column('#0', width=50)
        table.heading('login', text='Логин')
        table.column('login', width=100)
        table.heading('cps', text='Символы в секунду')
        table.column('cps', width=100)
        table.heading('cpm', text='Символы в минуту')
        table.column('cpm', width=100)
        table.heading('accuracy', text='Точность, %')
        table.column('accuracy', width=100)

        for i, attempt in enumerate(attempts, start=1):
            login, cps, cpm, accuracy = attempt
            table.insert(parent='', index='end', iid=i, text=str(i),
                         values=(login, cps, cpm, accuracy))

        table.pack(expand=True, fill='both')

    def show_dynamics(self):
        '''
        Показывает изменение средних значений пользователя
        '''
        self.clear_table()
        tb = self.app.db_service.user_dynamics()
        tb = json.loads(tb)
        attempts = tb['stat']
        if (attempts == []):
            message = f"Пользователь сделал слишком мало попыток\n"
            messagebox.showinfo("Неудача", message)
            return
        table = ttk.Treeview(self.app.root)

        table['columns'] = ('login', 'cps', 'cpm', 'accuracy')
        table.heading('login', text='Логин')
        table.column('login', width=50)
        table.heading('cps', text='Символы в секунду')
        table.column('cps', width=100)
        table.heading('cpm', text='Символы в минуту')
        table.column('cpm', width=100)
        table.heading('accuracy', text='Точность, %')
        table.column('accuracy', width=100)

        for i, attempt in enumerate(attempts, start=1):
            login, cps, cpm, accuracy = attempt
            table.insert(parent='', index='end', iid=i, text=str(i),
                         values=(login, cps, cpm, accuracy))

        table.pack(expand=True, fill='both')

    def show_last_attempts(self):
        '''
        Показывает до 20 последних попыток
        '''
        self.clear_table()
        tb = self.app.db_service.user_log()
        tb = json.loads(tb)
        attempts = tb['stat']
        table = ttk.Treeview(self.app.root)

        table['columns'] = ('cps', 'cpm', 'accuracy')
        table.heading('#0', text='Номер')
        table.column('#0', width=50)
        table.heading('cps', text='Символы в секунду')
        table.column('cps', width=100)
        table.heading('cpm', text='Символы в минуту')
        table.column('cpm', width=100)
        table.heading('accuracy', text='Точность, %')
        table.column('accuracy', width=100)

        for i, attempt in enumerate(attempts, start=1):
            cps, cpm, accuracy = attempt
            table.insert(parent='', index='end', iid=i, text=str(i),
                         values=(cps, cpm, accuracy))

        table.pack(expand=True, fill='both')

    def show_problematic_letters(self):
        '''
        Показывает самые проблемные буквы пользователя
        '''
        self.clear_table()
        tb = self.app.db_service.get_user_letter()
        tb = json.loads(tb)

        attempts = tb['stat']
        table = ttk.Treeview(self.app.root)

        table['columns'] = ('letter', 'cnt')
        table.heading('#0', text='Номер')
        table.column('#0', width=50)
        table.heading('letter', text='Буква')
        table.column('letter', width=100)
        table.heading('cnt', text='Колличество ошибок')
        table.column('cnt', width=100)

        for i, attempt in enumerate(attempts, start=1):
            letter, cnt = attempt

            table.insert(parent='', index='end', iid=i, text=str(i),
                         values=(letter, cnt))

        table.pack(expand=True, fill='both')

    def show_top_problematic_letters(self):
        '''
        Показывает самые проблемные буквы всех пользователей
        '''
        self.clear_table()
        tb = self.app.db_service.get_top_letter()
        tb = json.loads(tb)

        attempts = tb['stat']
        table = ttk.Treeview(self.app.root)

        table['columns'] = ('letter', 'cnt')
        table.heading('#0', text='Номер')
        table.column('#0', width=50)
        table.heading('letter', text='Буква')
        table.column('letter', width=100)
        table.heading('cnt', text='Колличество ошибок')
        table.column('cnt', width=100)

        for i, attempt in enumerate(attempts, start=1):
            letter, cnt = attempt

            table.insert(parent='', index='end', iid=i, text=str(i),
                         values=(letter, cnt))

        table.pack(expand=True, fill='both')

    def show_weekly_rating(self):
        '''
        Показывает рейтинг за последнюю неделю
        '''
        self.clear_table()
        tb = self.app.db_service.get_top_users_week()
        tb = json.loads(tb)
        attempts = tb['stat']
        table = ttk.Treeview(self.app.root)

        table['columns'] = ('login', 'cps', 'cpm', 'accuracy')
        table.heading('#0', text='Номер')
        table.column('#0', width=50)
        table.heading('login', text='Логин')
        table.column('login', width=100)
        table.heading('cps', text='Символы в секунду')
        table.column('cps', width=100)
        table.heading('cpm', text='Символы в минуту')
        table.column('cpm', width=100)
        table.heading('accuracy', text='Точность, %')
        table.column('accuracy', width=100)

        # Заполнение таблицы данными
        for i, attempt in enumerate(attempts, start=1):
            login, cps, cpm, accuracy = attempt
            table.insert(parent='', index='end', iid=i, text=str(i),
                         values=(login, cps, cpm, accuracy))

        # Отображение таблицы
        table.pack(expand=True, fill='both')


class LoginPanel:
    '''
    Класс описывает методы для авторизации и аутентификации пользователей
    '''

    def __init__(self, app):
        '''
        Создание панели логина с базовыми настройками
        :param app: корень панели
        '''
        self.db_service = app.db_service
        self.app = app
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

    def clear(self):
        '''
        Функция очищает окно от старых виджетов
        '''
        for i in self.app.root.winfo_children():
            i.destroy()

    def show_login_screen(self):
        '''
        Показывает пользователю экран авторизации
        '''
        self.login_frame = tk.Frame(self.app.root, padx=240, pady=200)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)

    def login(self):
        '''
        Функция отправляет запрос на аутентификацию к базе данных
        '''

        self.username = self.username_var.get()
        self.password = self.password_var.get()

        if not self.username or not self.password:
            messagebox.showerror("Error", "Введите парль и логин")
            return
        try:
            self.db_service.log_in(self.username, self.password)
            message = f"Вы успешно вошли в аккаунт\n"
            messagebox.showinfo("Имя пользователя", message)
            self.app.login_success(self.username)
        except:
            message = f"Неверный логин или пароль\n"
            messagebox.showinfo("Имя пользователя", message)

    def register(self):
        '''
        Функция регестрирует пользователя, сохраняя его в базе данных
        :return:
        '''
        self.username = self.username_var.get()
        self.password = self.password_var.get()

        if not self.username or not self.password:
            messagebox.showerror("Ошибка", "Введите парль и логин")
            return
        if self.db_service.valid_password(self.password):
            try:
                self.db_service.reg_user(self.username, self.password)
                message = f"Вы успешно зарегистрировались\n"
                messagebox.showinfo("Имя пользователя", message)

            except:
                message = f"Пользователь с таким ником уже зарегистрирован/использован слабый пароль"
                messagebox.showinfo("Login", message)
        else:
            message = f"Пароль слишком слабый, используйте только цифры и буквы для пароля длинной не менее 6 символов"
            messagebox.showinfo("Login", message)


class TrainingModePanel:
    '''
    Класс описывает панель для тренировок пользователя
    '''

    def __init__(self, app):
        '''
        Создает базовый экран настроек тренировки
        :param app: корень панели
        '''
        self.app = app
        self.trans = {'Легкий': 1, 'Средний': 2, 'Сложный': 3}

    def clear(self):
        '''
        Функция очищает окно от старых виджетов
        '''
        for i in self.app.root.winfo_children():
            i.destroy()

    def show_training_mode_page(self, mode):
        '''
        Показывает пользователю тренировочную панель
        :param dict mode: режим тренировки
        '''
        self.training_frame = tk.Frame(self.app.root, padx=240, pady=200)
        self.training_frame.pack()

        tk.Label(self.training_frame, text="TypeTonic!").grid(row=0, column=1,
                                                              columnspan=2,
                                                              pady=10)
        tk.Label(self.training_frame, text="Выберете сложность:").grid(row=1, column=0, columnspan=2, pady=5)

        difficulty_var = tk.StringVar()
        difficulty_var.set(self.int_to_diff(mode['difficulty']))
        difficulty_options = ["Легкий", "Средний", "Сложный"]

        difficulty_menu = tk.OptionMenu(self.training_frame, difficulty_var, *difficulty_options,
                                        command=self.on_level_selected)
        difficulty_menu.grid(row=2, column=0, columnspan=2, pady=5)

        start_button = tk.Button(self.training_frame, text="Начать тренировку", command=self.start_training)
        start_button.grid(row=3, column=1, columnspan=2, pady=10)

        tk.Label(self.training_frame, text="Выберете язык:").grid(row=1, column=2, columnspan=2, pady=5)

        language_var = tk.StringVar()
        language_var.set(mode['language'])
        language_options = ["Английский", "Русский"]

        language_menu = tk.OptionMenu(self.training_frame, language_var, *language_options,
                                      command=self.on_language_selected)
        language_menu.grid(row=2, column=2, columnspan=2, pady=5)


        user_button = tk.Button(self.training_frame, text="Аккаунт", command=self.show_cabinet_panel)
        user_button.grid(row=4, column=1, columnspan=2, pady=10)

    def on_language_selected(self, value):
        '''
        Функция устанавливает язык тренировки
        :param str value: язык тренировки
        '''
        self.app.set_lang(value)

    def start_training(self):
        '''
        Функция запускает тренировку
        '''
        self.app.start_training()

    def show_cabinet_panel(self):
        '''
        Функция вызывает панель личного кабинета
        :return:
        '''
        self.app.show_cabinet_panel()

    def on_level_selected(self, value):
        '''
        Функция устанавливает сложность тренировки
        :param int value: цифра уровня
        '''
        self.app.set_diff(self.diff_to_int(value))

    def diff_to_int(self, value):
        '''
        Переводит сложность в цифру, для удобства
        :param str value:
        '''
        return self.trans[value]

    def int_to_diff(self, value):
        '''
        Переводит цифру уровня в наименования сложности, для удобства
        :param int value:
        '''
        return {v: k for k, v in self.trans.items()}.get(value)


class TrainingPanel:
    '''
    Класс описывает саму тренировку пользователя и методы связанные с ней
    '''

    def __init__(self, app):
        '''
        Создает объект класса с базовыми настройками
        :param app: корень панели 
        '''
        self.db_service = app.db_service
        self.app = app
        self.nickname = app.account['nickname']
        self.clear_stat()
        self.mistakes = dict({})
        self.warr = 0

    def clear_stat(self):
        '''
        Функция очищает параметры ошибок при каждой попытке
        :return: 
        '''
        self.warr = 0
        self.mistakes = dict({})
        self.running = False
        self.counter = 0

    def clear(self):
        '''
        Функция очищает поле от старых виджетов
        '''
        for i in self.app.root.winfo_children():
            i.destroy()

    def show_training(self, mode):
        '''
        Функция запускает тренировку печати
        :param dict mode: режим тренировки 
        '''

        self.clear()
        self.frame = tk.Frame(self.app.root,  padx=20, pady=90)

        self.sample_label = tk.Label(self.frame, text=self.get_random_text(mode), font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = tk.Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)

        self.speed_label = tk.Label(self.frame, text="Результат: \n0.00 CPS\n0.00 CPM\n0.0 Acc", font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Еще раз", command=lambda: self.reset(mode),
                                      font=("Helvetica", 24))
        self.reset_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = tk.Button(self.frame, text="Выход", command=self.end_training, font=("Helvetica", 24))
        self.reset_button.grid(row=3, column=1, columnspan=2, padx=5, pady=10)

        self.frame.pack(expand=True)

        self.counter = 0
        self.running = False

    def end_training(self):
        '''
        Функция завершает тренировку
        '''
        self.app.end_training()

    def start(self, event):
        '''
        Функция проверяет, если тренировка еще не запущена, то запускает ее. Иначе, проверяет введенный текст на корректность. Если весь текст введен корректно, то функция останавливается
        :param event:
        '''
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
            if letter in self.mistakes:
                self.mistakes[letter] += 1
            else:
                self.mistakes[letter] = 1
            self.input_entry.config(fg="red")
        else:
            self.input_entry.config(fg="black")
        if self.input_entry.get() == self.sample_label.cget('text').strip():
            self.running = False
            self.input_entry.config(fg="green")

    def time_thread(self):
        '''
        Функция производит отсчет времени, прошедшего в тренировке. Пересчитывает колличество ошибок и скорость пользователя. По завершению, отправляет данные на сервер
        '''
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
        self.speed_label.config(text=f"Результат: \n{cps:.2f} CPS\n{cpm:.2f} CPM \n{acc:.1f}% Acc")
        self.db_service.send_attempt(self.nickname, cps, cpm, acc, self.mistakes)

    def reset(self, mode):
        '''
        Функция перезапускает попытку 
        :param dict mode: режим тренировки 
        '''
        self.clear_stat()
        self.speed_label.config(text="Результат: \n0.00 CPS\n0.0 CPM\n0.0 Acc")
        self.sample_label.config(text=self.get_random_text(mode))
        self.input_entry.delete(0, tk.END)

    def get_random_text(self, mode):
        '''
        Функция генирирует текст для тренировки
        :param dict mode: режим тренировки
        :return str: строка с текстом, который необходимо ввести пользователю
        '''

        with open('languages/' + mode["language"] + '_' + str(mode["difficulty"]) + 'k.json') as file:
            text = json.load(file)
            return ' '.join([random.choice(text["words"]) for i in range(1)])


class SpeedTypingApp:
    '''
    Класс опиывает корень приложения и его базовые возможности
    '''

    def __init__(self, root):
        '''
        Создает объект класса с базовыми настройками
        :param root:
        '''
        self.root = root
        self.root.title("TypeTonic")
        self.db_service = app_server()
        self.show_login_panel()
        self.account = {
            'nickname': "Noname"
        }
        self.mode = {
            'difficulty': 2,
            'language': "Русский"
        }

    def clear_all(self):
        '''
        Очищает все существующие панели от виджетов
        '''
        if hasattr(self, 'login_panel'):
            self.login_panel.clear()
        if hasattr(self, 'cabinet_panel'):
            self.cabinet_panel.clear()
        if hasattr(self, 'training_mode_panel'):
            self.training_mode_panel.clear()
        if hasattr(self, 'training_panel'):
            self.training_panel.clear()

    def show_login_panel(self):
        '''
        Показывает панель аутентификации
        '''
        self.clear_all()
        self.login_panel = LoginPanel(self)
        self.login_panel.show_login_screen()

    def show_training_mode_panel(self):
        '''
        Показывает панель настройки тренировки
        '''
        self.clear_all()
        self.training_mode_panel = TrainingModePanel(self)
        self.training_mode_panel.show_training_mode_page(self.mode)

    def show_cabinet_panel(self):
        '''
        Показывает панель личного кабинета пользователя
        '''
        self.clear_all()
        self.cabinet_panel = PersonalCabinet(self)
        self.cabinet_panel.show_acc()

    def show_training_panel(self):
        '''
        Показывает панель тренировки
        '''
        self.clear_all()
        self.training_panel = TrainingPanel(self)
        self.training_panel.show_training(self.mode)

    def login_success(self, username):
        '''
        Функция определяет текущего пользователя в случае успешной авторизации
        :param str username: Имя пользователя
        '''
        self.account['nickname'] = username
        self.show_training_mode_panel()

    def clear(self):
        '''
        Очищение панели от виджетов
        '''
        for i in self.root.winfo_children():
            i.destroy()

    def set_lang(self, value):
        '''
        Функция устанавливает заданный пользователем язык, в режим тренировки
        :param str value: язык тренировки
        '''
        self.mode["language"] = value

    def set_diff(self, value):
        '''
        Функция устанавливает заданный пользователем уровень сложности, в режим тренировки
        :param int value: уровень тренировки
        '''
        self.mode["difficulty"] = value

    def start_training(self):
        '''
        Функция запускает тренировочную панель
        '''
        self.show_training_panel()

    def end_training(self):
        '''
        Функция вызывает панель настроек тренировки, в случае ее завершения
        '''
        self.show_training_mode_panel()


if __name__ == "__main__":
    root = tk.Tk()
    speed_app = SpeedTypingApp(root)
    root.mainloop()
