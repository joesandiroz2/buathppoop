import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
import re

domain_ganti = "https://poo.phd"  # Replace with your target domain

def scrape_website(url: str) -> list:
    headers = {
        "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

    results = []
    page_number = 1

    # First request to fetch the total number of pages
    response = requests.get(url, headers=headers)

    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to fetch initial page: {response.status_code}")
        return results  # Return empty list instead of None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract total number of pages from the pagination links
    pagination = soup.find('ul', class_='pagination mt-4')
    if pagination:
        last_page_link = pagination.find_all('a', class_='page-link')[-1]  # Get the last link
        max_pages = int(last_page_link.text)  # Extract the page number
    else:
        print("No pagination found. Exiting.")
        return results

    # Start scraping each page
    while page_number <= max_pages:
        # Create the paginated URL
        paginated_url = f"{url}?p={page_number}"  # Adjust based on the pagination structure
        response = requests.get(paginated_url, headers=headers)

        # Check for successful response
        if response.status_code != 200:
            print(f"Failed to fetch page {page_number}: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        videos = soup.find_all('div', class_='col-sm col-md-6 col-lg-4')

        if not videos:
            print(f"No more videos found on page {page_number}. Ending scrape.")
            break  # Exit loop if no videos are found

        # Extract video data
        for video in videos:
            img_src = video.find('img')['src']
            a_href = video.find('a')['href']
            # Add domain from the input URL to the scraped href
            domain = url.split("/")[2]  # Extract domain from input URL
            a_href = f"https://{domain}{a_href}"
            print(a_href)
            title = video.find('a', class_='title_video').strong.get_text()
            results.append({'img_src': img_src, 'a_href': a_href, 'title': title})

        print(f"Scraped page {page_number} successfully.")
        page_number += 1  # Move to the next page

    return results  # Return the list of results

def main():
    # Read URLs from link.txt
    with open('link.txt', 'r', encoding='utf-8') as file:
        urls = file.readlines()

    scraped_content = []
    new_netloc = urlparse(domain_ganti).netloc  # Mengambil netloc dari domain_ganti

    for url in urls:
        url = url.strip()  # Remove any leading/trailing whitespace
        if url:
            # Replace the domain with 'poophd.cc'
            parsed_url = urlparse(url)
            url = urlunparse(parsed_url._replace(netloc=new_netloc))  # Replace the domain
            scraped_result = scrape_website(url)
            scraped_content.extend(scraped_result)

    # Define the file path
    file_path = "output_link.txt"
    # Write only the links to the file
    with open(file_path, "w", encoding="utf-8") as file:
        for item in scraped_content:
            file.write(f"{item['a_href']}\n")

    total_links = len(scraped_content)
    print(f"Total links scraped: {total_links}")



# Lanjut upload========================================================

import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import httpx


try:
    with open('output_link.txt', 'r') as file:
        url1 = file.readlines()
        # Menghilangkan baris kosong dan mengganti domain apapun
        url_mentah = [url.strip().replace(url.split('/')[2], domain_ganti.split('/')[2]) for url in url1 if url.strip()]

    # Menulis kembali URL yang telah diperbarui ke dalam link.txt
    with open('output_link.txt', 'w') as file:
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
        # Menggunakan regex untuk mencari URL dalam fungsi fetchDirectLink
        match = re.search(r'https?://[^\s]+/\w+\.php\?key=[\w\d]+', script_tag.string)
        if match:
            print("Found download link:", match.group(0))
            return match.group(0)  # Mengembalikan URL yang ditemukan
    return None


    # if script_tag:
    #     download_link_start = script_tag.string.find("https://mba.dog/download_hashed.php?key=")
    #     if download_link_start != -1:
    #         download_link_end = script_tag.string.find('"', download_link_start)
    #         if download_link_end != -1:
    #             download_link = script_tag.string[download_link_start:download_link_end]
    #             return download_link
    # return None

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

def exmain():
    try:
        with open('output_link.txt', 'r') as file:
            urls = [convert_url(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        print("The file 'output_link.txt' was not found.")
        return
    except Exception as e:
        print(f"Error reading 'output_link.txt': {e}")
        return

    if not urls:
        print("No URLs found in 'output_link.txt'.")
        return

    total_direct_links = 0  # Counter for total direct links found
    total_errors = 0  # Counter for errors or "not found" cases

    with open('zfinal_hasil.txt', 'w') as output_file:
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
    # Run the main function
    main()
    exmain()
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
    with open('zfinal_hasil.txt', 'r') as file:
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
