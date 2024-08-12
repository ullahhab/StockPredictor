import threading
import tkinter as tk
import time

def create_window():
    root = tk.Tk()
    root.title("Threaded Tkinter Window")

    label = tk.Label(root, text="This window is created in a thread!")
    label.pack()


    # Simulate some processing in the thread
    for i in range(10):
        label.config(text=f"Processing: {i+1}/10")
        root.update()  # Update the window in the thread (optional)
        time.sleep(1)  # Simulate some wait time

    root.mainloop()


def start_window():
    sellThread = threading.Thread(target=create_window, name="sellThread", args=())

    sellThread.start()
    sellThread.join()


root = tk.Tk()
root.title("Main Thread Control")

start_button = tk.Button(root, text="Start Window", command=start_window)
start_button.pack()

root.mainloop()