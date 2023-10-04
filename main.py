#-*- coding: cp1251 -*-
from requests import get
from bs4 import BeautifulSoup as BS
from PIL import Image, UnidentifiedImageError
from io import BytesIO

WIKI_URL = 'https://en.wikipedia.org/wiki/%s'


def get_wiki_images(word):
    try:
        soup = BS(get(WIKI_URL % word).content, 'html.parser')
        images = soup.find_all('img')
        images_src = []
        for img in images:
            src = img.get('src')
            if src and word in src.lower():
                images_src.append(src)
        return images_src
    except ConnectionError as e:
        import sys
        print(word, e, file=sys.stderr)
        return []


def get_image_from_url(url):
    try:
        response = get('https:' + url)
        image = Image.open(BytesIO(response.content))
        return image
    except (UnidentifiedImageError, ConnectionError) as e:
        import sys
        print(url, e, file=sys.stderr)
        return None


if __name__ == "__main__":
    search_word = 'cats'
    images_urls = get_wiki_images(search_word)
    for img_url in images_urls:
        image = get_image_from_url(img_url)
        if image:
            image.show()
