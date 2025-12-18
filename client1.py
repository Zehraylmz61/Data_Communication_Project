import socket
import algorithms
import random

HOST = '127.0.0.1'
PORT = 6001

def start_sender():
    print("--- CLIENT 1 (SENDER NODE) ---")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        print(f"Connected to Server on port {PORT}.")
        
        while True:
            text = input("\n[INPUT] Text to Send (Type 'exit' to quit): ")
            if text.lower() == 'exit': break
            
            print("\n--- SELECT METHOD ---")
            print("1. CRC-16")
            print("2. Parity (Even)")
            print("3. 2D Parity")
            print("4. Hamming Code")
            print("5. Internet Checksum")
            print("6. ALL METHODS (Compare All)")
            print("7. RANDOM METHOD")
            
            choice = input("Select (1-7): ")
            
            # --- HANDLE RANDOM ---
            if choice == '7':
                choice = str(random.randint(1, 5))
                print(f"-> Randomly Selected Method: {choice}")

            method_name = ""
            checksum = ""
            
            # --- CALCULATIONS ---
            if choice == '1':
                method_name = "CRC16"
                checksum = algorithms.calculate_crc16(text)
            elif choice == '2':
                method_name = "Parity"
                checksum = algorithms.calculate_parity(text, 'even')
            elif choice == '3':
                method_name = "2DParity"
                checksum = algorithms.calculate_2d_parity(text)
            elif choice == '4':
                method_name = "Hamming"
                checksum = algorithms.calculate_hamming(text)
            elif choice == '5':
                method_name = "InternetChecksum"
                checksum = algorithms.calculate_internet_checksum(text)
            elif choice == '6':
                method_name = "ALL"
                # Calculate ALL and pack them into the checksum field separated by commas
                c1 = algorithms.calculate_crc16(text)
                c2 = algorithms.calculate_parity(text, 'even')
                c3 = algorithms.calculate_2d_parity(text)
                c4 = algorithms.calculate_hamming(text)
                c5 = algorithms.calculate_internet_checksum(text)
                checksum = f"{c1},{c2},{c3},{c4},{c5}" # Composite Checksum
            else:
                print("Invalid! Defaulting to CRC-16.")
                method_name = "CRC16"
                checksum = algorithms.calculate_crc16(text)

            # --- VISUALIZATION ---
            binary_data = algorithms.text_to_binary(text)
            print("\n" + "="*60)
            print(f"PACKET READY:")
            print(f"Text     : {text}")
            print(f"Method   : {method_name}")
            print(f"Checksum : {checksum}")
            print("="*60)
            
            packet = f"{text}|{method_name}|{checksum}"
            s.send(packet.encode('utf-8'))
            print("-> Packet Sent.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    start_sender()