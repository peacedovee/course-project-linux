import socket
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_graph(equation, x, y, z):
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

def handle_client(conn):
    data = conn.recv(1024).decode()
    equation, x, y, z = data.split(",")
    x, y, z = int(x), int(y), int(z)

    print(f"Получены данные: уравнение={equation}, x={x}, y={y}, z={z}")
    create_graph(equation, x, y, z)

def start_server():
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
