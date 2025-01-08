import os
import requests
import re
from bs4 import BeautifulSoup
import cloudscraper
from domain_ganti import domain_ganti
def convert_dood():
    results = []
    num_found = 0  # Counter for number of direct links found

    # Membaca URL dari file link.txt
    file_path = 'link.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            urls = file.readlines()  # Membaca semua baris dari file
            print(urls)

        for url in urls:
            # Menghapus whitespace di awal dan akhir
            url = url.strip()
            if url:  # Pastikan URL tidak kosong
                # Ganti domain lama dengan domain baru
                # Asumsi bahwa URL dimulai dengan http:// atau https://
                if url.startswith("http://") or url.startswith("https://"):
                    new_url = domain_ganti + url[url.find('/', url.find('//') + 2):]
                else:
                    new_url = domain_ganti + '/' + url  # Jika tidak ada skema, tambahkan '/'
                results.append(new_url)
                num_found += 1

    else:
        return {"error": "File link.txt tidak ditemukan."}

    scraper = cloudscraper.create_scraper()  # Create a Cloudscraper instance
    print(scraper)
    for url in urls:
        url = url.strip()  # Clean up whitespace around URL
        if not url:
            continue  # Skip empty URLs
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
        }
        try:
            response = scraper.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <script> tags
            script_tags = soup.find_all('script')
            print(script_tags)
            found_id = None
            found_url = None
            found_length_id = None
            iframe_src_final = None  # Initialize iframe_src_final to None

            # Loop through each script tag to find the specified parts
            for script_tag in script_tags:
                script_content = script_tag.text
                
                # Use regular expressions to find the ID next to 'length'
                length_match = re.search(r"'length'\s*,\s*'([^']+)'", script_content)
                
                # Use regular expressions to find the URL 'https://berlagu.com/jembud/' and the ID next to it
                url_match = re.search(r"'https://berlagu\.com/jembud/'\s*,\s*'([^']+)'", script_content)
                
                # Use regular expressions to find the 'poopiframe' value
                poopiframe_match = re.search(r"'poopiframe'\s*,\s*'([^']+)'", script_content)
                if length_match:
                    found_length_id = length_match.group(1)
                    print(f"Found length ID: {found_length_id}")

                if url_match:
                    found_id = url_match.group(1)
                    print(f"Found ID: {found_id}")

                if poopiframe_match:
                    found_url = poopiframe_match.group(1)
                    print(f"Found poopiframe URL: {found_url}")
                
                # If all matches are found, no need to continue looping
                if found_length_id and found_id and found_url:
                    break

            if found_length_id or found_id or found_url:
                # Process found values and prepare data for post request
                post_url = "https://metrolagu.cam/video"
                data = {"poop": found_length_id}
                headers = {"Content-Type": "application/x-www-form-urlencoded"}
                
                post_response = scraper.post(post_url, data=data, headers=headers)
                post_response.raise_for_status()  # Raise an exception for bad responses
    
                iframe_match = re.search(r'<iframe\s+class="pemain"\s+src="([^"]+)"', post_response.text)
                print(f"Iframe Match: {iframe_match}")

                if iframe_match:
                    iframe_src = iframe_match.group(1)
                    print(f"Found iframe source: {iframe_src}")

                    # Scrape the iframe source content
                    iframe_response = scraper.get(iframe_src, headers=headers)
                    iframe_response.raise_for_status()

                    # Parse the final iframe content
                    iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
                    iframe_src_final = iframe_soup.find('iframe', class_='pemain')['src']
                    print(f"Final iframe source: {iframe_src_final}")

                # Only add to results if iframe_src_final was assigned
                results.append({
                    "url": url, 
                    "length_id": found_length_id, 
                    "poopiframe": found_url, 
                    "id": found_id,
                    "iframe_src": iframe_src_final
                })
                num_found += 1

            else:
                print(f"IDs not found in the <script> tags for URL: {url}")

        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")

        except Exception as e:
            print (f"Error processing URL {url}: {str(e)}")

    # Return aggregated results
    print(results)
    return results

convert_dood()