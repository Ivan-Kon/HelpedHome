from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio

from Settings import *
from SQL import Tables


class Scrape:
    def __init__(self):
        self.all_links_lists = [URL]
        self.links_lists = []
        self.all_links_obv = []
        self.page = None
        self.browser = None
        self.obv_info = []


    async def add_info(self,page_url,price,area,obv_info):
        """self.page_info = {
            'url': page_url,
            'price': price,
            'area': area,
            'devices': obv_info
        }
        self.all_info_obv.append(self.page_info)"""
        Tables(url=page_url,
               area=area,
               money=price,
               devices=obv_info).add_flat()


    async def scrape_href_lists(self):
        for j in self.all_links_lists:
            await self.page.goto(j, timeout=60000)
            html = await self.page.content()
            data = BeautifulSoup(html, "lxml")
            div_lists = data.find("div", class_=LISTS_DIV_CLASS)
            lists = div_lists.find_all("a", class_=LISTS_A_CLASS)
            for i in lists[-1:]:
                if len(self.all_links_lists) <= len(lists) - 1:
                    if "https://tver.cian.ru" in i.get("href") and i not in self.all_links_lists:
                        self.all_links_lists.append(i.get("href"))
                    elif i not in self.all_links_lists:
                        i = "https://tver.cian.ru" + i.get("href")
                        self.all_links_lists.append(i)
                else:
                    break


    async def scrape_href_obv(self):
        #парсим все объявления
        for link_list in self.all_links_lists:
            await self.page.goto(link_list, timeout=60000)
            html = await self.page.content()
            data = BeautifulSoup(html, "lxml")
            all_links = data.find_all("a", class_=OBV_CLASS_LINK)
            for i in all_links:
                self.all_links_obv.append(i.get("href"))


    async  def scrape_info_obv(self):
        obv_info = []
        info_area = None
        for link_obv in self.all_links_obv:
            await self.page.goto(link_obv, timeout=60000)
            html = await self.page.content()
            data = BeautifulSoup(html, "lxml")
            try:
                info_devices_div = data.find(name="div", class_=OBV_CLASS_INFO_DIV)
                info_devices = info_devices_div.find_all(name="span", class_=OBV_CLASS_INFO_SPAN)
            except AttributeError:
                info_devices = None

            info_price_div = data.find(name="div",class_=OBV_CLASS_PRICE_DIV)
            info_price = info_price_div.find(name="span",class_=OBV_CLASS_PRICE_SPAN).get_text().replace('₽/мес.', '').replace('\xa0', '')
            if info_devices is not None:
                for i in info_devices:
                    obv_info.append(i.get_text())
            info_area_div = data.find(name="div",class_=OBV_CLASS_AREA_DIV)
            info_area_all = info_area_div.find_all(name="a", class_=OBV_CLASS_AREA_A)
            print(info_area_all)
            for area in info_area_all:
                area = area.get_text()
                print(area)
                if area == "Заволжский" or area == "Московский" or area == "Центральный" or area == "Пролетарсикй":
                    info_area = area
                    break
            await self.add_info(page_url=link_obv,
                                price=info_price,
                                area=info_area,
                                obv_info=obv_info)


    async def run(self):
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=False)
            self.page = await self.browser.new_page()
            await self.page.set_extra_http_headers(USER_AGENT)
            await self.scrape_href_lists()
            await self.scrape_href_obv()
            await self.scrape_info_obv()

asyncio.run(Scrape().run())