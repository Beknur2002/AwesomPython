import subprocess

# Попробуем запустить HTTP сервер с увеличенными параметрами
command = ["python", "-m", "http.server", "8080", "--bind", "127.0.0.1", "--max-header-size", "8192", "--buffer-size", "8192"]

# Запуск процесса
process = subprocess.Popen(command)

# Получение PID запущенного процесса
print(f"Запущен процесс с PID: {process.pid}")
