import numpy as np
import matplotlib.pyplot as plt
import logging
import asyncio
import zmq
import zmq.asyncio
from mpl_toolkits.mplot3d import Axes3D
from graph_utils import create_graph, parse_message, log_client_action

# Настройка логирования
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def process_client(socket):
    """Обработка каждого клиента"""
    while True:
        try:
            message = await socket.recv_string()
            equation, x, y, z = parse_message(message)

            log_client_action(socket, x, y, z, equation)

            await create_graph(equation, x, y, z)  # Асинхронное создание графика
            await socket.send_string("График построен!")
        except asyncio.CancelledError:
            print("Остановка обработки клиента.")
            return

async def main():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)  # REP позволяет отвечать клиентам
    socket.bind("tcp://*:5555")

    print("Сервер запущен! Нажмите Ctrl+C для завершения.")
    while True:
        await process_client(socket)  # Обрабатываем каждый клиент асинхронно

asyncio.run(main())