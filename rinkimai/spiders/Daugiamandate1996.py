from __future__ import division
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import DaugiamandatesRezultataiApygardojeItem 
from rinkimai.items import DaugiamandatesRezultataiApylinkejeItem 
import re

class DaugiamandateSpider(CrawlSpider):
        name = "daugiamandate1996"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/n/rinkimai/seim96/rdsarl.htm-1.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['rdapgpl.htm']), 'parse_apygarda', follow=False),
#		Rule(SgmlLinkExtractor(allow=['rezultatai/rez_apg_l_'],deny=['rez_apg_e_']), 'parse_apygarda', follow=True)

			]

        def parse_apygarda(self,response):
                hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//p/font/text()')[4].extract().encode('UTF8')
		viso = int(hxs.select('//p')[6].select('b/text()')[0].extract().encode('UTF8'))
		viso_biuleteniu = int(hxs.select('//p')[6].select('b/text()')[5].extract().encode('UTF8'))

		partijos =hxs.select('//table/tr')

		for part in partijos:
			item = DaugiamandatesRezultataiApygardojeItem()
			item['apygarda'] = apygarda
			if len(part.select('td/text()').extract())>0:
				item['partija'] = part.select('td/a/text()').extract()[0].encode('UTF8')
				item['apylinkese'] =  (part.select('td/text()').extract()[1]).encode('UTF8').replace("\xc2\xa0", "")
				item['pastu'] = (part.select('td/text()').extract()[2]).encode('UTF8').replace("\xc2\xa0", "")
				item['nuo_galiojanciu_biuleteniu'] =round(int((part.select('td/text()').extract()[3]).encode('UTF8').replace("\xc2\xa0", ""))/viso_biuleteniu,4)
				yield item
		"""
	
	def parse_apylinke(self,response):
		hxs = HtmlXPathSelector(response)
		apylinke = hxs.select('//h4/text()').extract()[0].encode('UTF8')
		apygarda = hxs.select('//h5/a')[1].select('text()').extract()[0].encode('UTF8')
		partijos = hxs.select('//table[@class="basic"]')[0].select('tr')
		 
		for part in partijos:
			
			item = DaugiamandatesRezultataiApylinkejeItem()
			item['apygarda'] = apygarda
			item['apylinke'] = apylinke
			if len(part.select('td/text()').extract())>0:
				item['partija'] = (part.select('td/table/tr/td/text()').extract())[0].encode('UTF8')
				item['apylinkese'] = (part.select('td/text()').extract()[1]).encode('UTF8')
				item['pastu'] = (part.select('td/text()').extract()[2]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (part.select('td/text()').extract()[4]).encode('UTF8')
				yield item
		"""	
