import requests
import re
from domain_ganti import domain_ganti

# Fungsi untuk melakukan scraping dan mendapatkan link video dari satu halaman
def scrape_links(url):
    response = requests.get(url)
    
    # Memastikan permintaan berhasil
    if response.status_code == 200:
        # Mencari semua link video dalam tag <a>
        matches = re.findall(r'<a href="(/d/[^"]+)"', response.text)
        full_links = {domain_ganti + match for match in matches}  # Menggunakan set untuk menghindari duplikat
        return full_links
    else:
        print(f"Failed to retrieve {url}: {response.status_code}")
        return set()  # Mengembalikan set kosong jika gagal

# Fungsi untuk mendapatkan semua link dari semua halaman
def scrape_all_pages(initial_url):
    all_links = set()
    page_number = 1

    while True:
        # Membuat URL untuk halaman saat ini
        page_url = f"{initial_url}?p={page_number}"
        print(f"Scraping {page_url}...")
        
        # Mengambil link dari halaman saat ini
        video_links = scrape_links(page_url)
        if not video_links:
            break  # Jika tidak ada link, keluar dari loop

        all_links.update(video_links)  # Menambahkan link ke set

        # Cek apakah ada link pagination untuk halaman berikutnya
        response = requests.get(page_url)
        if response.status_code == 200:
            # Mencari link pagination
            pagination_matches = re.findall(r'<a class="page-link" href="(/f/[^"]+\?p=\d+)"', response.text)
            if not pagination_matches or page_number >= len(pagination_matches):
                break  # Jika tidak ada halaman berikutnya, keluar dari loop
        else:
            print(f"Failed to retrieve pagination for {page_url}: {response.status_code}")
            break

        page_number += 1  # Melanjutkan ke halaman berikutnya

    return all_links

# Membaca file folder_link.txt
with open('folder_link.txt', 'r') as file:
    links = file.readlines()

# Menyimpan hasil ke link.txt
with open('link.txt', 'w') as output_file:
    found_links = set()  # Menggunakan set untuk menyimpan link yang ditemukan
    for link in links:
        link = link.strip()
        if link:
            video_links = scrape_all_pages(link)
            found_links.update(video_links)  # Menambahkan link ke set

            # Mencetak hasil ke terminal
            for video_link in video_links:
                print(video_link)

    # Menyimpan semua link yang ditemukan ke file
    for found_link in found_links:
        output_file.write(found_link + '\n')

# Mencetak jumlah link yang ditemukan
print(f'Jumlah link yang ditemukan: {len(found_links)}')