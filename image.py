from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import io
from PIL import Image
import time, os
import pandas as pd

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument("--disable-blink-features")
option.add_argument("--disable-gpu")
#option.add_argument("--headless")
option.add_argument('--disable-blink-features=AutomationControlled')
wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

	url = "https://www.pexels.com/search/hd%20wallpaper/"
	wd.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'})
	wd.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
	wd.get(url)
	image_urls = list()
	global img_name
	img_name = list()
	while len(image_urls) < max_images:
		scroll_down(wd)
		time.sleep(delay)
		images = wd.find_elements(By.CLASS_NAME, "photo-item__img")
		for image in images:
			if image.get_attribute('src') in image_urls:
				continue
			if len(image_urls) >= max_images:
				break

			if image.get_attribute('src') and 'http' in image.get_attribute('src'):
				image_urls.append(image.get_attribute('src'))
				
			if image.get_attribute('alt'):
				img_name.append(image.get_attribute('alt'))
				print(f"Found {len(image_urls)}")

	return image_urls

def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name
		with open('images.csv', 'a') as f:
			f.write(str(a) + ',' + url + ',' + file_name + '\n')
		with open(file_path, "wb") as f:
			image.save(f, "JPEG")
		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 10)
try:
    os.mkdir('imgs')
except:
	pass
a = 0
try:
    os.remove('images.csv')
except:
    pass
with open('images.csv', 'w') as fp:
    pass
for i, url in enumerate(urls):
    a = a+1
    download_image("imgs/", url, img_name[i] + ".jpg")
wd.quit()