import requests
from urllib.parse import unquote, urlparse, parse_qs

# Fungsi untuk mengekstrak nama file dari URL
def extract_filename_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    if 'response-content-disposition' in query_params:
        disposition = query_params['response-content-disposition'][0]
        if 'filename=' in disposition:
            filename_part = disposition.split('filename=')[1]
            filename = unquote(filename_part.strip('"'))
            return filename
    return None

# Fungsi untuk melakukan curl request
def perform_curl_request(title, url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '_ga=GA1.1.1180926332.1735003220; _ga_3P0P07VSKJ=GS1.1.1738293727.3.1.1738293744.0.0.0; app_session=6tnjs1oa8kq81f6hvtcpgk4p8npe8kkm',
        'origin': 'https://new.racaty.my.id',
        'priority': 'u=0, i',
        'referer': 'https://new.racaty.my.id/upload',
    }

    data = {
        'judul': title,
        'url': url
    }

    response = requests.post('https://new.racaty.my.id/upload/upload', headers=headers, data=data)
    return response.status_code, response.text

# Fungsi utama untuk memproses file output_link.txt
def racaty_upload_slash(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line:  # Pastikan tidak ada baris kosong
            title, url = line.split('/<>/')  # Memisahkan judul dan URL
            title = title.strip()  # Menghapus spasi di sekitar judul
            url = url.strip()  # Menghapus spasi di sekitar URL
            
            status_code, response_text = perform_curl_request(title, url)
            print(f"Racaty Upload --> Status Code: {status_code}")
