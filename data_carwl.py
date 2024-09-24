import os
import requests
from bs4 import BeautifulSoup

url = "https://kr.ufc.com/athlete/klidson-abreu"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

bio_data = soup.find("div", class_="c-bio__row--3col")
height_data = bio_data.find_all('div',class_="c-bio__text")[1]
weight_data = bio_data.find_all('div',class_="c-bio__text")[2]
height = height_data.text.strip()
weight = weight_data.text.strip()
print(height,weight)
