import psutil 
import tkinter as tk 
from tkinter import ttk, messagebox 
import random 
import string 
import pika 
import csv

# Функция для получения списка процессов 
def get_processes(): 
    processes = [] 
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']): 
        try: 
            processes.append(proc.info) 
        except psutil.NoSuchProcess: 
            continue 
    return processes 
 
# Функция для обновления списка процессов 
def update_process_list(): 
    for row in tree.get_children(): 
        tree.delete(row) 
     
    processes = get_processes() 
    found_threat = False 
    for process in processes: 
        pid = process['pid'] 
        name = process['name'] 
        memory = process['memory_info'].rss // (1024 * 1024) if process['memory_info'] else 0 
        tree.insert("", "end", values=(pid, name, f"{memory} MB")) 
         
        # Проверка на угрозу 
        if pid == 255: 
            found_threat = True 
            send_process_to_queue(process) 
 
    if found_threat: 
        show_threat_alert(255) 
     
    # Запускаем следующее обновление через 10 секунд 
    root.after(10000, update_process_list) 
 
# Функция для анализа процессов 
def analyze_processes(): 
    processes = get_processes() 
    suspicious = [] 
    for process in processes: 
        name = process['name'] 
        if any(keyword in (name or "").lower() for keyword in ["malware", "suspicious", "hacktool"]): 
            suspicious.append(name) 
     
    if suspicious: 
        status_label.config(text=f"⚠️ Обнаружено: {', '.join(suspicious)}", fg="red") 
    else: 
        status_label.config(text="✅ Все процессы нормальны.", fg="green") 
     
    # Запускаем следующий анализ через 10 секунд 
    root.after(10000, analyze_processes) 
 
# Функция для отправки процессов в очередь RabbitMQ 
def send_process_to_queue(process): 
    message = str(process) 
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='process_queue')
        channel.basic_publish(exchange='', routing_key='process_queue', body=message)
        connection.close()
    except pika.exceptions.AMQPError as e:
        print(f"Error sending message to RabbitMQ: {e}")
 
# Функция для добавления процесса вручную 
def add_manual_process(): 
    pid = 255 
    name = ''.join(random.choices(string.ascii_letters, k=8))  # Генерируем случайное имя 
    memory = random.randint(50, 200)  # Задаем случайный объем памяти в MB 
    tree.insert("", "end", values=(pid, name, f"{memory} MB")) 
    status_label.config(text=f"Обновление процессов......", fg="green") 
 
    root.after(25000, show_threat_alert(17384)) 
 
     
    # Перезапуск обновления после добавления процесса 
    # update_process_list() 
 
# Функция для отображения предупреждения 
def show_threat_alert(pid): 
    messagebox.showwarning("Угроза обнаружена", f"⚠️ Обнаружен процесс с PID {pid}. Это может быть угроза!") 
    # os.kill(pid, 9) 
 
# Создаем графический интерфейс 
root = tk.Tk() 
root.title("Мониторинг процессов") 
 
# Создаем таблицу для отображения процессов 
columns = ("PID", "Название", "Память (RSS)") 
tree = ttk.Treeview(root, columns=columns, show="headings") 
for col in columns: 
    tree.heading(col, text=col) 
    tree.column(col, width=150) 
 
tree.pack(fill=tk.BOTH, expand=True) 
 
# Добавляем статусную строку 
status_label = tk.Label(root, text="Инициализация...", fg="blue") 
status_label.pack(pady=10) 
 
# Запуск обновления списка процессов и анализа 
update_process_list() 
analyze_processes() 
 
# Запуск добавления процесса вручную через 5 секунд 
root.after(50000, add_manual_process) 
 
# Запускаем главное окно 
root.mainloop()


# # Функция для загрузки хэшей процессов из файла antivirus.csv
# def load_antivirus_hashes(file_path):
#     hashes = set()
#     with open(file_path, mode='r', newline='') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             if row:  # Пропускаем пустые строки
#                 hashes.add(row[0])  # Предполагается, что хэш в первом столбце
#     return hashes