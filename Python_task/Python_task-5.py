import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool
import sys


def get_links(url: str) -> list:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    links = soup.find_all("img")
    lst = []
    
    for item in links:
        if item['src'].startswith('http'):
            lst.append(item['src'])
        else:
            lst.append("https:" + item['src'])

    return lst

def download_images(url: str) -> None:
    links = get_links(url)
    if len(links) == 0:
        print(f"Скачать картинки с сайта {url} не удалось")
        return None
    dir_name = url.split('/')[2]
    os.mkdir(dir_name)
    count = 0
    
    for link in links:
        with open(f"{dir_name}/{count}.jpeg", "wb") as f:
            try:
                if link.startswith('http'):
                    f.write(requests.get(link).content)
                count += 1
            except:
                continue
            
if __name__ == "__main__":
    try:
        with Pool(20) as p:
            p.map(download_images, sys.argv[1:])
    except:
        print("Что-то пошло не так")
