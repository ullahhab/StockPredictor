import tkinter as tk
from tkinter import ttk
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import time
import os
from tkinter import messagebox


class inputUI:
    def __init__(self, root) -> None:
        self.root = root
        self.value = 0
        self.secret = ""
        self.key = ""
        self.dotEnvFileExist = False
        self.populateMoreFields = False
        self.accVal = -1

    # Create the main window
    def startUI(self):
        self.root.title("Bot money start")

        def getAccValue(secret, api):
            try:
                APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
                APCA_API_KEY_ID = api #"PK7L6LK63UD41XRYVRQV"
                APCA_API_SECRET_KEY = secret #"FyMslIcTvjIYm8Mtzcw4NcLglTHbnOsnb3MK8AdF"
                api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)

                account = api.get_account()

                return account.cash
            except Exception as e:
                messagebox.showinfo("Error", e)
                messagebox.showinfo("try again", "Try secrets again")
                return openSecretWindow()
                



        def process_money():
            if not self.dotEnvFileExist:
                saveFile = messagebox.askyesno(title="Save Secrets", message="Would you like to save?")
                if saveFile:
                    file = open(".env", 'w')
                    file.write("APCA_API_KEY_ID="+str(api_entry.get())+"\nAPCA_API_SECRET_KEY="+str(secret_entry.get()))
                    file.close()
                self.secret = secret_entry.get()
                self.key = api_entry.get()
            else:
                file = open(".env", 'r')
                file = file.read().split("\n")
                for value in file:
                    value = value.split("=")
                    if value[0] == "APCA_API_KEY_ID":
                        self.key = value[1]
                    else:
                        self.secret = value[1]
            money_amount = money_entry.get()
            try:
                # Attempt to convert the entered text to a float
                money_amount = float(money_amount)
                accValue = float(getAccValue(self.secret, self.key))
                # Process the money amount (you can replace this with your own logic)
                if accValue >= money_amount:
                    result_label.config(text=f"Money Amount: ${money_amount:.2f} processed successfully")
                    self.value = money_amount
                    self.root.destroy()
                else:
                    result_label.config(
                        text=f"Money Amount: ${money_amount:.2f} is greater than account value Account Value: ${accValue:.2f}")
            except ValueError:
                result_label.config(text="Invalid input. Please enter a valid number.")
        
        def openSecretWindow():
            self.root.withdraw()
            def processSecrets():
                try:
                    APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
                    APCA_API_KEY_ID = api_entry.get() #"PK7L6LK63UD41XRYVRQV"
                    APCA_API_SECRET_KEY = secret_entry.get() #"FyMslIcTvjIYm8Mtzcw4NcLglTHbnOsnb3MK8AdF"
                    api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, base_url=APCA_API_BASE_URL)
                    account = api.get_account()

                    self.key = APCA_API_KEY_ID
                    self.secret = APCA_API_SECRET_KEY
                    saveFile = messagebox.askyesno(title="Save Secrets", message="Would you like to save?")
                    if saveFile:
                        file = open(".env", 'w')
                        file.write("APCA_API_KEY_ID="+str(api_entry.get())+"\nAPCA_API_SECRET_KEY="+str(secret_entry.get()))
                        file.close()
                    secretsWindow.destroy()
                    self.root.deiconify()

                    self.accVal = account.cash
                except Exception as e:
                    messagebox.showinfo("Error", e)
                    self.accVal = -1
                
            
            secretsWindow = tk.Toplevel(self.root)
            secretsWindow.title("Secrets window")
            api_label = ttk.Label(secretsWindow, text="Enter API key:")
            api_label.grid(row=1, column=0, padx=10, pady=10)

            api_entry = ttk.Entry(secretsWindow)
            api_entry.grid(row=1, column=1, padx=10, pady=10)

            secret_label = ttk.Label(secretsWindow, text="Enter secrets:")
            secret_label.grid(row=2, column=0, padx=10, pady=10)

            secret_entry = ttk.Entry(secretsWindow)
            secret_entry.grid(row=2, column=1, padx=10, pady=10)

            submit_button = ttk.Button(secretsWindow, text="submit", command=processSecrets)
            submit_button.grid(row=3, column=0, columnspan=2, pady=10)

            secretsWindow.wait_window()
            return self.accVal


            # Create and place widgets
        if os.path.isfile('.env'):
            self.dotEnvFileExist = True
            money_label = ttk.Label(self.root, text="Enter Money Amount:")
            money_label.grid(row=0, column=0, padx=10, pady=10)

            money_entry = ttk.Entry(self.root)
            money_entry.grid(row=0, column=1, padx=10, pady=10)

            process_button = ttk.Button(self.root, text="Start Bot", command=process_money)
            process_button.grid(row=3, column=0, columnspan=2, pady=10)

            result_label = ttk.Label(self.root, text="")
            result_label.grid(row=4, column=0, columnspan=2, pady=10)
            
        else:
            self.dotEnvFileExist = False
            money_label = ttk.Label(self.root, text="Enter Money Amount:")
            money_label.grid(row=0, column=0, padx=10, pady=10)

            money_entry = ttk.Entry(self.root)
            money_entry.grid(row=0, column=1, padx=10, pady=10)

            api_label = ttk.Label(self.root, text="Enter API key:")
            api_label.grid(row=1, column=0, padx=10, pady=10)

            api_entry = ttk.Entry(self.root)
            api_entry.grid(row=1, column=1, padx=10, pady=10)

            secret_label = ttk.Label(self.root, text="Enter secrets:")
            secret_label.grid(row=2, column=0, padx=10, pady=10)

            secret_entry = ttk.Entry(self.root)
            secret_entry.grid(row=2, column=1, padx=10, pady=10)

            process_button = ttk.Button(self.root, text="Start Bot", command=process_money)
            process_button.grid(row=3, column=0, columnspan=2, pady=10)

            result_label = ttk.Label(self.root, text="")
            result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def getValue(self):
        return self.value

    def getSecret(self):
        return self.key, self.secret




