from __future__ import division
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import DaugiamandatesRezultataiApygardojeItem 
from rinkimai.items import DaugiamandatesRezultataiApylinkejeItem 
import re

class DaugiamandateSpider(CrawlSpider):
        name = "daugiamandate2000"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/n/rinkimai/20001008/rdsarl.htm-13.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['rdapgl.htm']),'parse_apygarda', follow=True),
		Rule(SgmlLinkExtractor(allow=['rdapll.htm']), 'parse_apylinke', follow=False)

			]

        def parse_apygarda(self,response):

                hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//p/b/font/font/text()').extract()[0].encode('UTF8')
		viso = int(hxs.select('//p/b/text()')[1].extract().encode('UTF8'))
		viso_biuleteniu =int(hxs.select('//p/b/text()')[3].extract().encode('UTF8'))
		
		partijos =hxs.select('//table/tr')

		for part in partijos:
			item = DaugiamandatesRezultataiApygardojeItem()
			item['apygarda'] = apygarda
			if len(part.select('td/a/text()').extract())>0:
				item['partija'] = part.select('td/a/text()').extract()[0].encode('UTF8')
				item['apylinkese'] =  (part.select('td/text()').extract()[3]).encode('UTF8').replace("\xc2\xa0", "")
				item['pastu'] = (part.select('td/text()').extract()[4]).encode('UTF8').replace("\xc2\xa0", "")
				item['nuo_galiojanciu_biuleteniu'] =round(int((part.select('td/text()').extract()[5]).encode('UTF8').replace("\xc2\xa0", ""))/viso_biuleteniu,4)
				yield item
	
	def parse_apylinke(self,response):

		hxs = HtmlXPathSelector(response)
		apylinke = hxs.select('//p/b/font/font/text()').extract()[1].encode('UTF8')
		apygarda = hxs.select('//p/b/font/font/text()').extract()[0].encode('UTF8')
		partijos =hxs.select('//table/tr') 
		viso = int(hxs.select('//b/text()')[1].extract().encode('UTF8'))
		viso_biuleteniu =int(hxs.select('//b/text()')[3].extract().encode('UTF8'))
		for part in partijos:
			
			item = DaugiamandatesRezultataiApylinkejeItem()
			item['apygarda'] = apygarda
			item['apylinke'] = apylinke
			if len(part.select('td/a/text()').extract())>0:
				item['partija'] = (part.select('td/a/text()').extract())[0].encode('UTF8')
				item['apylinkese'] = (part.select('td/text()').extract())[3].encode('UTF8').replace("\xc2\xa0", "")
				item['pastu'] =(part.select('td/text()').extract())[4].encode('UTF8').replace("\xc2\xa0", "")

				gal_biul = 0
				if ((part.select('td/text()').extract())[5].encode('UTF8').replace("\xc2\xa0", "")).isdigit():
					gal_biul = int((part.select('td/text()').extract())[5].encode('UTF8').replace("\xc2\xa0", ""))
					item['nuo_galiojanciu_biuleteniu'] = round(gal_biul/viso_biuleteniu,4)
				yield item
