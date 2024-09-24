import socket

HOST = "127.0.0.1"  # адрес сервера
PORT = 30001  # порт сервера
MSG = "my message: привет!"

# создание сокета UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST, PORT))  # подключение к серверу
    s.sendall(MSG.encode())  # отправка сообщения серверу
    data_responce = s.recv(1024) # ответ от сервера
    s.close() # закрытие сокета

print(f"Ответ от сервера: {data_responce.decode()}")