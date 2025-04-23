import numpy as np
import matplotlib.pyplot as plt
import logging
import asyncio
from mpl_toolkits.mplot3d import Axes3D

# Настройка логирования
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def create_graph(equation, x, y, z):
    """Асинхронное построение графика"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _create_graph_sync, equation, x, y, z)

def _create_graph_sync(equation, x, y, z):
    """Синхронная версия построения графика"""
    X = np.linspace(-10, 10, 100)
    Y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(X, Y)

    if equation == "x^2 + z^2 = y":
        Z = X**2 + z**2
    elif equation == "x^2 + y^2 - z^2 = 0":
        Z = X**2 + Y**2 - z**2
    elif equation == "sin(x) + cos(y) = z":
        Z = np.sin(X) + np.cos(Y)
    else:
        raise ValueError("Неизвестное уравнение")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("График уравнения")

    plt.show()  # Теперь график открывается в окне

def parse_message(message):
    """Разбирает сообщение клиента и возвращает параметры."""
    equation, x, y, z = message.split(",")
    return equation, int(x), int(y), int(z)

def log_client_action(client_ip, x, y, z, equation):
    """Записывает действия клиента в журнал."""
    log_message = f"Клиент ({client_ip}) x={x}, y={y}, z={z}, функция={equation}"
    logging.info(log_message)
    print(log_message)