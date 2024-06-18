from bs4 import *
import requests
import os
import concurrent.futures
import time

max_workers = 10

# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):

	# initial count is zero
	count = 0

	# print total images found in URL
	# print(f"Total {len(images)} Image Found! for {folder_name}")

	# checking if images is not zero
	if len(images) != 0:
		for i, image in enumerate(images):
			# From image tag ,Fetch image Source URL

						# 1.data-srcset
						# 2.data-src
						# 3.data-fallback-src
						# 4.src

			# Here we will use exception handling

			# first we will search for "data-srcset" in img tag
			try:
				# In image tag ,searching for "data-srcset"
				image_link = image["data-srcset"]

			# then we will search for "data-src" in img
			# tag and so on..
			except:
				try:
					# In image tag ,searching for "data-src"
					image_link = image["data-src"]
				except:
					try:
						# In image tag ,searching for "data-fallback-src"
						image_link = image["data-fallback-src"]
					except:
						try:
							# In image tag ,searching for "src"
							image_link = image["src"]

						# if no Source URL found
						except:
							pass

			# After getting Image Source URL
			# We will try to get the content of image
			try:
				r = requests.get(image_link).content
				try:

					# possibility of decode
					r = str(r, 'utf-8')

				except UnicodeDecodeError:

					# After checking above condition, Image Download start
					with open(f"{folder_name}/images{i+1:03}.jpg", "wb+") as f:
						f.write(r)

					# counting number of image downloaded
					count += 1
			except:
				pass

		# There might be possible, that all
		# images not download
		# if all images download
		if count == len(images):
			print(f"Chapter '{folder_name}' All Images Downloaded!")

		# if all images not download
		else:
			print(f"Incompleted chapter '{folder_name}', {count} Images Downloaded Out of {len(images)}")
			os.rmdir(folder_name)

def get_all_images(url, folder_name):
	# content of URL
	time.sleep(1)
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	r = requests.get(url,headers=headers)

	# Parse HTML Code
	soup = BeautifulSoup(r.text, 'html.parser')

	# Find div with panel-body class
	panel_body = soup.find('div', class_='panel-body')

	if panel_body:
		# find all images in URL
		images = panel_body.findAll('img')
		if len(images) != 0:
			os.mkdir(folder_name)
			download_images(images, folder_name)

def get_all_links(url):

	# Obtener el contenido de la página
	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')

	# Encontrar todos los elementos <li> con la clase 'list-group-item'
	list_items = soup.find_all('li', class_='list-group-item')

	# Extraer los enlaces
	links = []
	for item in list_items:
		a_tag = item.find('a')
		if a_tag:
			links.append({'url' : a_tag['href'], 'title' : a_tag.text.strip()})
	return links

# MAIN FUNCTION START
def main(url):
	links = get_all_links(url)
	if not links:
		print(f"No one link Found for {url}")
		exit()

	# content of URL
	with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
		# Create future requests
		futures = [executor.submit(get_all_images, link['url'], link['title']) for link in links]

		# Wait to complete
		for future in concurrent.futures.as_completed(futures):
			try:
				# Get results
				future.result()
			except Exception as exc:
				print(f"Generated an exception: {exc}")

baseurl = r"https://mangalatino.com/serie/mahou-tsukai-no-yome"
# take url
url = input("Please insert the url: ")
if url:
	baseurl = url
main(baseurl)
