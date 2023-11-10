from datetime import datetime
#from stockPred import *
import time

def run_bot():
    print("wake_up")



while True:
    current_time = datetime.now().strftime("%H:%M")
    print(datetime.now().strftime("%H:%M"))
    if current_time >= "8:30" and current_time <"15:30":
        run_bot()
    time.sleep(1)
