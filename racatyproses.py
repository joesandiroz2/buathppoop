from urllib.parse import quote,unquote
import subprocess
import uuid
import re
# Fungsi untuk membaca URL dari file
def read_links(file_path):
    with open(file_path, 'r') as file:
        links = file.readlines()
    return [link.strip() for link in links]

def extract_filename(url):
    # Decode URL jika perlu
    decoded_url = unquote(url)
    # Cari pola filename (di antara 'filename="' dan '"')
    match = re.search(r'filename%3D%22([^"]+)"', decoded_url)
    if match:
        return match.group(1)  # Ambil nama file dari query parameter
    else:
        # Jika tidak ada, ambil nama file dari path terakhir
        return decoded_url.split('/')[-1].split('?')[0]



# Fungsi untuk mengupload menggunakan curl
def upload_video(url):
    # Meng-encode URL agar menjadi URL-encoded
    encoded_url = quote(url, safe='')  # Meng-encode seluruh karakter kecuali yang aman
    print(f"Uploading: {encoded_url}")
    filename = extract_filename(url)
    # Menyusun perintah curl
    curl_command = [
        'curl', 'https://new.racaty.my.id/upload/upload',
        '-H', 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        '-H', 'accept-language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        '-H', 'cache-control: max-age=0',
        '-H', 'content-type: application/x-www-form-urlencoded',
        '-H', 'cookie: _ga=GA1.1.1180926332.1735003220; _ga_3P0P07VSKJ=GS1.1.1735003220.1.1.1735003671.0.0.0; app_session=mbnf2k8abn93f7bmrsjs6fc8q0our00s',
        '-H', 'origin: https://new.racaty.my.id',
        '-H', 'priority: u=0, i',
        '-H', 'referer: https://new.racaty.my.id/upload',
        '-H', 'sec-ch-ua: "Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', 'sec-ch-ua-platform: "Linux"',
        '-H', 'sec-fetch-dest: document',
        '-H', 'sec-fetch-mode: navigate',
        '-H', 'sec-fetch-site: same-origin',
        '-H', 'sec-fetch-user: ?1',
        '-H', 'upgrade-insecure-requests: 1',
        '-H', 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        '--data-raw', f'judul={filename}&url={encoded_url}'
    ]
    
    # Menjalankan perintah curl
    subprocess.run(curl_command)

# Main program
if __name__ == "__main__":
    links = read_links('racatyoutput.txt')
    for link in links:
        upload_video(link)