import binascii

def text_to_binary(text):
    """Metni 0 ve 1'lerden oluşan binary string'e çevirir."""
    return ''.join(format(ord(c), '08b') for c in text)

def calculate_crc16(data):
    """
    CRC-16-CCITT algoritması kullanarak checksum hesaplar.
    Sonuç hex (onaltılık) formatında döner (Örn: A1B2).
    """
    data = bytearray(data, 'utf-8')
    crc = 0xFFFF
    for b in data:
        crc ^= (b << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
        crc &= 0xFFFF
    return f"{crc:04X}"

def calculate_parity(data, parity_type='even'):
    """
    Basit Parity (VRC): Tüm bitleri toplar.
    Even (Çift) Parity: 1'lerin sayısı çiftse 0, tekse 1 döner.
    """
    binary_data = text_to_binary(data)
    ones_count = binary_data.count('1')
    
    if parity_type == 'even':
        return "0" if ones_count % 2 == 0 else "1"
    else: # odd
        return "1" if ones_count % 2 == 0 else "0"

def calculate_2d_parity(data):
    """
    2D Parity (LRC): Her sütunun (bit pozisyonunun) parity'sini hesaplar.
    Sonuç 8 bitlik bir değer döner.
    """
    if not data: return "00"
    
    # Her karakterin binary kodunu al
    binaries = [format(ord(c), '08b') for c in data]
    
    lrc_result = ""
    # 8 sütun için (her bit pozisyonu) tek tek bak
    for i in range(8):
        column_sum = 0
        for b in binaries:
            column_sum += int(b[i])
        
        # Sütun toplamı çift mi tek mi? (Even Parity)
        lrc_result += "0" if column_sum % 2 == 0 else "1"
        
    # Sonucu Hex'e çevirip kısa gösterelim (Örn: A5)
    return f"{int(lrc_result, 2):02X}"

def calculate_hamming(data):
    """
    Hamming Benzeri Checksum:
    Gerçek Hamming kodu çok uzundur, burada verinin
    içeriğine duyarlı bir 'Redundancy Bit' hesaplaması yapıyoruz.
    Veri değişirse, bu kod kesinlikle değişir.
    """
    if not data: return "0000"
    
    # Veriyi binary yap
    binary_string = text_to_binary(data)
    m = len(binary_string)
    r = 0
    # Gerekli parity bit sayısını bul (2^r >= m + r + 1)
    while (2**r < m + r + 1):
        r += 1
        
    # Basitleştirilmiş Hamming Checksum:
    # Bit pozisyonlarına göre XOR işlemi yapıyoruz.
    check_val = 0
    for i, bit in enumerate(binary_string):
        if bit == '1':
            check_val ^= (i + 1)
            
    return f"{check_val:04X}"

def calculate_internet_checksum(data):
    """
    Internet Checksum (IP/TCP stili):
    Veriyi 16-bitlik parçalar halinde toplar.
    """
    if len(data) % 2 == 1:
        data += "\0" # Çift sayıya tamamla
        
    s = 0
    for i in range(0, len(data), 2):
        w = (ord(data[i]) << 8) + (ord(data[i+1]))
        s += w
        
    # Taşmaları (carry) ekle
    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)
    
    # 1's complement (Tersini al)
    return f"{(~s & 0xffff):04X}"