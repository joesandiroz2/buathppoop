import cloudscraper
from bs4 import BeautifulSoup

def scrape_javeve(page=1, search=None):
    # Construct the URL based on the search term and page number
    if search:
        url = f"https://darenx-unblockjapan.hf.space/proxy/https://javeve.tv/page/{page}/?s={search}"
    else:
        url = f"https://darenx-unblockjapan.hf.space/proxy/https://javeve.tv/censored-jav/page/{page}/"

    print(f"Scraping URL: {url}")
    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except Exception as e:
        print(f"Failed to access the main page: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', class_='post')

        results = []  # To store the main results

        for post in posts:
            try:
                link = post.find('a', class_='img')['href']
                img = post.find('img')['data-original'] if 'data-original' in post.find('img').attrs else post.find('img')['src']
                print(f"\n{link}\n")
                # Scrape additional data from the individual post link
                additional_data = scrape_additional_data(link)

                results.append({
                    'href': link,
                    'img': img,
                    'additional_data': additional_data
                })
            except Exception as e:
                print(f"Failed to process post: {e}")

        return results  # Return the main results
    except Exception as e:
        print(f"Failed to parse the main page: {e}")
        return None
def scrape_additional_data(link):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(link)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        btns_div = soup.find('div', class_='btns')
        
        if btns_div:
            servers = {}
            for btn in btns_div.find_all('a', class_='btn-server'):
                title = btn.get_text(strip=True)
                data_link = btn['data-link']
                servers[title] = data_link
            print(servers)
            return servers  # Return the dictionary of servers
    else:
        print(f"Failed to access the page: {link}")
    
    return None  # Return None if failed

def reverse_string(s):
    return s[::-1]

def fetch_redirect_url(data_link):
    reversed_link = reverse_string(data_link)
    url = f'https://darenx-unblockjapan.hf.space/proxy/https://lk1.supremejav.com/javeve_tv.php?c={reversed_link}'
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': url,
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
    }
    
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers=headers)
    if response.status_code == 200:
        return extract_redirect_url(response.text)
    else:
        print(f"Failed to fetch URL: {url}")
        return None

def extract_redirect_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Check for the <meta> tag with name="og:url"
    meta_tag = soup.find('meta', attrs={'name': 'og:url'})
    if meta_tag and 'content' in meta_tag.attrs:
        streamtape_url = meta_tag['content']
        # Remove the '/proxy/' prefix if it exists
        if streamtape_url.startswith('/proxy/'):
            streamtape_url = streamtape_url.replace('/proxy/', '', 1)
        # Prepend the base URL
        streamtape_url = f"{streamtape_url}"
        print(streamtape_url)
        return replace_streamtape_url(streamtape_url)  # Replace the URL if it's a streamtape URL

    # If no valid meta tag found, continue with the script extraction
    script_tag = soup.find('script')
    if script_tag:
        script_content = script_tag.string
        print(script_content)
        if script_content:
            # Check for the 'else' block
            if 'window.location.href' in script_content:
                # Extract the URL from the else block
                if "window.location.href = '" in script_content:
                    start = script_content.find("window.location.href = '") + len("window.location.href = '")
                    end = script_content.find("'", start)
                    redirect_url = script_content[start:end]
                    redirect_url = redirect_url.replace("/proxy/https://maxfinishseveral.com/", "https://voe.sx/")
                    print(redirect_url)
                    return replace_streamtape_url(redirect_url)  # Replace the URL if it's a streamtape URL

    print("No valid redirect URL found.")
    return None

def replace_streamtape_url(url):
    if "streamtape.com" in url:
        # Replace the base URL with streamtape.to
        return url.replace("https://streamtape.com/e/", "https://streamtape.to/v/")
    return url