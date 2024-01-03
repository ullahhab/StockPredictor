import tkinter as tk
from tkinter import ttk
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import time

class inputUI:
    def __init__(self, root) -> None:
        self.root = root
        self.value = 0
    # Create the main window
    def startUI(self):
        self.root.title("Bot money start")

        def getAccValue():
            APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
            APCA_API_KEY_ID = "PKD8V1TQWBUDC69ELWKM"
            APCA_API_SECRET_KEY = "xE1m8nLhVrOPZK1aFmVpSyrouyhWh8iwb9D2XgX8"
            api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)

            account = api.get_account()

            return account.cash


        def process_money():
        # Retrieve the entered money amount from the Entry widget
            money_amount = money_entry.get()

            try:
                # Attempt to convert the entered text to a float
                money_amount = float(money_amount)
                accValue = float(getAccValue())
                # Process the money amount (you can replace this with your own logic)
                if accValue >= money_amount:
                    result_label.config(text=f"Money Amount: ${money_amount:.2f} processed successfully")
                    self.value = money_amount
                    self.root.destroy()
                else:
                    result_label.config(text=f"Money Amount: ${money_amount:.2f} is greater than account value Account Value: ${accValue:.2f}")
            except ValueError:
                result_label.config(text="Invalid input. Please enter a valid number.")


            # Create and place widgets
        money_label = ttk.Label(self.root, text="Enter Money Amount:")
        money_label.grid(row=0, column=0, padx=10, pady=10)

        money_entry = ttk.Entry(self.root)
        money_entry.grid(row=0, column=1, padx=10, pady=10)

        process_button = ttk.Button(self.root, text="Start Bot", command=process_money)
        process_button.grid(row=1, column=0, columnspan=2, pady=10)

        result_label = ttk.Label(self.root, text="")
        result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def getValue(self):
        return self.value
    

    