import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def get_page(url):
	r = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"})
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	return r.text

def get_subway_url(html):
	subway_url_list = []
	soup = BeautifulSoup(html,"html.parser")
	s = soup.find(attrs={'log-set-param':'table_view'})
	for i in s.find_all(attrs={"target":"_blank"}):
		subway_url_list.append("https://baike.baidu.com" + i.attrs['href'])
	return subway_url_list

def get_station_connection(subway_url_list):
	station_connection = defaultdict(list)
	for subway_url in subway_url_list:
		subway_html = get_page(subway_url)
		soup = BeautifulSoup(subway_html, "html.parser")
		s = soup.find(attrs={'log-set-param':'table_view','data-sort':'sortDisabled'})
		station_list = s.select('a[target="_blank"]')
		for index, station in enumerate(station_list):
			if i.string:
				if "站" != i.string[-1]:
					continue
			if i.string not in station_list.keys():
				station_list[i.string] = []
			else:
				if index != 0:
					station_list[station_list[index-1]].append(i.string)
	return station_connection

if __name__ == "__main__":

	url = "https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485"
	main_page = get_page(url)
	subway_url_list = get_subway_url(main_page)
	get_station_connection(subway_url_list)

