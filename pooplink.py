import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import httpx

domain_ganti = "https://poop.skin"  # Replace with your target domain

try:
    with open('link.txt', 'r') as file:
        url1 = file.readlines()
        # Menghilangkan baris kosong dan mengganti domain apapun
        url_mentah = [url.strip().replace(url.split('/')[2], domain_ganti.split('/')[2]) for url in url1 if url.strip()]

    # Menulis kembali URL yang telah diperbarui ke dalam link.txt
    with open('link.txt', 'w') as file:
        for url in url_mentah:
            file.write(url + '\n')

    print("Domain URLs updated successfully in link.txt.")
except FileNotFoundError:
    print("The file 'link.txt' was not found. Please ensure it exists in the same directory.")
    exit()

import requests
from bs4 import BeautifulSoup
import json
import re

# Define headers for the first request (to the initial URLs)
headers_initial = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=0, i',
    'referer': 'https://metrolagu.cam/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

def convert_url(url):
    match = re.search(r'/[de]/([^/]+)$', url)
    if match:
        video_id = match.group(1)
        base_url = url.split('/d/')[0] if '/d/' in url else url.split('/e/')[0]
        return f"{base_url}/p0?id={video_id}"
    return url

def extract_download_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', string=lambda t: 'fetchDirectLink' in t if t else False)

    if script_tag:
        download_link_start = script_tag.string.find("https://pay.kininews.co/download_hashed.php?key=")
        if download_link_start != -1:
            download_link_end = script_tag.string.find('"', download_link_start)
            if download_link_end != -1:
                download_link = script_tag.string[download_link_start:download_link_end]
                return download_link
    return None

def extract_authorization_token(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', string=lambda t: 'fetchDirectLink' in t if t else False)

    if script_tag:
        # Use regex to find the authorization token
        # match = re.search(r"'Authorization':\s*'Bearer\s*([^']+)'", script_tag.string)
        match = re.search(r"'Authorization':\s*'([^']+)'", script_tag.string)

        if match:
            return match.group(1)  # Return the captured token
    return None


def extract_final_direct_link(download_url, authorization_token):
    print(authorization_token)
    headers_download = {
        'accept': '*/*',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': f'{authorization_token}',
        'content-type': 'application/json',
        'origin': domain_ganti,
        'priority': 'u=1, i',
        'referer': f'{domain_ganti}/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(download_url, headers=headers_download, timeout=10)
        response.raise_for_status()  # Memicu exception untuk status kode 4xx/5xx


        json_data = response.json()
        return json_data.get("direct_link")
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON response from {download_url}")
        return None

def main():
    try:
        with open('link.txt', 'r') as file:
            urls = [convert_url(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        print("The file 'link.txt' was not found.")
        return
    except Exception as e:
        print(f"Error reading 'link.txt': {e}")
        return

    if not urls:
        print("No URLs found in 'link.txt'.")
        return

    total_direct_links = 0  # Counter for total direct links found
    total_errors = 0  # Counter for errors or "not found" cases

    with open('output_link.txt', 'w') as output_file:
        # Process each URL
        for url in urls:
            try:
                response = requests.get(url, headers=headers_initial, timeout=10)
                response.raise_for_status()

                download_url = extract_download_link(response.text)

                if not download_url:
                    print(f"No download.php link found in {url}")
                    total_errors += 1
                    continue

                authorization_token = extract_authorization_token(response.text)
                if not authorization_token:
                    print(f"No authorization token found in {url}")
                    total_errors += 1
                    continue

                final_direct_link = extract_final_direct_link(download_url, authorization_token)
                if final_direct_link:
                    print(f"{final_direct_link}\n")
                    output_file.write(f"{final_direct_link}\n")
                    total_direct_links += 1
                else:
                    print(f"No direct link found in {download_url}")
                    total_errors += 1

            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}\n")
                total_errors += 1
            except Exception as e:
                print(f"An unexpected error occurred while processing {url}: {e}\n")
                total_errors += 1

    print("\n===========================================")
    print(f"Total direct links found: {total_direct_links}")
    print(f"Total not found or errors: {total_errors}")




# Menjalankan main.py
try:
    main()
    print("main.py executed successfully!")

except Exception as e:
    print(f"Failed to run main.py: {e}")
    exit()

# Lanjutkan eksekusi kode
def encrypt_url(url, key):
    # Pastikan kunci adalah 16-byte
    key = key.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)

    # Pad URL menggunakan PKCS7
    padded_url = pad(url.encode('utf-8'), AES.block_size)

    # Enkripsi data
    encrypted = cipher.encrypt(padded_url)

    # Encode hasil enkripsi ke Base64 URL-safe
    encrypted_base64 = base64.urlsafe_b64encode(encrypted).decode('utf-8')
    return encrypted_base64

# API Keys
dood_api_key = '219725bbkborbourrp2cd4'
lulustream_api_key = '936yclje4cl5mud6kcw'  # Lulustream API Key
streamhg_api_key = "32zasu667srtcygcrm"


key = "mysecretkey12345"  # Kunci AES untuk enkripsi
dood_api_endpoint = "https://doodapi.com/api/upload/url"
lulustream_api_endpoint = "https://api.lulustream.com/api/upload/url"

streamhg_api_endpoint = "https://bigwarp.io/api/upload/url"


# Variabel untuk menghitung jumlah sukses
success_count = 0

# Read URLs from output.txt
try:
    with open('output_link.txt', 'r') as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls if url.strip()]  # Remove empty lines and whitespace

    # Encrypt each URL and send GET requests to both APIs
    for url in urls:
        # Enkripsi URL
        encrypted = encrypt_url(url, key)
        new_url = f"https://darenx-upbkafe.hf.space/ex/{encrypted}"

        # Kirim permintaan ke DoodAPI
        try:
            # DoodAPI request
            response_dood = httpx.get(dood_api_endpoint, params={"key": dood_api_key, "url": new_url})
            if response_dood.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {new_url} - DoodAPI Response: {response_dood.status_code} - {response_dood.text}")

            # Lulustream request
            response_lulustream = httpx.get(lulustream_api_endpoint, params={"key": lulustream_api_key, "url": new_url})
            if response_lulustream.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - Lulustream Response: {response_lulustream.status_code} - {response_lulustream.text}")

            # streamhg request
            response_lulustream = httpx.get(streamhg_api_endpoint, params={"key": streamhg_api_key, "url": new_url})
            if response_lulustream.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - earnvids Response: {response_lulustream.status_code} - {response_lulustream.text}")



            print(f"=====> SUCCES UPLOAD KE Doodstream & Lulustream <============= ")

        except Exception as e:
            print(f"Error during request for {new_url}: {e}")

    # Tampilkan total jumlah sukses
    print("\n=========================================")
    print(f"Total Successful Uploads: {success_count}")
    print("=========================================")

except FileNotFoundError:
    print("The file 'output.txt' was not found. Please ensure it exists in the same directory.")
