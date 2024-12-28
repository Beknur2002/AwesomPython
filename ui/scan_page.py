import os

def block_process(pid):
    try:
        os.kill(pid, 9)
        print(f" {pid} .")

    except Exception as e:
        print(f" {pid}: {e}")