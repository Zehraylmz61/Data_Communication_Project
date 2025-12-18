import socket
import algorithms  # algorithms.py dosyanın aynı klasörde olduğundan emin ol

HOST = '127.0.0.1'
PORT = 6002  

def start_receiver():
    print("--- CLIENT 2 (RECEIVER) LISTENING ---")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bağlantı bekleme modu (Bind & Listen)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Listening on {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            # print(f"Connection from: {addr}") # İstersen bu satırı silebilirsin, ekranı temiz tutar.
            
            while True:
                data = conn.recv(4096)
                if not data: break
                
                full_packet = data.decode('utf-8')
                parts = full_packet.split('|')
                
                if len(parts) != 3: continue

                received_text = parts[0]
                method = parts[1]
                received_checksum = parts[2]
                
                # --- HESAPLAMA KISMI ---
                calc_checksum = "CALC_ERROR"
                
                if method == "CRC16": 
                    calc_checksum = algorithms.calculate_crc16(received_text)
                elif method == "Parity": 
                    calc_checksum = algorithms.calculate_parity(received_text, 'even')
                elif method == "2DParity": 
                    calc_checksum = algorithms.calculate_2d_parity(received_text)
                elif method == "Hamming": 
                    calc_checksum = algorithms.calculate_hamming(received_text)
                elif method == "InternetChecksum": # PDF'de bu opsiyonel ama kodda varsa kalsın
                    calc_checksum = algorithms.calculate_internet_checksum(received_text)
                
                # --- EKRAN ÇIKTISI (İSTEDİĞİN FORMAT) ---
                print("\n" + "-"*30)
                print(f"Received Data       : {received_text}")
                print(f"Method              : {method}")
                print(f"Sent Check Bits     : {received_checksum}")
                print(f"Computed Check Bits : {calc_checksum}")
                
                if received_checksum == calc_checksum:
                    print("Status              : DATA CORRECT")
                else:
                    print("Status              : DATA CORRUPTED")
                print("-" * 30 + "\n")
            
            conn.close()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    start_receiver()