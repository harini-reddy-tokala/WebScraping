import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page
URL = "https://nagpur.gov.in/"

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = []

    # Extract headings
    for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        data.append({
            'type': 'heading',
            'content': heading.text.strip()
        })
    
    # Extract paragraphs
    for paragraph in soup.find_all('p'):
        data.append({
            'type': 'paragraph',
            'content': paragraph.text.strip()
        })
    
    # Extract links
    for link in soup.find_all('a', href=True):
        data.append({
            'type': 'link',
            'content': link['href']
        })

    return data

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    html = get_html(URL)
    if html:
        data = parse_html(html)
        save_to_csv(data, 'nagpur.csv')
        print(f"Scraped {len(data)} elements and saved to 'nagpur.csv'")
    else:
        print("Failed to retrieve the HTML content.")
