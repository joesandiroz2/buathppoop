from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess
import threading
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)  # Inisialisasi SocketIO

# Nama file untuk menyimpan data
LINK_FILE = 'link.txt'
OUTPUT_FILE = 'zfinal_hasil.txt'


with open('output_link.txt', 'w') as file:
    pass  # Tidak ada isi, hanya membuat file kosong
with open(OUTPUT_FILE, 'w') as file:
    pass  # Tidak ada isi, hanya membuat file kosong

@app.route('/', methods=['GET', 'POST'])
def index():
    preview_links = []
    output_process = ""

    # Cek apakah file link.txt ada dan baca isinya
    if os.path.exists(LINK_FILE):
        with open(LINK_FILE, 'r') as f:
            preview_links = f.read().splitlines()  # Baca semua baris dan pisahkan

    if request.method == 'POST':
        if 'link_data' in request.form:
            # Ambil data dari textarea
            link_data = request.form['link_data']
            
            # Hapus isi file jika sudah ada, kemudian tulis data baru
            with open(LINK_FILE, 'w') as f:
                f.write(link_data + '\n')  # Simpan data ke file
            
            # Ambil link yang baru disimpan untuk ditampilkan sebagai preview
            preview_links = link_data.splitlines()  # Pisahkan berdasarkan baris
            
            return render_template('index.html', preview_links=preview_links, output_process=output_process)

    return render_template('index.html', preview_links=preview_links, output_process=output_process)

def run_process():
    # Jalankan proses.py dan ambil outputnya
    process = subprocess.Popen(['python3', 'proses.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(process)
    while True:
        output = process.stdout.readline()
        print(output.strip())

        if output == '' and process.poll() is not None:
            break
        if output:
            # Emit output ke client
            socketio.emit('process_output', {'data': output.strip()})
    
    with open(OUTPUT_FILE, 'r') as f:
        results = f.read().splitlines()  # Baca setiap baris


    # Emit event ketika proses selesai
    socketio.emit('process_complete',{'results': results})

@socketio.on('start_process')
def start_process():
    # Mulai proses di thread terpisah
    thread = threading.Thread(target=run_process)
    thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True)