import tkinter as tk
import asyncio
import threading
from parser import Parser
from Settings import *
from webbrowser import open

class TkinterBase:
    def __init__(self):


        self.root = tk.Tk()
        self.root.geometry("640x460")
        self.root.title("HelpedHome")
        self.root.resizable(False, False)

        self.area_var = tk.StringVar()
        self.money_var = tk.StringVar()
        self.device_var = tk.StringVar()

        self.screen_menu = tk.Frame(self.root)
        self.screen_area = tk.Frame(self.root)
        self.screen_money = tk.Frame(self.root)
        self.screen_devices = tk.Frame(self.root)
        self.screen_result = tk.Frame(self.root)


        tk.Label(
            self.screen_menu,
            text='Помощник по поиску квартир',
            font=('Arial', 18, 'bold')
        ).pack(pady=30)

        tk.Label(
            self.screen_menu,
            text='Нажми кнопку, чтобы начать',
            font=('Arial', 11)
        ).pack()

        tk.Button(
            self.screen_menu,
            text='Начать',
            command=lambda: self.show_frame(self.screen_area),
            width=18
        ).pack(pady=20)

        tk.Label(
            self.screen_area,
            text='Шаг 1: В каком районе ты бы хотел приобрести квартиру/студию?',
            font=('Arial', 12, 'bold')
        ).pack(pady=8)

        tk.Radiobutton(
            self.screen_area,
            text='Заволжский',
            variable=self.area_var,
            value='Заволжский',
            font=('Arial', 12)
        ).pack(anchor='w', padx=50, pady=5)

        tk.Radiobutton(
            self.screen_area,
            text='Московский',
            variable=self.area_var,
            value='Московский',
            font=('Arial', 12)
        ).pack(anchor='w', padx=50, pady=5)

        tk.Radiobutton(
            self.screen_area,
            text='Пролетарский',
            variable=self.area_var,
            value='Пролетарский',
            font=('Arial', 12)
        ).pack(anchor='w', padx=50, pady=5)

        tk.Radiobutton(
            self.screen_area,
            text='Центральный',
            variable=self.area_var,
            value='Центральный',
            font=('Arial', 12)
        ).pack(anchor='w', padx=50, pady=5)

        tk.Button(
            self.screen_area,
            text='Дальше',
            command=lambda: self.go_to_next_step(self.screen_area, self.screen_money),
            width=16
        ).pack(pady=20)

        tk.Button(
            self.screen_area,
            text='В меню',
            command=self.restart,
            width=16
        ).pack()

        # Переменные для хранения значений "от" и "до"
        self.money_from_var = tk.StringVar()
        self.money_to_var = tk.StringVar()

        # Оформление экрана бюджета
        tk.Label(
            self.screen_money,
            text='Шаг 2: Бюджет',
            font=('Arial', 12, 'bold')
        ).pack(pady=20)

        tk.Label(
            self.screen_money,
            text='Сколько вы готовы тратить на аренду квартиры/студии?',
            font=('Arial', 11)
        ).pack(pady=8)

        # Фрейм для строки ввода (от и до)
        self.input_frame = tk.Frame(self.screen_money)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="от:", font=("Arial", 12)).pack(side='left', padx=(0,5))
        tk.Entry(self.input_frame, textvariable=self.money_from_var, width=10, font=("Arial", 12)).pack(side='left', padx=(0,20))
        tk.Label(self.input_frame, text="до:", font=("Arial", 12)).pack(side='left', padx=(0,5))
        tk.Entry(self.input_frame, textvariable=self.money_to_var, width=10, font=("Arial", 12)).pack(side='left')

        # Фрейм для кнопок
        self.buttons_frame = tk.Frame(self.screen_money)
        self.buttons_frame.pack(pady=20)

        tk.Button(
            self.buttons_frame,
            text='Назад',
            command=lambda: self.show_frame(self.screen_area),
            width=16
        ).pack(side='left', padx=10)

        tk.Button(
            self.buttons_frame,
            text='Дальше',
            command=lambda: self.show_frame(self.screen_devices),
            width=16
        ).pack(side='left', padx=10)


        device_options = [
            'Холодильник',
            'Телевизор',
            'Кондиционер',
            'Стиральная машина',
            'Посудомоечная машина',
            'Комнатная мебель',
            'Кухонная мебель',
            'Телефон',
            'Интернет'
            # при необходимости добавьте ещё
        ]

        # Словарь для хранения переменных (ключ — название, значение — BooleanVar)
        self.device_vars = {}

        tk.Label(
            self.screen_devices,
            text='Шаг 3: Какие удобства вы бы хотели в квартире/студии?',
            font=('Arial', 12, 'bold')
        ).pack(pady=20)

        # Фрейм для размещения флажков (используем grid)
        self.check_frame = tk.Frame(self.screen_devices)
        self.check_frame.pack(pady=10)

        # Создаём флажки в сетке 3 колонки
        self.row, self.col = 0, 0
        for option in device_options:
            self.var = tk.BooleanVar()                # создаём переменную
            self.device_vars[option] = self.var            # сохраняем в словарь
            chk = tk.Checkbutton(
                self.check_frame,
                text=option,
                variable=self.var,
                font=('Arial', 11)
            )
            chk.grid(row=self.row, column=self.col, sticky='w', padx=20, pady=8)
            self.col += 1
            if self.col > 2:
                self.col = 0
                self.row += 1

        # Фрейм для кнопок управления
        self.buttons_frame = tk.Frame(self.screen_devices)
        self.buttons_frame.pack(pady=20)

        tk.Button(
            self.buttons_frame,
            text='Назад',
            command=lambda: self.show_frame(self.screen_money),
            width=16
        ).pack(side='left', padx=10)

        tk.Button(
            self.buttons_frame,
            text='Рассчитать',
            command=self.run_parser,  # убрали lambda
            width=16
        ).pack(side='left', padx=10)


        self.show_frame(self.screen_menu)

        self.root.mainloop()

    def run_parser(self):
        """Показывает экран загрузки и запускает парсер в отдельном потоке."""
        # Переключаемся на экран результата с сообщением о загрузке
        self.show_frame(self.screen_result)
        for widget in self.screen_result.winfo_children():
            widget.destroy()
        tk.Label(self.screen_result, text="Идёт поиск, подождите...",
                 font=('Arial', 16, 'bold')).pack(pady=50)

        # Собираем данные из GUI
        area = self.area_var.get()
        money_from = self.money_from_var.get()
        money_to = self.money_to_var.get()
        devices = [opt for opt, var in self.device_vars.items() if var.get()]

        # Запускаем парсер в фоновом потоке
        thread = threading.Thread(
            target=self._parser_thread,
            args=(area, money_from, money_to, devices)
        )
        thread.daemon = True
        thread.start()


    def show_frame(self,frame_to_show):
        for f in (
            self.screen_menu,
            self.screen_area,
            self.screen_money,
            self.screen_devices,
            self.screen_result
        ):
            f.pack_forget()
        frame_to_show.pack(fill='both', expand='true')

    def _parser_thread(self, area, money_from, money_to, devices):
        """Выполняется в отдельном потоке, запускает асинхронный парсер."""
        # Создаём экземпляр парсера и передаём ему данные
        parser = Parser()
        parser.area = area
        # При необходимости можно сохранить бюджет и устройства
        # для последующей фильтрации внутри парсера
        # parser.price_from = money_from
        # parser.price_to = money_to
        # parser.required_devices = devices

        # Запускаем асинхронную функцию в новом цикле событий
        asyncio.run(parser.scrape_with_playwright(ALL_URLS))

        # После завершения парсинга возвращаем результаты в основной поток
        self.root.after(0, self.show_results, parser.all_info_obv)

        asyncio.run(parser.scrape_with_playwright(ALL_URLS))

        # После завершения парсинга возвращаем результаты в основной поток
        self.root.after(0, self.show_results, parser.all_info_obv)


    def go_to_next_step(self,current_frame, next_frame):
        self.show_frame(next_frame)

    def restart(self):
        self.show_frame(self.screen_menu)

    def show_results(self, results):
        """Отображает результаты парсинга на экране screen_result."""
        for widget in self.screen_result.winfo_children():
            widget.destroy()

        if not results:
            tk.Label(self.screen_result, text="Ничего не найдено.",
                     font=('Arial', 14)).pack(pady=20)
        else:
            tk.Label(self.screen_result,
                     text=f"Найдено объявлений: {len(results)}",
                     font=('Arial', 16, 'bold')).pack(pady=20)

            # Контейнер для прокрутки, если объявлений много
            canvas = tk.Canvas(self.screen_result)
            scrollbar = tk.Scrollbar(self.screen_result, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Заполняем результатами
            for i, item in enumerate(results):
                frame_item = tk.Frame(scrollable_frame, relief='solid', borderwidth=1)
                frame_item.pack(fill='x', padx=10, pady=5)

                # Текст с ценой и районом
                info = f"{i + 1}. {item.get('price', 'цена не указана')} – {item.get('area', 'район не указан')}"
                lbl_info = tk.Label(frame_item, text=info, font=('Arial', 10))
                lbl_info.pack(side='left', padx=5)

                # Кнопка-ссылка
                url = item.get('url', '')
                if url:
                    btn_link = tk.Button(
                        frame_item,
                        text="Перейти",
                        font=('Arial', 8),
                        command=lambda u=url: open(u)
                    )
                    btn_link.pack(side='right', padx=5)
                else:
                    tk.Label(frame_item, text="(нет ссылки)", font=('Arial', 8)).pack(side='right', padx=5)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        tk.Button(self.screen_result, text='Начать заново',
                  command=self.restart, width=16).pack(pady=20)

if __name__=="__main__":
    TkinterBase()