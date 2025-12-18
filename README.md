# Data_Communication_Project
->Çalıştırma Sırası

Soketlerin düzgün bağlanması için terminalde şu sırayla çalıştırın:

python client2_gui.py (Alıcı)

python server_gui.py (Gürültü Simülatörü)

python client1_gui.py (Gönderici)

Not: Arayüzsüz çalıştırmak için _gui eki olmayan dosyaları aynı sırayla kullanabilirsiniz.

-> Dosya Yapısı

algorithms.py: Çekirdek algoritmalar (CRC, Parity, Hamming vb.).

client1: Veri paketini hazırlar ve gönderir.

server: Veriyi yolda yakalar ve hata (noise) enjekte eder.

client2: Gelen verinin doğruluğunu kontrol eder.
