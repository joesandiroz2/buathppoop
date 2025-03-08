from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def grabnwatch_process_links(links):
    results = []
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Menjalankan browser di background
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Inisialisasi driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    total_links = len(links)  # Total jumlah link yang akan diproses

    for index, link in enumerate(links):
        print(f"Processing {index + 1} dari {total_links}: {link}")  # Menampilkan proses
        driver.get('https://grabnwatch.com/')
        time.sleep(2)  # Tunggu beberapa detik agar halaman sepenuhnya dimuat

        # Temukan kotak input dan masukkan link
        input_box = driver.find_element(By.NAME, 'video_url')
        input_box.clear()
        input_box.send_keys(link)

        # Klik tombol grab
        grab_button = driver.find_element(By.XPATH, '//button[contains(text(), "Grab")]')
        grab_button.click()
        time.sleep(5)  # Tunggu beberapa detik untuk mendapatkan hasil

        # Ambil link download
        try:
            download_link = driver.find_element(By.CLASS_NAME, 'btn-secondary').get_attribute('href')
            print(download_link)
            results.append(download_link)
        except Exception as e:
            print(f"Error: Download link not found for link: {link}. Error: {e}")

    driver.quit()

    # Write results to output_link.txt
    with open("output_link.txt", "w") as f:
        for result in results:
            f.write(result + "\n")  # Write each result to a new line

    return results

