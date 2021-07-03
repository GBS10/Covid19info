import requests
from bs4 import BeautifulSoup as bs
import json
url=["https://nhmtn.maps.arcgis.com/apps/opsdashboard/index.html#/095ad0a1c0254b058fa36b32d1ab1977"]
for link in url:
	r=requests.get(link)
	if r.status_code!=200:
		print("Link failed")
		continue
	page=r.text
	soup=bs(page,'html.parser')
	print(soup)
