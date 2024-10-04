import tkinter as tk
import threading
import time

# Global variables and stop flag
stop_loop = False
valueRetry = 0
sellList, goodForBuy, last5, money, buySuspended = [], [], [], 0.0, False

# Placeholder for account value function
def accountValue():
    return "100.0"  # Replace with actual logic

# Placeholder for the buy function (receives a lock)
def buy(lock):
    with lock:
        # Simulate buying process
        print("Buying...")

# Placeholder for the sell function (receives a lock)
def sell(lock):
    with lock:
        # Simulate selling process
        print("Selling...")

# Run bot logic, creates buy/sell threads
def run_bot():
    global sellList, goodForBuy, last5, money, buySuspended
    lock = threading.Lock()  # Lock for thread-safe operations

    # Create and start buy and sell threads
    buyThread = threading.Thread(target=buy, name="buyThread", args=(lock,))
    sellThread = threading.Thread(target=sell, name="sellThread", args=(lock,))

    buyThread.start()
    sellThread.start()

    buyThread.join()  # Wait for buyThread to finish
    sellThread.join()  # Wait for sellThread to finish

# The bot loop function
def start_bot_loop():
    global valueRetry, stop_loop
    stop_loop = False  # Reset stop flag when loop starts

    while not stop_loop:
        if float(accountValue()) > 0.0:
            run_bot()  # Run bot in the loop
            valueRetry = 0
        elif valueRetry > 3:
            print("Exceeded retries, stopping loop.")
            break
        else:
            valueRetry += 1

        time.sleep(1)  # Sleep for 60 seconds

    print("Bot loop stopped.")

    # After loop stops, update button states to allow starting again
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Function to run the bot loop in a separate thread
def run_bot_thread():
    start_button.config(state=tk.DISABLED)  # Disable Start Button when bot is running
    stop_button.config(state=tk.NORMAL)  # Enable Stop Button
    bot_thread = threading.Thread(target=start_bot_loop)
    bot_thread.start()

# Function to stop the bot loop
def stop_bot():
    global stop_loop
    stop_loop = True  # Set the flag to stop the loop
    print("Stop signal sent.")
    stop_button.config(state=tk.DISABLED)  # Disable Stop Button
    start_button.config(state=tk.NORMAL)  # Enable Start Button after stopping

# Function to automatically start the bot when the UI is launched
def auto_start():
    run_bot_thread()  # Automatically start the bot

# Create the UI
root = tk.Tk()
root.title("Bot Control")

# Start Button to manually run the bot (disabled initially)
start_button = tk.Button(root, text="Start Bot", state=tk.DISABLED, command=run_bot_thread)
start_button.pack(pady=10)

# Stop Button to stop the bot
stop_button = tk.Button(root, text="Stop Bot", command=stop_bot)
stop_button.pack(pady=10)

# Automatically start the bot when the app runs
root.after(100, auto_start)  # Delay to allow the UI to load before starting the bot

# Start the Tkinter event loop
root.mainloop()
