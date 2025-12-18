import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

# import algorithms  <-- BUNU İPTAL ETTİM Kİ HATA VERMESİN

HOST = '127.0.0.1'
PORT = 6002

class ReceiverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TEST PENCERESİ")
        self.root.geometry("500x650")
        
        tk.Label(root, text="BU PENCERE AÇILDI MI?", font=("Arial", 14, "bold"), fg="red").pack(pady=20)
        
        self.log_area = scrolledtext.ScrolledText(root, width=50, height=20)
        self.log_area.pack(padx=10)
        
        self.log_area.insert(tk.END, "Eğer bunu okuyorsan Tkinter çalışıyor demektir.\n")
        self.log_area.insert(tk.END, "Sorun muhtemelen 'algorithms.py' dosyasını bulamamasıydı.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverGUI(root)
    root.mainloop()