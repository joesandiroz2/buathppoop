import requests

# Fungsi untuk melakukan penghapusan
def delete_file(file_id):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '_ga=GA1.1.1180926332.1735003220; _ga_3P0P07VSKJ=GS1.1.1738293727.3.1.1738293744.0.0.0; app_session=t8gbheb5i2hup6m9q8a0b0lecru9dkkc',
        'origin': 'https://new.racaty.my.id',
        'priority': 'u=0, i',
        'referer': 'https://new.racaty.my.id/index.php/filme',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = {
        'id': file_id
    }

    response = requests.post('https://new.racaty.my.id/index.php/filme/excluir', headers=headers, data=data)
    return response.status_code, response.text

# Rentang ID yang ingin dihapus
start_id = 5588
end_id = 5544

# Loop melalui setiap ID dalam rentang
for file_id in range(start_id, end_id - 1, -1):  # Loop dari 5588 ke 5544
    print(f"Deleting file with ID: {file_id}")
    
    status_code, response_text = delete_file(file_id)
    
    print(f"Status Code: {status_code}")
    print(f"Response: {response_text}\n")