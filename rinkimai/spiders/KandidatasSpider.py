# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatasItem
import re

class KandidatasSpider(CrawlSpider):
        name = "kandidatas"
        allowed_domains = ["www.vrk.lt"]
	start_urls = ["http://www.vrk.lt/2012_seimo_rinkimai/output_lt/rezultatai_vienmand_apygardose/rezultatai_apylinke219686visodesc1turas.html"]
	rules =[Rule(SgmlLinkExtractor(allow=['/Kandidatai/Kandidatas'],deny=['output_en']), 'parse_kandidatas', follow=False)

			]

	def parse_kandidatas(self,response):
		hxs = HtmlXPathSelector(response)
		item = KandidatasItem()
		item['kandidatas'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/text()')[0].extract().encode('UTF8')
		item['iskele'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/text()')[2].extract().encode('UTF8')
		item['saraso_numeris'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/text()')[4].extract().encode('UTF8')
		item['apygarda'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/a/text()')[0].extract().encode('UTF8')
		rez=hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[1].select('tr/td').extract()[0].encode('UTF8')
		item['gimimo_data'] = rez[rez.rfind('Gimimo data <b>')+len('Gimimo data <b>'):rez.find('Gimimo data <b>')+10+len('Gimimo data <b>')]
		rez = rez[rez.rfind('gyvenamosios vietos adresas <b>')+len('gyvenamosios vietos adresas <b>'):]
		item['gyvena'] = rez[0:rez.find('</b>')]
		rez = rez[rez.find('Gimimo vieta <b>')+len('Gimimo vieta <b>'):]
		item['gimimo_vieta'] = rez[0:rez.find('</b>')]
		rez = rez[rez.find('11. Tautyb')+len('11. Tautyb')+6:]
		item['tautybe'] = rez[0:rez.find('\r\n')]
		if rez.find('16. Pagrindin')>0:
			rez = rez[rez.find('16. Pagrindin')+len('16. Pagrindin')+28:]
			item['darboviete'] = rez[0:rez.find('</b>')]
		if rez[rez.find('18. Pom')]>0:
			rez = rez[rez.find('18. Pom')+len('18. Pom')+10:]
			item['pomegiai'] = rez[0:rez.find('</b>')]
		if rez.find('19. Šeiminė padėtis')>0:
			rez = rez[rez.find('19. Šeiminė padėtis')+len('18. Šeiminė padėtis <b>'):]
			item['seimynine_padetis'] = rez[0:rez.find('</b>')]
		yield item

