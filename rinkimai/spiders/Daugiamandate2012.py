from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import DaugiamandatesRezultataiApygardojeItem 
from rinkimai.items import DaugiamandatesRezultataiApylinkejeItem 
import re

class DaugiamandateSpider(CrawlSpider):
        name = "daugiamandate2012"
        allowed_domains = ["www.vrk.lt"]
	start_urls = ["http://www.vrk.lt/2012_seimo_rinkimai/output_lt/rezultatai_daugiamand_apygardose/rezultatai_daugiamand_apygardose1turas.html"]
	rules =[Rule(SgmlLinkExtractor(allow=['output_lt/rezultatai_daugiamand_apygardose/apylinkes'],deny=['output_en']), 'parse_apylinke', follow=False),
		Rule(SgmlLinkExtractor(allow=['rezultatai_daugiamand_apygardose/balsavimasatstovybese'],deny=['output_en']), 'parse_apylinke', follow=True),
		Rule(SgmlLinkExtractor(allow=['rezultatai_daugiamand_apygardose/apygardos_rezultatai'],deny=['output_en']), 'parse_apygarda', follow=True)

			]

        def parse_apygarda(self,response):

                hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//h2')[0].select('text()').extract()[0].encode('UTF8')
		apylinkes = hxs.select('//table[@class="partydata"]')[3].select('tr')
		partijos = hxs.select('//table[@class="partydata"]')[2].select('tr')
		for part in partijos:
			item = DaugiamandatesRezultataiApygardojeItem()
			item['apygarda'] = apygarda
			if len(part.select('td/a/text()').extract())>0:
				item['partija'] = (part.select('td/a/text()').extract())[0].encode('UTF8')
				item['apylinkese'] = (part.select('td')[3].select('text()').extract()[0]).encode('UTF8')
				item['pastu'] =(part.select('td')[4].select('text()').extract()[0]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (part.select('td')[6].select('text()').extract()[0]).encode('UTF8')
				yield item
	
	def parse_apylinke(self,response):
		hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//h2')[0].select('a/text()').extract()[0].encode('UTF8')
		apylinke = hxs.select('//h2')[1].select('text()').extract()[0].encode('UTF8')
		
		partijos = hxs.select('//table[@class="partydata"]')[2].select('tr')
		for part in partijos:
			
			item = DaugiamandatesRezultataiApylinkejeItem()
			item['apygarda'] = apygarda
			item['apylinke'] = apylinke

			if len(part.select('td/text()').extract())>0  and len(part.select('td[@colspan="3"]'))==0:
				if len(part.select('td')[1].select('text()'))>0:
                                        item['partija'] = (part.select('td')[1].select('text()')[0].extract()).encode('UTF8')
                                else:
                                        item['partija'] = (part.select('td')[1].select('a/text()')[0].extract()).encode('UTF8')
				item['apylinkese'] =  (part.select('td')[3].select('text()')[0].extract()).encode('UTF8')
				item['pastu'] = (part.select('td')[4].select('text()')[0].extract()).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (part.select('td')[6].select('text()')[0].extract()).encode('UTF8')
				yield item
