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
RACATY_OUTPUT = 'racatyoutput.txt'


with open('output_link.txt', 'w') as file:
    pass  # Tidak ada isi, hanya membuat file kosong
with open(OUTPUT_FILE, 'w') as file:
    pass  # Tidak ada isi, hanya membuat file kosong


@app.route('/save_links', methods=['POST'])
def save_links():
    links = request.json.get('links', [])
    with open(LINK_FILE, 'w') as f:
        for link in links:
            f.write(link + '\n')  # Tulis setiap link ke file
    return {'status': 'success', 'links': links}, 200  # Kembalikan status dan link yang disimpan


@app.route('/output_link.txt')
def output_link():
    with open('output_link.txt', 'r') as file:
        content = file.read()  # Baca isi file
    return content, 200, {'Content-Type': 'text/plain'}  # Kembalikan isi file dengan status 200



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

    with open(RACATY_OUTPUT, 'w') as racaty_file:
        racaty_file.write('\n'.join(results))

    subprocess.run(['python3', 'racatyproses.py'])


    # Emit event ketika proses selesai
    socketio.emit('process_complete',{'results': results})




@socketio.on('start_process')
def start_process():
    # Mulai proses di thread terpisah
    thread = threading.Thread(target=run_process)
    thread.start()


@socketio.on('start_extract')
def start_extract():
    # Mulai proses extract di thread terpisah
    thread = threading.Thread(target=run_extract_process)
    thread.start()

def run_extract_process():
    # Jalankan pooplink.txt dan ambil outputnya
    process = subprocess.Popen(['python3', 'pooplink.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # Emit output ke client
            socketio.emit('process_output', {'data': output.strip()})

    with open('output_link.txt', 'r') as f:
        results = f.read().splitlines()  # Baca setiap baris

    with open(RACATY_OUTPUT, 'w') as racaty_file:
        racaty_file.write('\n'.join(results))

    subprocess.run(['python3', 'racatyproses.py'])


    # Emit event ketika proses selesai
    socketio.emit('process_complete', {'results': results, 'type': 'extract'})  # Tambahkan type




@socketio.on('dood_extract')
def start_dood_extract():
    # Start the dood extract process in a separate thread
    thread = threading.Thread(target=run_dood_extract_process)
    thread.start()

def run_dood_extract_process():
    # Import the convert_dood function from doodextract.py
    from doodextract import convert_dood

    # Call the convert_dood function and get the results
    results = convert_dood()

    # Emit the results back to the client
    socketio.emit('dood_extract_output', {'results': results})

if __name__ == '__main__':
    socketio.run(app, debug=True)