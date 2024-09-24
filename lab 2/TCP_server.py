import socket

HOST = "127.0.0.1"  # адрес сервера
PORT = 30001  # порт сервера

# создание сокета TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # прявязка к адресу и порту
    s.listen()  # режим ожидания подключения
    print(f"Прослушивание {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"Сервен запущен: {addr}")
        while True:
            data = conn.recv(1024)  # получения данных от клиента
            if not data:
                break
            print(f"Сообщение получено от{addr}: {data.decode()}")
            conn.sendall(data) # отправка полученных данных обратно клиенту
            s.close() # закрытие сокета
            break