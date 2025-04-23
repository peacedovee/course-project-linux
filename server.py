import asyncio
import zmq
import zmq.asyncio
from graph_utils import create_graph, parse_message, log_client_action

async def handle_client(socket):
    while True:
        try:
            message = await socket.recv_string()
            equation, x, y, z = parse_message(message)
            client_ip = socket.getsockopt(zmq.LAST_ENDPOINT)

            log_client_action(client_ip, x, y, z, equation)
            await create_graph(equation, x, y, z)

            await socket.send_string("График построен!")
        except zmq.ZMQError as e:
            print(f"Ошибка сокета: {e}")
            break

async def main():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Сервер запущен! Нажмите Ctrl+C для завершения.")
    try:
        while True:
            await handle_client(socket)
    except KeyboardInterrupt:
        print("\nСервер закрывается...")
        socket.close()
        context.term()

asyncio.run(main())

#sudo apt update
#sudo apt install python3 python3-pip
#pip install pyzmq asyncio matplotlib tkinter

# запуск сервера python3 server.py
# запуск клиента python3 client.py