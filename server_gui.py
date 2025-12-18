import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import random
import time
import algorithms

HOST = '127.0.0.1'
PORT_IN = 6001
PORT_OUT = 6002

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Server: Advanced Noise Simulator")
        self.root.geometry("600x750") # Pencereyi uzattık çünkü seçenekler arttı
        self.root.configure(bg="#2c3e50")
        
        self.pending_data = None
        self.client_socket = None
        
        # --- BAŞLIK ---
        header = tk.Frame(root, bg="#e74c3c", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="🕵️ VERİ YAKALAYICI (SERVER)", font=("Segoe UI", 16, "bold"), bg="#e74c3c", fg="white").pack()
        
        # --- DURUM ---
        self.lbl_status = tk.Label(root, text="DURUM: Veri Bekleniyor...", font=("Consolas", 12, "bold"), bg="#f1c40f", fg="#2c3e50", pady=10)
        self.lbl_status.pack(fill="x")

        # --- YAKALANAN VERİ ---
        frame_data = tk.Frame(root, bg="#2c3e50", pady=10)
        frame_data.pack()
        tk.Label(frame_data, text="YAKALANAN VERİ:", font=("Segoe UI", 10), bg="#2c3e50", fg="white").pack()
        self.lbl_captured = tk.Label(frame_data, text="- yok -", font=("Consolas", 14, "bold"), bg="#34495e", fg="#2ecc71", width=30, pady=5)
        self.lbl_captured.pack()

        # --- HATA SEÇİMİ (Genişletildi) ---
        control_frame = tk.LabelFrame(root, text="Hangi Hatayı Uygulayalım?", font=("Segoe UI", 10, "bold"), bg="#ecf0f1", fg="#333", padx=15, pady=10)
        control_frame.pack(pady=10, padx=20, fill="x")
        
        self.selected_error = tk.IntVar(value=0)
        
        # YENİ LİSTE
        options = [
            ("✅ Dokunma (Temiz Gönder)", 0),
            ("🔀 Single Bit Flip (Tek Bit Çevir)", 1),
            ("🔂 Multiple Bit Flips (Çoklu Bit Çevir)", 6), # YENİ
            ("🔠 Substitution (Harf Değişimi)", 2),
            ("➕ Insertion (Karakter Ekleme)", 4),          # YENİ
            ("❌ Deletion (Karakter Silme)", 3),
            ("🔄 Swapping (Karakter Kaydırma)", 5),        # YENİ
            ("💥 Burst Error (Gürültü Patlaması)", 7)
        ]
        
        # Radyo butonlarını iki sütun halinde dizelim ki sığsın
        for i, (text, val) in enumerate(options):
            r = i // 2
            c = i % 2
            tk.Radiobutton(control_frame, text=text, variable=self.selected_error, value=val, 
                           font=("Segoe UI", 10), bg="#ecf0f1", cursor="hand2").grid(row=r, column=c, sticky="w", padx=10, pady=2)

        # --- BUTON ---
        self.btn_send = tk.Button(root, text="UYGULA VE İLET 🚀", command=self.forward_packet, 
                                  bg="#27ae60", fg="white", font=("Segoe UI", 14, "bold"), state="disabled")
        self.btn_send.pack(pady=10, ipadx=20, ipady=5)

        # --- LOG ---
        self.log_area = scrolledtext.ScrolledText(root, width=65, height=12, font=("Consolas", 9), bg="#34495e", fg="white")
        self.log_area.pack(padx=20, pady=10)

        self.setup_sockets()
        threading.Thread(target=self.wait_for_packet, daemon=True).start()

    def log(self, msg):
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)

    def setup_sockets(self):
        self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            try:
                self.sock_out.connect((HOST, PORT_OUT))
                connected = True
                self.log(">>> Client 2'ye bağlandı.")
            except:
                time.sleep(1)

        self.sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_in.bind((HOST, PORT_IN))
        self.sock_in.listen(1)
        self.log(">>> Sistem Hazır. Client 1 bekleniyor...")

    def wait_for_packet(self):
        while True:
            conn, addr = self.sock_in.accept()
            try:
                data = conn.recv(4096)
                if data:
                    self.pending_data = data.decode('utf-8')
                    self.client_socket = conn 
                    
                    parts = self.pending_data.split('|')
                    if len(parts) >= 1:
                        self.update_ui_captured(parts[0])
                    
                    self.log(f"\n[YAKALANDI] Veri: {parts[0]}")
                    self.root.after(0, lambda: self.btn_send.config(state="normal", bg="#e67e22"))
                    break 
            except Exception as e:
                self.log(f"Hata: {e}")

    def update_ui_captured(self, text):
        self.lbl_captured.config(text=text)
        self.lbl_status.config(text="⚠️ ONAY BEKLENİYOR", bg="#e67e22", fg="white")

    # --- HATA MANTIKLARI BURADA ---
    def apply_error(self, text, choice):
        if not text: return text, "Empty"
        
        # 0: No Error
        if choice == 0: return text, "No Error"
        
        # 1: Single Bit Flip
        if choice == 1: 
             idx = random.randint(0, len(text)-1)
             new_char = chr(ord(text[idx]) ^ 1)
             return text[:idx] + new_char + text[idx+1:], "Single Bit Flip"
        
        # 2: Substitution
        if choice == 2: 
             idx = random.randint(0, len(text)-1)
             return text[:idx] + "X" + text[idx+1:], "Substitution"
        
        # 3: Deletion
        if choice == 3:
             if len(text) < 2: return text, "Deletion Fail"
             idx = random.randint(0, len(text)-1)
             return text[:idx] + text[idx+1:], "Deletion"
             
        # 4: Insertion (YENİ)
        if choice == 4:
            idx = random.randint(0, len(text)) # Başa, sona veya araya
            char = chr(random.randint(65, 90)) # Rastgele A-Z arası harf
            return text[:idx] + char + text[idx:], "Insertion (+1 Char)"
            
        # 5: Swapping (YENİ)
        if choice == 5:
            if len(text) < 2: return text, "Swap Fail (Too Short)"
            idx = random.randint(0, len(text) - 2)
            # idx ile idx+1'in yerini değiştir
            return text[:idx] + text[idx+1] + text[idx] + text[idx+2:], "Swapping"
            
        # 6: Multiple Bit Flips (YENİ)
        if choice == 6:
            # En az 2, en fazla 3 karakterin bitlerini değiştirelim
            count = min(len(text), 3) 
            indices = random.sample(range(len(text)), count) # Rastgele benzersiz indexler
            temp_list = list(text)
            for i in indices:
                temp_list[i] = chr(ord(temp_list[i]) ^ 1) # Her birini flip et
            return "".join(temp_list), "Multi Bit Flip"

        # 7: Burst Error
        if choice == 7:
             return text + "XXX", "Burst Error"
             
        return text, "Unknown"

    def forward_packet(self):
        if not self.pending_data: return
        
        parts = self.pending_data.split('|')
        text = parts[0]
        method = parts[1]
        checksum = parts[2]
        
        # Hata Uygula
        choice = self.selected_error.get()
        corrupted_text, err_name = self.apply_error(text, choice)
        
        new_packet = f"{corrupted_text}|{method}|{checksum}"
        
        try:
            self.sock_out.send(new_packet.encode('utf-8'))
            self.log(f"--> İŞLEM: {err_name}")
            self.log(f"--> GİDEN: {corrupted_text}")
            self.log("-" * 30)
            
            if self.client_socket:
                self.client_socket.close()
                
        except Exception as e:
            self.log(f"Gönderim Hatası: {e}")

        self.lbl_captured.config(text="- gönderildi -")
        self.lbl_status.config(text="DURUM: Yeni Veri Bekleniyor...", bg="#f1c40f", fg="#2c3e50")
        self.btn_send.config(state="disabled", bg="#27ae60")
        self.pending_data = None
        
        threading.Thread(target=self.wait_for_packet, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop()