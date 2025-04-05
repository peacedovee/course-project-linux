import socket
import plotly.graph_objects as go
import numpy as np

def create_graph(equation, x, y, z):
    X = np.linspace(-10, 10, 100)
    Y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(X, Y)

    if equation == "x^2 + z^2 = y":
        Z = X ** 2 + z ** 2
    elif equation == "x^2 + y^2 - z^2 = 0":
        Z = X ** 2 + Y ** 2 - z ** 2
    elif equation == "sin(x) + cos(y) = z":
        Z = np.sin(X) + np.cos(Y)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.write_image("graph.png")

def handle_client(conn):
    data = conn.recv(1024).decode()
    equation, x, y, z = data.split(",")
    x, y, z = int(x), int(y), int(z)

    print(f"Получены данные: уравнение={equation}, x={x}, y={y}, z={z}")
    create_graph(equation, x, y, z)

    with open("graph.png", "rb") as f:
        while chunk := f.read(4096):
            conn.sendall(chunk)

def start_server():
    # Создаём серверный сокет с параметром SO_REUSEADDR
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", 65432))
        server.listen()
        print("Сервер запущен и ожидает подключения...")

        while True:
            try:
                conn, addr = server.accept()
                with conn:
                    print(f"Подключение от {addr}")
                    handle_client(conn)
            except KeyboardInterrupt:
                print("\nСервер завершает работу...")
                break

if __name__ == "__main__":
    start_server()