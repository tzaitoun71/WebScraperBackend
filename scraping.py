import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        main_content = soup.find('article') or soup.find('main') or soup.find('body')
        if not main_content:
            return "No main content found on the page."
        
        paragraphs = [p.text for p in main_content.find_all('p')]
        return ' '.join(paragraphs)
    
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"