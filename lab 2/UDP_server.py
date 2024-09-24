import socket

HOST = "127.0.0.1"  # адрес сервера
PORT = 30001  # порт сервера

# создание сокета UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))  # прявязка к адресу и порту
    print(f"Прослушивание {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(1024)  # получения данных от клиента
        if not data:
            break
        print(f"Сообщение получено от {addr}: {data.decode()}")
        s.sendto(data, addr)  # отправка полученных данных обратно клиенту
        s.close() # закрытие сокета
        break