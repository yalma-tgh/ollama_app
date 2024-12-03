# get_models.py
from bs4 import BeautifulSoup
import requests

def get_models():
    url = "https://ollama.com/library"
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    models = []
    li_elements = soup.find_all('li', class_='flex items-baseline border-b border-neutral-200 py-6')

    for li in li_elements:
        model = {}

        # Extract name
        name_elem = li.find('h2', class_='truncate text-xl font-medium underline-offset-2 md:text-2xl')
        if name_elem and name_elem.find('span'):
            model['name'] = name_elem.find('span').text.strip()

        # Extract size
        size_element = li.find('span', class_='inline-flex items-center rounded-md bg-[#ddf4ff] px-2 py-0.5 text-xs sm:text-[13px] font-medium text-blue-600')
        if size_element:
            model['size'] = size_element.text.strip()

        models.append(model)

    return models
