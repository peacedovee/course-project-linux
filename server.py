import asyncio
import zmq
import zmq.asyncio
import numpy as np
import matplotlib.pyplot as plt
import logging
from mpl_toolkits.mplot3d import Axes3D

# Настройка логирования
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def create_graph(equation, x, y, z):
    X = np.linspace(-10, 10, 100)
    Y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(X, Y)

    if equation == "x^2 + z^2 = y":
        Z = X**2 + z**2
    elif equation == "x^2 + y^2 - z^2 = 0":
        Z = X**2 + Y**2 - z**2
    elif equation == "sin(x) + cos(y) = z":
        Z = np.sin(X) + np.cos(Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("График уравнения")

    plt.show()

async def handle_client(socket):
    while True:
        try:
            message = await socket.recv_string()
            equation, x, y, z = message.split(",")
            x, y, z = int(x), int(y), int(z)
            client_ip = socket.getsockopt(zmq.LAST_ENDPOINT)

            log_message = f"Клиент ({client_ip}) x={x}, y={y}, z={z}, функция={equation}"
            logging.info(log_message)
            print(log_message)

            await create_graph(equation, x, y, z)
            await socket.send_string("График построен!")

        except zmq.ZMQError as e:
            logging.error(f"Ошибка сокета: {e}")
            print(f"Ошибка сокета: {e}")
            break

async def main():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    logging.info("Сервер запущен! Нажмите Ctrl+C для завершения.")
    print("Сервер запущен! Нажмите Ctrl+C для завершения.")

    try:
        while True:
            await handle_client(socket)
    except KeyboardInterrupt:
        logging.info("Сервер закрывается...")
        print("\nСервер закрывается...")
        socket.close()
        context.term()

asyncio.run(main())

#sudo apt update
#sudo apt install python3 python3-pip
#pip install pyzmq asyncio matplotlib tkinter

# запуск сервера python3 server.py
# запуск клиента python3 client.py