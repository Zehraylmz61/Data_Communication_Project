import tkinter as tk
from tkinter import ttk, messagebox
import socket
import algorithms

HOST = '127.0.0.1'
PORT_SERVER = 6001

class SenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Client 1: Sender")
        self.root.geometry("450x480")
        self.root.configure(bg="#e8f8f5")
        
        # Başlık
        tk.Label(root, text="📤 VERİ GÖNDERİCİ", font=("Segoe UI", 16, "bold"), bg="#1abc9c", fg="white", pady=10).pack(fill="x")
        
        # İçerik Alanı
        main_frame = tk.Frame(root, bg="#e8f8f5", padx=20, pady=20)
        main_frame.pack()
        
        # Metin Girişi
        tk.Label(main_frame, text="Gönderilecek Mesaj:", font=("Segoe UI", 11), bg="#e8f8f5").pack(anchor="w")
        self.entry_text = tk.Entry(main_frame, width=30, font=("Segoe UI", 12), borderwidth=2, relief="solid")
        self.entry_text.pack(pady=(5, 20), ipady=5)
        
        # Yöntem Seçimi
        tk.Label(main_frame, text="Hata Denetim Yöntemi:", font=("Segoe UI", 11), bg="#e8f8f5").pack(anchor="w")
        
        # --- BURAYA "InternetChecksum" EKLENDİ ---
        self.combo_method = ttk.Combobox(main_frame, values=["CRC16", "Parity", "2DParity", "Hamming", "InternetChecksum"], state="readonly", font=("Segoe UI", 11))
        self.combo_method.current(0)
        self.combo_method.pack(pady=(5, 30), ipady=2)
        
        # Kocaman Gönder Butonu
        self.btn_send = tk.Button(main_frame, text="PAKETİ GÖNDER 🚀", command=self.send_data, 
                                  bg="#2ecc71", fg="white", font=("Segoe UI", 12, "bold"), 
                                  activebackground="#27ae60", cursor="hand2", relief="flat")
        self.btn_send.pack(fill="x", ipady=10)
        
        # Durum Çubuğu
        self.lbl_status = tk.Label(root, text="Sistem Hazır", bg="#e8f8f5", fg="#7f8c8d", font=("Segoe UI", 9))
        self.lbl_status.pack(side="bottom", pady=10)

    def send_data(self):
        text = self.entry_text.get()
        method = self.combo_method.get()
        
        if not text:
            messagebox.showwarning("Eksik Bilgi", "Lütfen bir mesaj yazın!")
            return

        # Checksum Hesapla
        checksum = "0000"
        if method == "CRC16": checksum = algorithms.calculate_crc16(text)
        elif method == "Parity": checksum = algorithms.calculate_parity(text, 'even')
        elif method == "2DParity": checksum = algorithms.calculate_2d_parity(text)
        elif method == "Hamming": checksum = algorithms.calculate_hamming(text)
        # --- YENİ YÖNTEM EKLENDİ ---
        elif method == "InternetChecksum": checksum = algorithms.calculate_internet_checksum(text)

        packet = f"{text}|{method}|{checksum}"
        
        self.lbl_status.config(text="Sunucuya bağlanılıyor...", fg="orange")
        self.root.update()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((HOST, PORT_SERVER))
                s.sendall(packet.encode('utf-8'))
                
            self.lbl_status.config(text=f"✅ Server'a İletildi: '{text}'", fg="#27ae60")
            self.entry_text.delete(0, tk.END) 
            
        except ConnectionRefusedError:
             self.lbl_status.config(text="⛔ Server Meşgul veya Kapalı!", fg="red")
             messagebox.showerror("Hata", "Server şu an yanıt vermiyor.\n\nServer'daki butona basarak önceki işlemi tamamladın mı?")
        except socket.timeout:
             self.lbl_status.config(text="⛔ Zaman Aşımı!", fg="red")
             messagebox.showwarning("Uyarı", "Server cevap vermedi.")
        except Exception as e:
            self.lbl_status.config(text=f"❌ HATA: {e}", fg="#e74c3c")

if __name__ == "__main__":
    root = tk.Tk()
    app = SenderGUI(root)
    root.mainloop()