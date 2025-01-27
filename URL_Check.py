import requests  # type: ignore
import csv 
from bs4 import BeautifulSoup # type: ignore
from concurrent.futures import ThreadPoolExecutor
import urllib3 # type: ignore


urllib3.disable_warnings()

# User Stories for URL Status Checking Program
def check_url(url): 
    try: 
        response = requests.get(url) 
        if response.status_code == 200: 
            print(f"The URL {url} responded positively.") 
        else: 
            print(f"The URL {url} responded with status code: {response.status_code}.") 
    except requests.exceptions.RequestException as e: 
        print(f"An error occurred: {e}") 

# As a user, I want to check if a website is loading or not, 
# so that I can verify its availability and accessibility.
def check_redirect(url): 
    try: 
        response = requests.head(url, allow_redirects=True) 
        if response.history: 
            print("The URL was redirected.") 
            for resp in response.history: 
                print(f"Redirected from {resp.url} to {resp.headers['Location']}") 
                print(f"Final destination: {response.url}") 
        else: 
            print("No redirect occurred. The URL is direct.") 
    except requests.exceptions.RequestException as e: 
        print(f"An error occurred: {e}")

# As a user, I want to know if the website is redirected and, if yes, 
# to where, so that I can understand the final destination of the URL.
def return_checked_redirect(url): 
    try: 
        response = requests.head(url, allow_redirects=True) 
        if response.history: 
            final_url = response.url 
            return (url, ' Yes, rediredt to:', final_url) 
        else: 
            return (url, ' No, it is the same as:', url) 
    except requests.exceptions.RequestException as e: 
        return (url, 'Error', str(e)) 

# As a user, I want to check 100 websites and have the output saved as a CSV file, 
# so that I can easily review and share the results.
def batch_process(urls, output_file): 
    results = [] 
    for url in urls: 
        result = return_checked_redirect(url) 
        results.append(result) 
        with open(output_file, mode='w', newline='') as file:
             writer = csv.writer(file) 
             writer.writerow(['Original URL', 'Redirected', 'Final URL']) 
             writer.writerows(results) 

# As a user, I want the program to automatically add 
# "http://" to URLs that lack a scheme, ensuring they load correctly.
def return_added_scheme(url): 
    try: 
        if not url.startswith(("http://", "https://")):
             final_url = "http://" + url 
             return (url, ' Without scheme:', final_url) 
        else:
            return (url, ' With scheme:', url) 
    except requests.exceptions.RequestException as e: 
        return (url, 'Error', str(e)) 

def add_scheme_to_urls(urls, output_file):
     updated_urls = []
     for url in urls:
        updated_url = return_added_scheme(url) 
        updated_urls.append(updated_url) 
        with open(output_file, mode='w', newline='') as file:
             writer = csv.writer(file) 
             writer.writerow(['Original URL', 'Redirected', 'Final URL']) 
             writer.writerows(updated_urls) 

def add_scheme_to_url(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url

# As a user, I want HTTPS errors to be ignored, allowing the program 
# to proceed with checking the website status without interruption.
def check_website_status(url):
    try:
        response = requests.get(url, timeout=5, verify=False)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    
# As a user, I want the program to check if a website is a "dummy page," 
# such as those under construction, so that I can filter out placeholder content.
def is_dummy_page(url):
    dummy_keywords = ["under construction", "coming soon", "placeholder", "dummy page"]
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()
        
        for keyword in dummy_keywords:
            if keyword in page_text:
                return True
        return False
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

#As a user, I want the website to be categorized as belonging to one of the Merck sectors 
# (Healthcare, Life Science, Electronics, or Emerging Fields). If the categorization confidence is below 90%, 
# I want it to be labeled as "unknown," ensuring accuracy in sector identification.
def categorize_website(url):
    merck_sectors = ["healthcare", "life science", "electronics", "emerging fields"]
    sector_keywords = {
        "healthcare": ["pharmaceutical", "biopharmaceutical", "drug", "medicine"],
        "life science": ["biotech", "biological", "lab equipment", "chemicals"],
        "electronics": ["semiconductor", "display", "materials", "electronics"],
        "emerging fields": ["innovation", "research", "new technology"]
    }
    
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text().lower()

        max_confidence = 0
        identified_sector = "unknown"
        
        for sector, keywords in sector_keywords.items():
            confidence = sum(keyword in page_text for keyword in keywords)
            confidence_percentage = (confidence / len(keywords)) * 100
            if confidence_percentage > max_confidence:
                max_confidence = confidence_percentage
                identified_sector = sector
        
        if max_confidence >= 50:
            return identified_sector
        else:
            return "unknown"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

#As a user, I want the program to utilize multiple workers to process URLs concurrently, 
# so that the status checking operation is completed more quickly and efficiently
def check_website_status_with_url(url):
    try:
        response = requests.get(url, verify=False)
        return (url, response.status_code)
    except requests.exceptions.RequestException as e:
        return (url, f"Error: {e}") 

def process_urls_concurrently(output_file, urls, max_workers=10):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_website_status_with_url, url) for url in urls]
        for future in futures:
            results.append(future.result())
            with open(output_file, mode='w', newline='') as file:
                writer = csv.writer(file) 
                writer.writerow(['Original URL', 'Status']) 
                writer.writerows(results) 
    #return results

