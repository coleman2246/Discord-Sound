import cv2
from bs4 import BeautifulSoup
import numpy as np
import requests
import threading
import urllib.request

count = 0

def download_img(folder, url):
    global count
    count += 1
    print("Downloading",count)
    urllib.request.urlretrieve(url, folder+"/" +url.split("/")[-1])

def get_pages(urls):
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}    
    
    for url in urls:
        html = requests.get(url,headers=header).text
        soup = BeautifulSoup(html,"html.parser")
        image_divs = soup.findAll("div", {"class": "post-image"})

        for i in image_divs:
            for x in i.findAll("img"):
                download_img("testing",x["src"])
        



thread_count = 16
base_url = "https://unbelievablefactsblog.com/page/"
urls = []
threads = []
for i in range(6137):
    urls.append(base_url+str(i))

split_urls = np.array_split(urls,thread_count)

for i in range(thread_count):
    t = threading.Thread(target=get_pages, args=(split_urls[i],))
    threads.append(t)
    print(i)
    t.start()



for i in threads:
    i.join()

