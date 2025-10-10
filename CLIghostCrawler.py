import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import staticScraper
import dynamicScraper



def is_dynamic(url, html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text_length = len(soup.get_text(strip=True))
    if text_length < 100:
        print("text_length < 100, The website is likely dynamic (content loaded via JavaScript).")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            request_made = []
            page.on("request", lambda request: request_made.append(request.url))
            page.goto(url)
            browser.close()
            dynamic= any("api" in req or "json" in req for req in request_made)
            print("Dynamic content loaded via JavaScript.")
            return dynamic
        return False
                  
    else:
        print("The website is likely static (content directly in HTML).")
        return False
    
def main():
    url = input("Paste the URL of the website you want to crawl: ")
    html_content = requests.get(url).text
    if (is_dynamic(url, html_content)):
        dynamicScraper.main()
    else:
        staticScraper.main()

if __name__ == "__main__":
    main()