# Run examples
urls = [
    "https://example.com",
    "https://example2.com",
    "https://example3.com"
]

# Data to be used in examples
# most used URLs
most_visited_urls = [ "https://www.google.com", "https://www.youtube.com", "https://www.facebook.com", "https://www.wikipedia.org", "https://www.instagram.com",
                      "https://www.reddit.com", "https://www.bing.com", "https://www.x.com", "https://www.whatsapp.com", "https://www.taboola.com",
                       "https://www.chatgpt.com", "https://www.yahoo.com", "https://www.amazon.com", "https://www.yandex.ru", "https://www.twitter.com",
                        "https://www.duckduckgo.com", "https://www.yahoo.co.jp", "https://www.tiktok.com", "https://www.msn.com", "https://www.netflix.com",
                        "https://www.weather.com", "https://login.live.com", "https://www.microsoftonline.com", "https://www.naver.com", "https://www.linkedin.com",
                        "https://www.microsoft.com", "https://www.twitch.tv", "https://www.office.com", "https://www.vk.com", "https://www.openai.com", 
                        "https://www.pinterest.com", "https://www.quora.com", "https://www.discord.com", "https://www.canva.com", "https://www.aliexpress.com", 
                        "https://www.github.com", "https://www.apple.com", "https://www.globo.com", "https://www.spotify.com", "https://www.roblox.com",
                        "https://www.mail.ru", "https://www.imdb.com", "https://www.cnn.com", "https://www.nytimes.com", "https://www.amazon.co.jp",
                        "www.ebay.com", "https://www.telegram.org", "https://www.paypal.com", "https://www.marca.com", "https://www.bbc.co.uk", 
                        "https://www.bbc.com", "https://www.espn.com", "www.samsung.com", "www.amazon.de", "https://www.dzen.ru", 
                        "https://www.instructure.com", "https://www.temu.com", "https://www.booking.com", "https://www.zoom.us", "https://www.indeed.com",
                        "https://www.amazon.in", "https://www.uol.com.br", "https://www.rakuten.co.jp", "www.dailymail.co.uk", "https://www.dailymotion.com",
                        "https://www.amazon.co.uk", "https://www.avito.ru", "https://www.accuweather.com", "https://www.wildberries.ru", "https://www.adobe.com",
                        "https://www.amazonaws.com", "https://www.theguardian.com", "https://www.google.de", "https://www.gismeteo.ru", "https://www.walmart.com",
                        "https://www.etsy.com", "https://www.primevideo.com", "www.disneyplus.com", "www.rutube.ru", "https://www.foxnews.com",
                        "https://www.google.co.uk", "www.ozon.ru", "www.ecosia.org", "https://www.as.com", "www.usps.com",
                        "https://www.infobae.com", "https://outlook.com", "https://www.google.fr", "https://www.google.com.br", "https://www.google.co.jp",
                        "https://www.flipkart.com", "https://www.line.me", "https://www.zillow.com", "https://www.ya.ru", "https://www.max.com",
                        "www.archive.org", "https://www.amazon.it", "https://www.tradingview.com", "www.ikea.com"]

most_ten_visited_urls = [ "https://www.google.com", "https://www.youtube.com", "https://www.facebook.com", "https://www.wikipedia.org", "https://www.instagram.com",
                      "https://www.reddit.com", "https://www.bing.com", "https://www.x.com", "https://www.whatsapp.com", "https://www.taboola.com"]


redirect_output_file = 'redirect_results.csv' 
add_scheme_file = 'add_scheme_results.csv' 
return_status_file = 'return_status_results.csv' 

batch_process(most_visited_urls, redirect_output_file)
add_scheme_to_urls(most_visited_urls, add_scheme_file)
process_urls_concurrently(return_status_file, most_visited_urls, max_workers=5)


url = "www.archve.org"
status_code = check_website_status(add_scheme_to_url(url))
print(f"Status Code: {status_code}")


url = "https://www.circuitlab.com/"
sector = categorize_website(url)
print(f"Identified Sector: {sector}")


is_dummy = is_dummy_page(add_scheme_to_url(url))
print(f"Is dummy page: {is_dummy}")

check_redirect("http://www.twitter.com/")

check_url("http://www.google.com")


