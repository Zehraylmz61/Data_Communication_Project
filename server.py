import socket
import random
import time
import algorithms  # Binary visualizer

HOST = '127.0.0.1'
PORT_IN = 6001   # Client 1'den gelen port
PORT_OUT = 6002  # Client 2'ye giden port

# [cite_start]--- ERROR INJECTION FUNCTIONS [cite: 35-52] ---
def error_bit_flip(text):
    if not text: return text
    index = random.randint(0, len(text) - 1)
    char_code = ord(text[index])
    corrupted_char = chr(char_code ^ 1) # Flip 1 bit
    return text[:index] + corrupted_char + text[index+1:]

def error_substitution(text):
    if not text: return text
    index = random.randint(0, len(text) - 1)
    new_char = chr(random.randint(65, 90)) # Random A-Z
    return text[:index] + new_char + text[index+1:]

def error_deletion(text):
    if len(text) < 2: return text
    index = random.randint(0, len(text) - 1)
    return text[:index] + text[index+1:]

def error_insertion(text):
    index = random.randint(0, len(text))
    new_char = chr(random.randint(65, 90))
    return text[:index] + new_char + text[index:]

def error_swap(text):
    if len(text) < 2: return text
    idx = random.randint(0, len(text) - 2)
    return text[:idx] + text[idx+1] + text[idx] + text[idx+2:]

def error_multi_bit_flip(text):
    if not text: return text
    temp_text = error_bit_flip(text)
    return error_bit_flip(temp_text)

def error_burst(text):
    if len(text) < 4: return error_substitution(text)
    start = random.randint(0, len(text) - 3)
    return text[:start] + "XXX" + text[start+3:]

def start_server():
    print("--- SERVER (NOISE SIMULATOR) STARTED ---")
    
    # 1. Setup Client 2 (Receiver) Connection - DÜZELTİLEN KISIM BURASI
    print("Trying to connect to Client 2 (Receiver)...")
    sock_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    connected = False
    while not connected:
        try:
            # Server burada Client 2'yi "ARAYAN" taraftır.
            sock_out.connect((HOST, PORT_OUT)) 
            connected = True
            print("Successfully Connected to Client 2.")
        except ConnectionRefusedError:
            print("Client 2 not found. Retrying in 2 seconds...")
            time.sleep(2)
    
    # Kalan kodda 'conn_out' kullanıldığı için ismi eşitliyoruz
    conn_out = sock_out 

    # 2. Setup Client 1 (Sender) Connection
    # Server burada Client 1'i "BEKLEYEN" taraftır.
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_in.bind((HOST, PORT_IN))
    sock_in.listen(1)
    print("\nWaiting for Client 1 (Sender)...")
    conn_in, _ = sock_in.accept()
    print("Client 1 Connected.")

    print("\n--- SYSTEM READY: LISTENING FOR PACKETS ---\n")

    while True:
        try:
            raw_data = conn_in.recv(4096)
            if not raw_data: break
            
            full_packet = raw_data.decode('utf-8')
            parts = full_packet.split('|')
            if len(parts) != 3:
                conn_out.send(raw_data)
                continue

            original_text = parts[0]
            method = parts[1]
            checksum = parts[2]
            
            orig_binary = algorithms.text_to_binary(original_text)
            
            print("\n" + "="*50)
            print(f"[INCOMING] Data: {original_text} | Method: {method}")
            print(f"[BINARY]       : {orig_binary}")
            print("-" * 50)

            # --- SELECTION MENU (1-9) ---
            print("Select Action:")
            print("1. Bit Flip")
            print("2. Character Substitution")
            print("3. Character Deletion")
            print("4. Character Insertion")
            print("5. Character Swapping")
            print("6. Multiple Bit Flips")
            print("7. Burst Error")
            print("8. NO ERROR (Clean Transmission)")
            print("9. RANDOM ERROR (Surprise Me!)")
            
            user_input = input("Selection (1-9): ")
            
            choice = 0 # Internal code for 'No Error' is 0
            
            # LOGIC MAPPING
            if user_input == '9':
                choice = random.randint(1, 7)
                print(f"-> Randomly Selected Error Type: {choice}")
            
            elif user_input == '8':
                choice = 0 
            
            elif user_input.isdigit() and 1 <= int(user_input) <= 7:
                choice = int(user_input)
            
            else:
                print("Invalid Input! Defaulting to 8 (No Error).")
                choice = 0

            # --- APPLY ERROR ---
            corrupted_text = original_text
            error_name = "NO ERROR"

            if choice == 0:
                error_name = "NONE (Clean Transmission)"
            elif choice == 1:
                error_name = "Bit Flip"
                corrupted_text = error_bit_flip(original_text)
            elif choice == 2:
                error_name = "Character Substitution"
                corrupted_text = error_substitution(original_text)
            elif choice == 3:
                error_name = "Character Deletion"
                corrupted_text = error_deletion(original_text)
            elif choice == 4:
                error_name = "Character Insertion"
                corrupted_text = error_insertion(original_text)
            elif choice == 5:
                error_name = "Character Swapping"
                corrupted_text = error_swap(original_text)
            elif choice == 6:
                error_name = "Multiple Bit Flips"
                corrupted_text = error_multi_bit_flip(original_text)
            elif choice == 7:
                error_name = "Burst Error"
                corrupted_text = error_burst(original_text)

            # --- VISUALIZATION ---
            print(f">>> ACTION: {error_name} <<<")
            
            if choice != 0:
                corr_binary = algorithms.text_to_binary(corrupted_text)
                print(f"Original Text  : {original_text}")
                print(f"Corrupted Text : {corrupted_text}")
                print(f"Orig Binary    : {orig_binary}")
                print(f"Corr Binary    : {corr_binary}")
            else:
                print(">>> Packet forwarded without changes.")

            # Forward Packet
            new_packet = f"{corrupted_text}|{method}|{checksum}"
            conn_out.send(new_packet.encode('utf-8'))
            print("[SENT] Packet forwarded to Client 2.")

        except Exception as e:
            print(f"Server Error: {e}")
            break

    conn_in.close(); sock_in.close(); sock_out.close()

if __name__ == "__main__":
    start_server()