

import base64
import httpx

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


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
lulustream_api_key = '936yclje4cl5mud6kcw'  # Lulustream API Key
streamhg_api_key = "2426evezy9bm5xz0uzzy"
veev_api_key = "81wfq1eryrdlombkfrej2ldx08p092x1rw"
vinovo_api_key = "8b857a827319ed70f22e4d0668853f"
dropload_api_key = "6228dp9snugc6viw066i"
bigwarp_api_key = "1185roh927m637ogi3lv"
abstream_api_key = "23vj7x7uk12znfyaxc"
doodstream_api_key = "219725bbkborbourrp2cd4"

key = "mysecretkey12345"  # Kunci AES untuk enkripsi
lulustream_api_endpoint = "https://api.lulustream.com/api/upload/url"
streamhg_api_endpoint = "https://streamhgapi.com/api/upload/url"
veev_api_endpoint  = "https://veev.to/api/upload/url"
vinovo_api_endpoint  = "https://api.vinovo.si/api/upload/url"
dropload_endpoint = "https://dropload.io/api/upload/url"
bigwarp_api_endpoint  = "https://bigwarp.io/api/upload/url"
abstream_api_endpoint  = "https://abstream.to/api/upload/url"
doodstream_api_endpoint  = "https://doodapi.com/api/upload/url"


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

        try:
            # doodstream request
            response_doodstream= httpx.get(doodstream_api_endpoint, params={"key": doodstream_api_key, "url": new_url})
            if response_doodstream.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - doodstream Response: {response_doodstream.status_code} - {response_doodstream.text}")
        except Exception as e:
            print(f"Error during Lulustream request for {new_url}: {e}")

        try:
            # Lulustream request
            response_lulustream = httpx.get(lulustream_api_endpoint, params={"key": lulustream_api_key, "url": new_url})
            if response_lulustream.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - Lulustream Response: {response_lulustream.status_code} - {response_lulustream.text}")
        except Exception as e:
            print(f"Error during Lulustream request for {new_url}: {e}")

        
        try:
            # streamhg request
            response_streamhg = httpx.get(streamhg_api_endpoint, params={"key": streamhg_api_key, "url": new_url})
            if response_streamhg.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - StreamHG Response: {response_streamhg.status_code} - {response_streamhg.text}")
        except Exception as e :
            print(f"Error during StreamHG request for {new_url}: {e}")

        try:
            # veev request
            response_veev = httpx.get(veev_api_endpoint, params={"key": veev_api_key, "url": new_url})
            if response_veev.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - Veev Response: {response_veev.status_code} - {response_veev.text}")
        except Exception as e:
            print(f"Error during Veev request for {new_url}: {e}")

        

        try:
            # vinovo request
            response_vinovo = httpx.get(vinovo_api_endpoint, params={"key": vinovo_api_key, "url": url})
            if response_vinovo.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - Vinovo Response: {response_vinovo.status_code} - {response_vinovo.text}")
        except Exception as e:
            print(f"Error during Vinovo request for {url}: {e}")

        try:
            url_to_upload = f"{dropload_endpoint}?key={dropload_api_key}&url={new_url}"

            # dropload request
            response_dropload = httpx.get(url_to_upload)
            if response_dropload.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - Dropload Response: {response_dropload.status_code} - {response_dropload.text}")
        except Exception as e:
            print(f"Error during Vinovo request for {url}: {e}")

        try:
            url_to_upload = f"{bigwarp_api_endpoint}?key={bigwarp_api_key}&url={new_url}"

            # dropload request
            response_bigwarp = httpx.get(url_to_upload)
            if response_bigwarp.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - bigwarp Response: {response_bigwarp.status_code} - {response_bigwarp.text}")
        except Exception as e:
            print(f"Error during Vinovo request for {url}: {e}")

        try:
            url_to_upload = f"{abstream_api_endpoint}?key={abstream_api_key}&url={new_url}"

            # abstream request
            response_abstream = httpx.get(url_to_upload)
            if response_abstream.status_code == 200:
                success_count += 1
            else:
                print(f"Failed: {url} - abstream Response: {response_abstream.status_code} - {response_abstream.text}")
        except Exception as e:
            print(f"Error during abstream request for {url}: {e}")


        print(f"=====> SUCCES UPLOAD KE DropLOAD & Lulustream <============= ")

    # Tampilkan total jumlah sukses
    print("\n=========================================")
    print(f"Total Successful Uploads: {success_count}")
    print("=========================================")

except FileNotFoundError:
    print("The file 'output_link.txt' was not found. Please ensure it exists in the same directory.")