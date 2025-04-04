import tkinter as tk
from tkinter import ttk
import logging

# Настройка журналирования
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Построение графика")
        self.root.geometry("300x400+450+150")
        self.root.configure(bg="#F3E0DC")

        self.default_value = tk.IntVar(value=0)

        # Заголовок
        self.label = tk.Label(root, text="График", bg="#F3E0DC", fg="#BC4639", font=("Arial", 14, "bold"))
        self.label.place(x=100, y=40)

        # Получение значений X, Y, Z
        self.create_numeric_input("X:", 100)
        self.create_numeric_input("Y:", 150)
        self.create_numeric_input("Z:", 200)

        # Выбор уравнения
        self.options = ["x^2 + z^2 = y", "x^2 + y^2 - z^2 = 0", "sin(x) + cos(y) = z"]
        self.combo = ttk.Combobox(root, values=self.options, font=("Arial", 14), width=15)
        self.combo.place(x=50, y=250)
        self.combo.set(self.options[0])

        # Кнопка получения графика
        self.apply_button = tk.Button(root, text="Получить график", bg="#D4A59A", fg="#5C2018",
                                      font=("Arial", 14, "bold"), activebackground="#BC4639",
                                      activeforeground="#F3E0DC", command=self.log_selection)
        self.apply_button.place(x=50, y=300)

    def create_numeric_input(self, label_text, y_position):
        label = tk.Label(self.root, text=label_text, bg="#F3E0DC", fg="#BC4639", font=("Arial", 14, "bold"))
        label.place(x=50, y=y_position)

        spinbox = tk.Spinbox(self.root, from_=-100, to=100, font=("Arial", 14), textvariable=self.default_value, width=13)
        spinbox.place(x=80, y=y_position)

    def log_selection(self):
        selected_equation = self.combo.get()
        logging.info(f"Выбрано уравнение: {selected_equation}")
        print(f"Выбрано уравнение: {selected_equation}")

# Запуск приложения
root = tk.Tk()
app = GraphApp(root)
root.mainloop()
