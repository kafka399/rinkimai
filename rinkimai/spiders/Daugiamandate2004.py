from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import DaugiamandatesRezultataiApygardojeItem 
from rinkimai.items import DaugiamandatesRezultataiApylinkejeItem 
import re

class Daugiamandate2004Spider(CrawlSpider):
        name = "daugiamandate2004"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/rinkimai/2004/seimas/rezultatai/rez_l_20.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['rezultatai/rez_apl_l_'],deny=['rez_apg_e_']), 'parse_apylinke', follow=False),
		Rule(SgmlLinkExtractor(allow=['rezultatai/rez_apg_l_'],deny=['rez_apg_e_']), 'parse_apygarda', follow=True)

			]

        def parse_apygarda(self,response):
		"""
                hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//h4/text()').extract()[0].encode('UTF8')
		partijos = hxs.select('//table[@class="basic"]')[0].select('tr')

		for part in partijos:
			item = DaugiamandatesRezultataiApygardojeItem()
			item['apygarda'] = apygarda
			if len(part.select('td/text()').extract())>0:
				item['partija'] = (part.select('td/table/tr/td/a/text()').extract())[0].encode('UTF8')
				item['apylinkese'] =  (part.select('td/text()').extract()[1]).encode('UTF8')
				item['pastu'] = (part.select('td/text()').extract()[2]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (part.select('td/text()').extract()[4]).encode('UTF8')
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
	
