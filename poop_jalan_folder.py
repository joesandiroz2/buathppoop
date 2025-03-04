import subprocess

# Menjalankan poop_baru.py
print("====== JALAN /f/ FOLDER poop =====\n\n")


print("Menjalankan poop_folder_extract.py...")
proses1 = subprocess.run(["python3", "poop_folder_extract.py"], check=True)


print("Menjalankan poop_baru.py...")
proses1 = subprocess.run(["python3", "poop_baru.py"], check=True)

# Menjalankan remote_upload.py setelah poop_baru.py selesai
print("Menjalankan remote_upload.py...")
proses2 = subprocess.run(["python3", "remote_upload.py"], check=True)

# Print jika kedua script sudah dijalankan
print("Semua script telah /f/  dijalankan!")
