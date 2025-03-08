import requests
import re
from domain_ganti import domain_ganti
import subprocess

# Mengosongkan file output_link.txt
open('output_link.txt', 'w').close()

# Fungsi untuk mendapatkan link dari URL
def get_video_link(url):
    try:
        # Mengambil ID dari URL
        video_id = url.split('/')[-1]
        # api_url = f'{domain_ganti}/p0?id={video_id}'
        api_url = f'https://api.poophd.com/player.php?id={video_id}'
        
        headers = {
            'Referer': 'https://metrolagu.cam/',
            'Upgrade-Insecure-Requests': '1',
            'User -Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        # Melakukan permintaan GET
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Memicu kesalahan untuk status kode 4xx/5xx
        
        # Mencari link video dalam respons
        match = re.search(r'player\("a", ".*?", "l", "(.*?)"\);', response.text)
        if match:
            video_link = match.group(1)
            return video_link
    except Exception as e:
        print(f"Error in get_video_link: {e}")
    return None

# Fungsi untuk mengikuti redirect dan mendapatkan link akhir
def follow_redirect(video_link):
    try:
        headers = {
            'accept': '*/*',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'i',
            'range': 'bytes=0-',
            'referer': f'{domain_ganti}/',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'video',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        }

        # Mengikuti redirect
        response = requests.get(video_link, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Memicu kesalahan untuk status kode 4xx/5xx
        
        # Mengambil URL akhir dari header Location jika ada
        if response.history:
            final_url = response.history[-1].headers.get('Location')
            return final_url
    except Exception as e:
        print(f"Error in follow_redirect: {e}")
    return None

# Membaca file link.txt
try:
    with open('link.txt', 'r') as file:
        links = file.readlines()
except Exception as e:
    print(f"Error reading link.txt: {e}")
    links = []

# Menyimpan hasil ke output_link.txt
try:
    total_links = len(links)  # Total link untuk ditampilkan
    with open('output_link.txt', 'w') as output_file:
        found_links = []
        for index, link in enumerate(links):
            link = link.strip()
            if link:
                print(f"Proses {index + 1} dari {total_links}")  # Menampilkan proses link
                video_link = get_video_link(link)
                if video_link:
                    final_link = follow_redirect(video_link)
                    if final_link:
                        output_file.write(final_link + '\n')
                        print(f"{final_link}\n")
                        found_links.append(final_link)

    # Mencetak jumlah link yang ditemukan
    print(f'Jumlah link yang ditemukan: {len(found_links)}')
except Exception as e:
    print(f"Error writing to output_link.txt: {e}")