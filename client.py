import tkinter as tk
from tkinter import ttk
import asyncio
import zmq
import zmq.asyncio

class GraphAppClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Клиент брокера сообщений")
        self.root.geometry("300x400+450+150")
        self.root.configure(bg="#F3E0DC")

        self.default_value_x = tk.IntVar(value=0)
        self.default_value_y = tk.IntVar(value=0)
        self.default_value_z = tk.IntVar(value=0)

        tk.Label(root, text="График", bg="#F3E0DC", fg="#BC4639", font=("Arial", 14, "bold")).place(x=100, y=40)

        self.create_numeric_input("X:", 100, self.default_value_x)
        self.create_numeric_input("Y:", 150, self.default_value_y)
        self.create_numeric_input("Z:", 200, self.default_value_z)

        self.options = ["x^2 + z^2 = y", "x^2 + y^2 - z^2 = 0", "sin(x) + cos(y) = z"]
        self.combo = ttk.Combobox(root, values=self.options, font=("Arial", 14), width=15)
        self.combo.place(x=50, y=250)
        self.combo.set(self.options[0])

        self.apply_button = tk.Button(root, text="Отправить данные", bg="#D4A59A", fg="#5C2018",
                                      font=("Arial", 14, "bold"), activebackground="#BC4639",
                                      activeforeground="#F3E0DC", command=self.send_data)
        self.apply_button.place(x=50, y=300)

    def create_numeric_input(self, label_text, y_position, variable):
        tk.Label(self.root, text=label_text, bg="#F3E0DC", fg="#BC4639", font=("Arial", 14, "bold")).place(x=50, y=y_position)
        tk.Spinbox(self.root, from_=-100, to=100, font=("Arial", 14), textvariable=variable, width=13).place(x=80, y=y_position)

    async def async_send_data(self):
        context = zmq.asyncio.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")

        data = f"{self.combo.get()},{self.default_value_x.get()},{self.default_value_y.get()},{self.default_value_z.get()}"
        await socket.send_string(data)
        reply = await socket.recv_string()
        print(f"Ответ от сервера: {reply}")

    def send_data(self):
        asyncio.run(self.async_send_data())

root = tk.Tk()
app = GraphAppClient(root)
root.mainloop()