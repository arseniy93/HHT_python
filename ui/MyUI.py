import tkinter as tk
from sysconfig import get_path
from tkinter import filedialog, messagebox
import os
import matplotlib.pyplot as plt
from guidata.qthelpers import click_on_widget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pathlib

import CSV
from files.Open_csv import Open_csv

# TODO chect put even of mouse in Listboox

class MyUI:
    def __init__(self):

        """Конструктор класса UI."""
        self.root = tk.Tk()
        self.csv_path=""



        self.root.title("Пример UI с меню (Класс)")
        self.root.geometry("800x600")


        self.selected_method = tk.StringVar()
        self.selected_method.set("")

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.method_vars = {
            "Метод ЭДМ + Фурье метод": tk.BooleanVar(),
            "Метод Гильберта-Хуанга": tk.BooleanVar(),
            "Фурье какой-то, дописать": tk.BooleanVar()
        }
        self.current_selected_file = None  # Добавляем переменную для хранения текущего выбранного файла
        # Создаем фрейм для списка
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Создаем список
        self.listbox = tk.Listbox(self.list_frame,  width=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<ButtonRelease-1>", self.on_listbox_click)

        # self.event = tk.Event()
        # self.event.widget = self.listbox
        # self.event.num = 3
        # <ButtonRelease-1>

        # Добавим скроллбар
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Создаем фрейм для остального контента
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Создаем фрейм для графика
        self.plot_frame = tk.Frame(self.content_frame)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Создаем фигуру для графика
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # self.get_path_of_folder("")

        self.path_to_folder=""


        self.create_menu()
        self.menu_of_method()

        # TODO set array of csv files
        self.update_list(["Item 1", "Item 2", "Item 3",
                          "Очень длинный элемент списка, который должен правильно отображаться со скроллбаром",
                          "Item 5", "Item 6", "Item 7", "Item 8", "Item 9", "Item 10", "Item 11"])

    def loop(self):
        self.root.mainloop()

    def get_path(self):
        return self.on_listbox_click(self)

    def on_listbox_click(self,event):
        """
        Обработчик события щелчка по элементу Listbox.
        """
        try:
            # Получаем индекс выбранного элемента
            index = self.listbox.curselection()[0]
            # Получаем значение выбранного элемента
            value = self.listbox.get(index)
            print(f"Выбран элемент: {value} (индекс: {index})")
            # self.csv_path.set_path(self.path_to_folder+value)
            original_path = pathlib.Path(self.path_to_folder+value)
            converted_path = str(original_path).replace('/', '\\').replace('\\', '\\\\')
            print(converted_path)
            print(self.path_to_folder+value)
            return self.path_to_folder+value
        except IndexError:
            # Если ни один элемент не выбран, игнорируем щелчок
            pass

    def eevent(self):
        return self.event.num

    # Возращаем путь к файлам
    def get_selected_file_path(self):
        """Метод для получения пути к выбранному файлу"""
        return self.current_selected_file



    def create_menu(self):
        """Создание меню 'Файл'."""
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)
        # file_menu.add_command(label="Открыть файл", command=self.open_file_by_click)
        file_menu.add_command(label="Открыть папку", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_app)


    #TODO доделать открытие списка csv
    def open_folder(self):
        """Функция для открытия папки с файлами CSV."""
        selected = self.get_selected_method()
        print(f"Открытие папки с использованием: {selected}")
        folder_path = filedialog.askdirectory(
            title="Выберите папку"
        )
        if folder_path:
            try:
                file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if (file.endswith('.csv') or file.endswith('.CSV') )]
                if file_paths:
                    name_of_files = []
                    path=file_paths[0][:-13]+"/"
                    self.path_to_folder =path
                    print(path)
                    # self.get_path_of_folder(path)
                    for file_path in file_paths:
                        name_of_files.append((file_path[-12:]))
                    self.update_list(name_of_files)
                else:
                    messagebox.showinfo("Нет CSV файлов", "В выбранной папке нет файлов с расширением .csv")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть папку:\n{e}")
        else:
            messagebox.showinfo("Отмена", "Открытие папки отменено")

    def exit_app(self):
        """Функция для выхода из приложения."""
        self.root.destroy()

    def menu_of_method(self):
        """Создание меню 'Обработка сигнала'."""
        file_menu_signal = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Обработка сигнала", menu=file_menu_signal)

        for method in self.method_vars.keys():
            file_menu_signal.add_checkbutton(
                label=method,
                variable=self.method_vars[method],
                onvalue=True, offvalue=False,
                command=lambda m=method: self.select_method(m)
            )

    def select_method(self, method):
        """Устанавливает выбранный метод, снимает выделение с других методов и выводит в консоль."""
        for key in self.method_vars:
            self.method_vars[key].set(key == method)
        self.selected_method.set(method)
        print(f"Выбран метод: {method}")
        self.plot_example_graph()  # Пример вызова функции для отображения графика

    def get_selected_method(self):
        """Возвращает выбранный метод."""
        return self.selected_method.get()

    def update_list(self, items):
        """Обновляет список элементов."""
        self.listbox.delete(0, tk.END)  # Очищаем список
        for item in items:
            self.listbox.insert(tk.END, item)

    def plot_example_graph(self):
        """Пример функции для отображения графика."""
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]
        self.ax.clear()
        self.ax.plot(x, y, marker='o')
        self.ax.set_title('Пример графика')
        self.ax.set_xlabel('X ось')
        self.ax.set_ylabel('Y ось')
        self.canvas.draw()


f = MyUI()

# Создаём фиктивный объект event (пример)
mock_event = tk.Event()
mock_event.widget = f.listbox  # Указываем виджет Listbox
mock_event.x = 10  # Пример координаты x
mock_event.y = 20  # Пример координаты y
mock_event.num = 1  # Номер кнопки мыши (1 для левой кнопки)

# Вызываем метод on_listbox_click и сохраняем результат
result = f.on_listbox_click(mock_event)

print("Вывод:")
print(result)  # Выводим результат

f.loop()  # Запускаем главный цикл
#
# if __name__ == "__main__":
#     # root = tk.Tk()
#     app = MyUI()
#     app.loop()
    # root.mainloop()*