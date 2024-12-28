import socket
import tkinter as tk
from tkinter import ttk

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))  # Используйте порт 12345
    server.listen(5)
    status_label.config(text="Сервер запущен и ждёт подключений...", fg="blue")
    
    while True:
        conn, addr = server.accept()
        status_label.config(text=f"Подключение от {addr}", fg="green")
        
        while True:
            data = conn.recv(1024)
            if not data:
                break
            process_info = data.decode("utf-8")
            tree.insert("", "end", values=process_info.split(","))
        
        conn.close()
        status_label.config(text="Ожидание нового подключения...", fg="blue")

# Создаем графический интерфейс для сервера
root = tk.Tk()
root.title("Сервер мониторинга процессов")

columns = ("PID", "Название", "Память (RSS)")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill=tk.BOTH, expand=True)

status_label = tk.Label(root, text="Сервер не запущен", fg="red")
status_label.pack(pady=10)

# Запускаем сервер в отдельном потоке
import threading
threading.Thread(target=start_server, daemon=True).start()

root.mainloop()
