from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
import subprocess
import threading
from flask_socketio import SocketIO, emit
from racaty_upload_by_slash_title import racaty_upload_slash
from scrape_jav.javeve.main import scrape_javeve,fetch_redirect_url
from grabnwatch import grabnwatch_process_links


app = Flask(__name__)


from flask_socketio import SocketIO

socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/grabnwatch", methods=["POST"])
def handle_grabnwatch():
    links = request.json.get("links", [])
    
    # Menulis link ke file link.txt
    with open("link.txt", "w") as f:
        for link in links:
            f.write(link + "\n")

    # Memanggil fungsi dari grabnwatch.py
    results = grabnwatch_process_links(links)
    print(results)
    # Menulis hasil ke output_link.txt
    with open("output_link.txt", "w") as f:
        for result in results:
            f.write(result + "\n")  # Menulis setiap hasil ke baris baru

    # Menjalankan grabnwatch_remote_upload.py setelah proses selesai
    try:
        subprocess.run(["python3", "grabnwatch_remote_upload.py"], check=True)
        socketio.emit("script_output", {"output": "\n".join(results)})
        print("grabnwatch_remote_upload.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing grabnwatch_remote_upload.py: {e}")
        socketio.emit("script_output", {"output": "\n".join(results)})


    return jsonify({"results": results})

   

@app.route("/poopbaru", methods=["GET", "POST"])
def poopbaru():
    return render_template("poopbaru.html")

@app.route("/get_output", methods=["GET"])
def get_output():
    try:
        with open('output_link.txt', 'r') as f:
            content = f.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)})

@socketio.on("run_script")
def handle_run_script(data):
    links = data.get("links", "").strip()
    script_type = data.get("script_type", "").strip()

    if not script_type:
        socketio.emit("script_output", {"output": "Error: script_type is required!"})
        return
    if not links:
        socketio.emit("script_output", {"output": "Error: Links cannot be empty!"})
        return

    if script_type == "d":
        with open("link.txt", "w") as f:
            f.write(links)
        script_file = "poop_jalan.py"
    elif script_type == "f":
        with open("folder_link.txt", "w") as f:
            f.write(links)
        script_file = "poop_jalan_folder.py"
    else:
        socketio.emit("script_output", {"output": "Error: Invalid script_type!"})
        return

    # Jalankan script dengan output realtime
    process = subprocess.Popen(
        ["python3", script_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        socketio.emit("script_output", {"output": line.strip()})

    for line in process.stderr:
        socketio.emit("script_output", {"output": f"Error: {line.strip()}"})

    socketio.emit("script_done", {"message": "Proses selesai!"})


def write_links_to_file(output_file_path,final_results):

    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'a') as file:  # Open the file in append mode
        for title, urls in final_results.items():
            for url in urls:
                file.write(f"{url}\n")  # Write each URL on a new line

@app.route("/read_output", methods=['GET'])
def read_output():
    # Get the path from the query parameters
    output_file_path = request.args.get('path', default='scrape_jav/javeve/output_javeve.txt', type=str)
    
    # Ensure the path is safe (you can implement more robust checks as needed)
    if not output_file_path.startswith('scrape_jav/javeve/'):
        return "Invalid file path.", 400

    # Check if the file exists and read its contents
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r') as file:
            content = file.read()
    else:
        content = "File not found."

    return content

@app.route("/scrape/javeve", methods=['GET', 'POST'])
def scrapejaveve():
    final_results = {}
    page = 1  # Default page number
    search = ""  # Default search term

    if request.method == 'POST':
        page = request.form.get('page', default=1, type=int)  # Get the page number from the form
        search = request.form.get('search', default="", type=str)  # Get the search term from the form
        scraped_data = scrape_javeve(page, search)
        
        if scraped_data:
            for item in scraped_data:
                additional_data = item['additional_data']
                if additional_data:
                    for title, data_link in additional_data.items():
                        redirect_url = fetch_redirect_url(data_link)
                        if redirect_url:
                            # If the title is already in final_results, append the URL
                            if title in final_results:
                                final_results[title].append(redirect_url)
                            else:
                                # Otherwise, create a new list with the URL
                                final_results[title] = [redirect_url]

            # Write the links to the output file
            write_links_to_file("scrape_jav/javeve/output_javeve.txt",final_results)

    return render_template("/jav/javeve/index.html", data=final_results, page=page, search=search)


# socketio = SocketIO(app)  # Inisialisasi SocketIO

# Nama file untuk menyimpan data
LINK_FILE = 'link.txt'
OUTPUT_FILE = 'zfinal_hasil.txt'
RACATY_LINK_FILE = 'racaty_link.txt'


with open('output_link.txt', 'w') as file:
    pass  # Tidak ada isi, hanya membuat file kosong
with open(OUTPUT_FILE, 'w') as file:
    pass  # Tidak ada isi, hanya membuat file kosong


@app.route('/save_racaty_links', methods=['POST'])
def save_racaty_links():
    links = request.json.get('links', [])
    overwrite = request.json.get('overwrite', False)

    try:
        # Kosongkan file terlebih dahulu
        with open(RACATY_LINK_FILE, "w") as f:
            f.truncate(0)  # Mengosongkan file

        # Tulis data baru ke file
        with open(RACATY_LINK_FILE, "a") as f:  # Gunakan mode append untuk menulis data baru
            for link in links:
                if link.strip():  # Hanya simpan link yang tidak kosong
                    # Misalkan format link adalah "Judul - DoodStream/<>/URL"
                    # Ambil judul dan URL dari link
                    parts = link.split('/<>/')
                    if len(parts) == 2:  # Pastikan ada dua bagian
                        title = parts[0].strip()  # Ambil judul
                        url = parts[1].strip()  # Ambil URL
                        f.write(f"{title}/<>/{url}\n")  # Tulis judul dan link ke file
                        print(f"{title} - {url}")
                    else:
                        print(f"Format tidak valid untuk link: {link}")

        racaty_upload_slash(RACATY_LINK_FILE)
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

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

@app.route('/zfinal_hasil.txt')
def output_zfinal():
    with open('zfinal_hasil.txt', 'r') as file:
        content = file.read()  # Baca isi file
        print(content)
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