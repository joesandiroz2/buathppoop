import subprocess

# Menjalankan poop_baru.py
print("Menjalankan poop_baru.py...")
proses1 = subprocess.run(["python3", "poop_baru.py"], check=True)

# Menjalankan remote_upload.py setelah poop_baru.py selesai
print("Menjalankan remote_upload.py...")
proses2 = subprocess.run(["python3", "remote_upload.py"], check=True)

# Print jika kedua script sudah dijalankan
print("Semua script telah dijalankan!")
