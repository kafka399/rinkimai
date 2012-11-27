from __future__ import division
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatoRezultaiApylinkejeItem
from rinkimai.items import ApylinkeItem
from rinkimai.items import KandidatoRezultaiApygardojeItem
import re

class VienmandateSpider(CrawlSpider):
        name = "vienmandate1996"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/n/rinkimai/seim96/rapgs1l.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['seim96/rapgpl.htm'],deny=['rezultatai/rezv_e_','_apg_e_']), 'parse_apygarda', follow=True),
		Rule(SgmlLinkExtractor(allow=['raplsarl.htm']), follow=True),
		Rule(SgmlLinkExtractor(allow=['seim96/raplpl.htm']), 'parse_apylinke', follow=False)

			]

        def parse_apygarda(self,response):
		hxs = HtmlXPathSelector(response)
		viso = int(hxs.select('//p/b/text()').extract()[2].encode())
		viso_biuleteniu = int(hxs.select('//p/b/text()').extract()[6]) 
		apygarda = hxs.select('//p/font/b/text()').extract()[0].encode('UTF8')
		kandidatai = hxs.select('//table/tr')
		#apylinkes = hxs.select('//div')[2].select('table/tr')

		for kan in kandidatai:
			item = KandidatoRezultaiApygardojeItem()
			item['apygarda'] = apygarda
			if len(kan.select('td/a/text()').extract())>0:
				item['kandidatas'] = (kan.select('td/a/text()').extract())[0].encode('UTF8')
				item['apylinkese'] =  (kan.select('td/text()').extract()[0]).encode('UTF8').replace("\xc2\xa0", "")
				item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8').replace("\xc2\xa0", "")
				item['nuo_galiojanciu_biuleteniu'] = round(int(hxs.select('//p/b/text()').extract()[6]),2)
				item['nuo_rinkeju'] = round(int((kan.select('td/text()').extract()[2]).encode('UTF8').replace("\xc2\xa0", ""))/(viso),2)
				yield item
		"""
		for ap in apylinkes:
	                item = ApylinkeItem()
			item['apygarda'] = apygarda
			if len(ap.select('td/a/text()').extract())>0:
				item['apylinke'] = (ap.select('td/a/text()').extract())[0].encode('UTF8')
				item['rinkeju_skaicius']=(ap.select('td/text()').extract())[1].encode('UTF8')
				item['dalyvavo'] = (ap.select('td/text()').extract())[2].encode('UTF8')
				item['negaliojantys_biuleteniai'] = (ap.select('td/text()').extract())[4].encode('UTF8')
				yield item
		"""

	def parse_apylinke(self,response):
		hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//p/font/b/text()').extract()[0].encode('UTF8')
		apylinke =hxs.select('//p/font/b/text()').extract()[1].encode('UTF8')
		viso = int(hxs.select('//b/text()')[3].extract().encode('UTF8'))
		viso_biuleteniu = int(hxs.select('//b/text()')[5].extract().encode('UTF8'))
		kandidatai = hxs.select('//table/tr')

		for kan in kandidatai:
			item = KandidatoRezultaiApylinkejeItem()
			item['apylinke'] = apylinke
			item['apygarda'] = apygarda

			if len(kan.select('td/a/text()').extract())>0:
				item['kandidatas'] = (kan.select('td/a/text()').extract())[0].encode('UTF8')
				item['balsadezeje'] =  (kan.select('td/text()').extract()[1]).encode('UTF8').replace("\xc2\xa0", "")
				item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8').replace("\xc2\xa0", "")
				item['nuo_galiojanciu_biuleteniu'] = round(int((kan.select('td/text()').extract()[2]).encode('UTF8').replace("\xc2\xa0", ""))/viso_biuleteniu,2)
				item['nuo_rinkeju'] = round(int((kan.select('td/text()').extract()[2]).encode('UTF8').replace("\xc2\xa0", ""))/viso,2)
				yield item
