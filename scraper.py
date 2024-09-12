import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.ufu.br"

def scraper_ufu():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    section = soup.find('section', {'id': 'block-menu-block-2'})
    
    if not section:
        print("Seção não encontrada!")
        return []

    menu_items = []
    for link in section.find_all('a', href=True):
        text = link.text.strip()
        href = link['href']
        
        if href.startswith('/'):
            href = URL + href
        
        if text and href:
            menu_items.append({
                'menuNav': text,
                'link': href,
                'created_at': datetime.now()
            })
    
    return menu_items
