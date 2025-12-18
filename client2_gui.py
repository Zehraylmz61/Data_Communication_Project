import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import algorithms 

HOST = '127.0.0.1'
PORT = 6002

class ReceiverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Client 2: Receiver (Alıcı)")
        self.root.geometry("520x680")
        self.root.configure(bg="#ecf0f1")
        
        # Başlık
        header_frame = tk.Frame(root, bg="#2c3e50", pady=15)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="📥 GELEN VERİ AKIŞI", font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="white").pack()
        
        # Log Ekranı
        log_frame = tk.Frame(root, bg="#ecf0f1", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, width=60, height=35, font=("Consolas", 10), bg="#1e1e1e", fg="#00ff00")
        self.log_area.pack(fill="both", expand=True)
        
        tk.Label(root, text="Sistem Dinleniyor...", bg="#ecf0f1", fg="#7f8c8d", font=("Segoe UI", 8)).pack(pady=5)
        
        threading.Thread(target=self.start_listening, daemon=True).start()

    def start_listening(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((HOST, PORT))
            s.listen()
            self.log_msg(">>> SİSTEM BAŞLATILDI. SERVER BEKLENİYOR...")
            
            while True:
                conn, addr = s.accept()
                while True:
                    data = conn.recv(4096)
                    if not data: break
                    self.process_packet(data.decode('utf-8'))
                conn.close()
        except Exception as e:
            self.log_msg(f"Hata: {e}")

    def process_packet(self, full_packet):
        parts = full_packet.split('|')
        if len(parts) != 3: return

        received_text = parts[0]
        method = parts[1]
        received_checksum = parts[2]
        
        # Hesaplama
        calc_checksum = "HATA"
        if method == "CRC16": calc_checksum = algorithms.calculate_crc16(received_text)
        elif method == "Parity": calc_checksum = algorithms.calculate_parity(received_text, 'even')
        elif method == "2DParity": calc_checksum = algorithms.calculate_2d_parity(received_text)
        elif method == "Hamming": calc_checksum = algorithms.calculate_hamming(received_text)
        # --- YENİ YÖNTEM EKLENDİ ---
        elif method == "InternetChecksum": calc_checksum = algorithms.calculate_internet_checksum(received_text)
        
        status = "DATA CORRECT" if received_checksum == calc_checksum else "DATA CORRUPTED"
        
        # Ekrana Yazdır
        msg = f"""
{'-'*45}
Received Data       : {received_text}
Method              : {method}
Sent Check Bits     : {received_checksum}
Computed Check Bits : {calc_checksum}
STATUS              : {status}
{'-'*45}
"""
        self.log_msg(msg)

    def log_msg(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ReceiverGUI(root)
    root.mainloop()