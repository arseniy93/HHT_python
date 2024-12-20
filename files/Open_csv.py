import csv

from numpy.f2py.auxfuncs import throw_error


class Open_csv:
    def __init__(self, file_path):
        """
        Инициализирует объект CSVReader.
        Args:
            file_path (str): Путь к CSV файлу.
        """
        self.file_path = file_path

        self.times_list = list()
        self.amplitude_list = list()
        self.step_by_time = 0.

    def set_path(self, file_path):
        self.file_path = file_path

    def get_path(self):
        return self.file_path

    """
    Класс для чтения CSV файлов.
    """

    def __read_data(self, delimiter=',', quotechar='"'):
        """
        Читает данные из CSV файла.

        Args:
            delimiter (str, optional): Разделитель полей. Defaults to ','.
            quotechar (str, optional): Символ кавычек. Defaults to '"'.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=delimiter, quotechar=quotechar)
                return list(reader)
        except FileNotFoundError:
            print(f"Файл не найден: {self.file_path}")
            self.data = []
            self.header = []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            self.data = []
            self.header = []

    def calculcated_all_lists(self):
        self.__get_list_of_amplitudes()
        self.__get_list_of_times()


    def __get_list_of_amplitudes(self):
        for raw in self.__read_data():
            if raw[0] == "Sample Interval":
                self.step_by_time = float(raw[1])
            self.amplitude_list.append(raw[4])
        self.amplitude_list = list(map(float, self.amplitude_list))
        # return self.amplitude_list

    def __get_list_of_times(self):
        if len(self.amplitude_list) == 0:
            raise Exception("сперва нужно получить амплитуду")
        else:
            for x in range(len(self.amplitude_list) + 1):
                self.times_list.append(x * self.step_by_time)
            return self.times_list.append



    # import tkinter as tk
    # from tkinter import ttk
    #
    #
    # class SignalAnalysisApp(tk.Tk):
    #     def init(self):
    #         super().init()
    #
    #         self.title("Signal Analysis")
    #         self.geometry("1200x800")
    #
    #         # First row of buttons
    #         first_row = tk.Frame(self)
    #         first_row.pack(fill='x', padx=5, pady=5)
    #
    #         buttons1 = [
    #             "Папка -> Загрузить",
    #             "Описание программы",
    #             "Удалить 1",
    #             "Сигнал 1",
    #             "АЧХ 1",
    #             "Сигнал 2",
    #             "АЧХ 2",
    #             "АЧХ 1 + 2"
    #         ]
    #
    #         for text in buttons1:
    #             ttk.Button(first_row, text=text).pack(side='left', padx=2)
    #
    #         # Checkbox
    #         ttk.Checkbutton(first_row, text="Сравнить 2 АЧХ").pack(side='left', padx=2)
    #
    #         # Second row of buttons
    #         second_row = tk.Frame(self)
    #         second_row.pack(fill='x', padx=5, pady=5)
    #
    #         buttons2 = [
    #             "<- Назад",
    #             "Открыть",
    #             "Удалить 2",
    #             "Файл данных сигнал 1",
    #             "Файл данных АЧХ 1",
    #             "Файл данных сигнал 2",
    #             "Файл данных АЧХ 2",
    #             "Удалить графики"
    #         ]
    #
    #         for text in buttons2:
    #             ttk.Button(second_row, text=text).pack(side='left', padx=2)
    #
    #         # Main content area
    #         content = tk.Frame(self)
    #         content.pack(fill='both', expand=True, padx=5, pady=5)
    #
    #         # Left sidebar (Listbox)
    #         sidebar = tk.Frame(content, width=200)
    #         sidebar.pack(side='left', fill='y', padx=(0, 5))
    #
    #         listbox = tk.Listbox(sidebar)
    #         listbox.pack(fill='both', expand=True)
    #         listbox.insert(0, "Список папок, кадров")
    #
    #         # Plots area
    #         plots_frame = tk.Frame(content)
    #         plots_frame.pack(side='left', fill='both', expand=True)
    #
    #         # Create 2x2 grid for plots
    #         for i in range(2):
    #             for j in range(2):
    #                 plot_frame = tk.Frame(
    #                     plots_frame,
    #                     bg='white',
    #                     relief='solid',
    #                     borderwidth=1
    #                 )
    #                 plot_frame.grid(
    #                     row=i,
    #                     column=j,
    #                     sticky='nsew',
    #                     padx=2,
    #                     pady=2
    #                 )
    #
    #                 # Labels for plots
    #                 if i == 0:
    #                     label_text = f"Сигнал {j + 1}"
    #                     y_label = "Амплитуда, В"
    #                     x_label = "Время, с"
    #                 else:
    #                     label_text = f"АЧХ {j + 1}"
    #                     y_label = "Амплитуда, В"
    #                     x_label = "Частота, Гц"
    #
    #                 tk.Label(plot_frame, text=label_text).pack()
    #                 tk.Label(plot_frame, text=y_label).pack(side='left')
    #                 tk.Label(plot_frame, text=x_label).pack(side='bottom')
    #
    #         # Configure grid weights
    #         plots_frame.grid_rowconfigure(0, weight=1)
    #         plots_frame.grid_rowconfigure(1, weight=1)
    #         plots_frame.grid_columnconfigure(0, weight=1)
    #         plots_frame.grid_columnconfigure(1, weight=1)
    #
    #
    # def main():
    #     app = SignalAnalysisApp()
    #     app.mainloop()
    #
    #
    #
    #
    # if __name__ == '__main__':
    #     main()

    # from kivy.app import App
    # from kivy.uix.boxlayout import BoxLayout
    # from kivy.uix.gridlayout import GridLayout
    # from kivy.uix.popup import Popup
    # from kivy.uix.button import Button
    # from kivy.uix.label import Label
    # from kivy.uix.floatlayout import FloatLayout
    # from kivy.uix.recycleview import RecycleView
    # from kivy.uix.recycleboxlayout import RecycleBoxLayout
    # from kivy.uix.recycleview.views import RecycleDataViewBehavior
    # from kivy.properties import BooleanProperty
    # import os
    # import matplotlib.pyplot as plt
    # # from matplotlib.backends.backend_kivyagg import FigureCanvasKivyAgg
    # from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
    #
    # # pip install kivy matplotlib pip install matplotlib[agg]
    #
    #
    # class SelectableRecycleBoxLayout(RecycleBoxLayout):
    #     select_with_touch = BooleanProperty(True)
    #     selected = BooleanProperty(False)
    #     selectable = BooleanProperty(True)
    #
    #
    # class SelectableLabel(RecycleDataViewBehavior, Label):
    #     index = None
    #
    #     def refresh_view_attrs(self, rv, index, data):
    #         self.index = index
    #         return super(SelectableLabel, self).refresh_view_attrs(
    #             rv, index, data)
    #
    #     def on_touch_down(self, touch):
    #         if super(SelectableLabel, self).on_touch_down(touch):
    #             return True
    #         if self.collide_point(*touch.pos) and self.selectable:
    #             return self.parent.select_with_touch
    #
    #
    # class RV(RecycleView):
    #     def __init__(self, **kwargs):
    #         super(RV, self).__init__(**kwargs)
    #         self.data = [{'text': str(fname)} for fname in os.listdir()]
    #
    #
    # class MainMenu(FloatLayout):
    #     def __init__(self, **kwargs):
    #         super().__init__(**kwargs)
    #
    #         # Создаем BoxLayout для размещения элементов
    #         box = BoxLayout(orientation='vertical')
    #
    #         # Меню
    #         menu_layout = GridLayout(cols=1, size_hint_y=None, height=50)
    #         file_menu_btn = Button(text='Файл', size_hint_y=None, height=50)
    #         file_menu_btn.bind(on_press=self.show_file_menu)
    #         menu_layout.add_widget(file_menu_btn)
    #         box.add_widget(menu_layout)
    #
    #         # Основная часть окна
    #         main_layout = BoxLayout(orientation='horizontal')
    #
    #         # Список файлов
    #         self.file_list = RV()
    #         main_layout.add_widget(self.file_list)
    #
    #         # График
    #         self.plot_widget = self.create_plot()
    #         main_layout.add_widget(self.plot_widget)
    #
    #         box.add_widget(main_layout)
    #         self.add_widget(box)
    #
    #     def show_file_menu(self, instance):
    #         content = BoxLayout(orientation='vertical')
    #         open_btn = Button(text='Открыть')
    #         open_btn.bind(on_press=self.open_file)
    #         save_btn = Button(text='Сохранить')
    #         save_btn.bind(on_press=self.save_file)
    #         content.add_widget(open_btn)
    #         content.add_widget(save_btn)
    #
    #         popup = Popup(title='Файл', content=content, size_hint=(0.4, 0.4))
    #         popup.open()
    #
    #     def open_file(self, instance):
    #         # Логика открытия файла
    #         pass
    #
    #     def save_file(self, instance):
    #         # Логика сохранения файла
    #         pass
    #
    #     def create_plot(self):
    #         fig, ax = plt.subplots()
    #         ax.plot([0, 1, 2, 3], [10, 20, 9, 30])
    #         canvas = FigureCanvasKivyAgg(fig)
    #         return canvas
    #
    #
    # class MainApp(App):
    #     def build(self):
    #         return MainMenu()
    #
    #
    # if __name__ == '__main__':
    #     MainApp().run()
