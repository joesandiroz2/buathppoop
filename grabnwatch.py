import requests
from bs4 import BeautifulSoup

def grabnwatch_process_links(links):
    results = []
    for link in links:
        print(link)  # For debugging, can be removed if not needed
        try:
            response = requests.post(
                'https://grabnwatch.com/',
                headers={
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'cache-control': 'max-age=0',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://grabnwatch.com',
                    'referer': 'https://grabnwatch.com/',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
                },
                data={'video_url': link}
            )

            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                try:
                    download_link = soup.find('a', class_='btn btn-secondary mb-4')['href']
                    full_link = f'https://grabnwatch.com{download_link}'
                    results.append(full_link)
                except TypeError:
                    print(f"Error: Download link not found for link: {link}")
            else:
                print(f"Error: Received response code {response.status_code} for link: {link}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed for link: {link}. Error: {e}")

    # Write results to output_link.txt
    with open("output_link.txt", "w") as f:
        for result in results:
            f.write(result + "\n")  # Write each result to a new line

    return results