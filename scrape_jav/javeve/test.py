import cfscrape

url = "https://darenx-unblockjapan.hf.space/proxy/https://javeve.tv/page/1/?s=yumi"

scraper = cfscrape.create_scraper() 
response = scraper.get(url)
print(response.text)