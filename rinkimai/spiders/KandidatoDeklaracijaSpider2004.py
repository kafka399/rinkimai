# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatoDeklaracija
import re

class KandidatoDeklaracijaSpider(CrawlSpider):
        name = "kandidatoDeklaracija2004"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/rinkimai/2004/seimas/kandidatai/vapg_sar_l_20.htm"]
        rules =[Rule(SgmlLinkExtractor(allow=['apg_kand_l_'],deny=['output_en']), follow=True),
                Rule(SgmlLinkExtractor(allow=['kandidatai/kand_anketa_l_' ]) ,follow=True),
		Rule(SgmlLinkExtractor(allow=['kand_pajam_l_' ]),'parse_deklaracija' ,follow=False)

                        ]

        def parse_deklaracija(self,response):

                hxs = HtmlXPathSelector(response)

		item = KandidatoDeklaracija()
		val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[2].select('td/b/text()').extract()[0].encode('UTF8')).replace(',','.')
		if val.isdigit():
	                item['turtas'] = float(val)
		val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[4].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
		if val.isdigit():
			item['vertybiniai_popieriai'] = float(val)
		val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[6].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
		if val.isdigit():
                        item['gryni_pinigai'] = float(val)
		val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[8].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
		if val.isdigit():
                        item['suteiktos_paskolos'] = float(val)
		val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[10].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
		if val.isdigit():
                        item['gautos_paskolos'] = float(val)

		for i in xrange(14,27,3):
			val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[i].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
			if val.isdigit():
                        	item['gautos_pajamos'] = float(val)
				val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[i+1].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
				
				if val.isdigit():
                        		item['mokesciai'] = float(val)
		"""

		else:
			val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[26].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
			if val.isdigit():
				item['gautos_pajamos'] = float(val)
				val = re.sub('[^0-9,]+', '', hxs.select("//table/tr/td/div/div/table/tr")[27].select('td/b/text()').extract()[0].encode('UTF8').replace(',','.'))
				if val.isdigit():
					item['gautos_pajamos'] = float(val)	
		"""
		item['kandidatas'] = hxs.select("//h4/text()")[0].extract().encode('UTF8')
                yield item
