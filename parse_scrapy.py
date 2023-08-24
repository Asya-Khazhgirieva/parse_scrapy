import scrapy
import re
from scrapy.item import Item, Field

#Чтобы запустить этот скрипт открываем терминал, переходим в расположение текущего паука:
#cd C:\Users\user\....
#Далее вводим команду запуска:
#scrapy crawl site
#Спаршенные данные сохраняются в C:\Users\user\Desktop\Рабочий ПК\Код\tutorial\tutorial\spiders\data\site
#Проверка селектора в Scrapy Shell
#>>> scrapy shell
#>>> fetch(“url”)
#Чтобы выйти из Scrapy Shell нажимаем Ctrl + z

class MySpider(scrapy.Spider):
	name = "site"
	start_urls = ["URL"]

	def parse(self, response):
		#Парсим ссылки на товары, которые в наличии
		for product_card in response.css("div.catalog-card"):
			availability = product_card.css("span.card-stock::text").get()
			if availability == "В наличии":
				links = product_card.css("div.catalog-card__info a::attr(href)")
				for link in links:
					yield response.follow(link, callback=self.parse_item)
					print("Зашла в IF")

		#Парсим ссылку на следующую страницу
		next_page = response.xpath("//li[@class='disabled']//following::li/a/@href").get()
		if next_page != 'mailto:info@site.ru':
			yield response.follow(next_page, callback=self.parse)

	def parse_item(self, response):
		#Характеристики оформляем в таблицу
		technical = response.css("div.itempage-info__table").get()
		if technical != None:
			technical = technical.replace('<div class="itempage-info__table">', '<table><tbody>')
			technical = technical.replace('<div class="itempage-info__row">', '<tr>')
			technical = technical.replace('<div class="itempage-info__first">', '<td>')
			technical = technical.replace('<div class="itempage-info__second">', '<td>')
			technical = technical.replace('</div><td>', '</td><td>')
			technical = technical.replace('</div></div><tr>', '</td></tr><tr>')
			technical = technical.replace('</div></div></div>', '</td></tr></tbody></table>')
			technical = re.sub("<tr><td>Код склада</td><td>(.*?)</td></tr>", "", technical)
			technical = re.sub("<tr><td>Сайт производителя</td><td>(.*?)</td></tr>", "", technical)
			technical = technical.replace('<tr><td>Область применения</td><td>для дома</td></tr>', '')
			technical = technical.replace('<tr><td></td><td>3</td></tr>', '')

		#Название делим на название и артикул
		name = response.css("h1::text").get()
		name_list = name.split(", ")
		artikle = name_list.pop(-1)
		name = name_list[:]
		name = ', '.join(name)

		#Добавляем домен к URL изображения
		image = response.css("img.itempage-slider__thumb::attr(src)").getall()
		i = len(image)
		if i >= 1:
			image1 = "https://site.ru" + image.pop(0)
		i = len(image)
		s = 0
		if i >= 1:
			while i >= 1:
				if image[s]:
					image[s] = "https://site.ru" + image[s]
					i -= 1
					s += 1
				else:
					break

		#Обрабатываем расширенное описание товара
		details = response.css("p.itempage-info__text::text").get()
		details = re.sub("^Мы работаем по полной или частичной онлайн предоплате.*", "", details)
		
		#Собираем нужные нам поля со страницы товара
		yield{
			"Name":name,
			"ItemID":artikle,
			"Price":response.css("span.itempage-content__price::text").get(),
			"Description":response.css("p.itempage-content__desc::text").get(),
			"Details":details,
			"Technical":technical,
			"Image":image1,
			"Image1":image,
			"Breadcrumb1":response.xpath("/html/body/div[1]/div[3]/div/div[1]/ul/li[3]/a/text()").get(),
			"Breadcrumb2":response.xpath("/html/body/div[1]/div[3]/div/div[1]/ul/li[4]/a/text()").get(),
		}