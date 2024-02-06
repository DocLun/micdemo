import pyaudio
import socket

# Конфигурация клиента
server_ip = '192.168.43.242'
server_port = 8002
chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
sample_rate = 44100

def send_audio():
    # Создаем объект PyAudio
    audio = pyaudio.PyAudio()

    # Открываем поток записи
    stream = audio.open(format=audio_format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    # Создаем сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Устанавливаем соединение с сервером
    client_socket.connect((server_ip, server_port))
    print(f"Установлено соединение с сервером {server_ip}:{server_port}")

    try:
        while True:
            # Читаем аудио данные из потока записи
            audio_data = stream.read(chunk_size)

            # Отправляем аудио данные серверу
            client_socket.sendall(audio_data)

    finally:
        # Закрываем поток записи, сокет и объект PyAudio
        stream.stop_stream()
        stream.close()
        client_socket.close()
        audio.terminate()

send_audio()
