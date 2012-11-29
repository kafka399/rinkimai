from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatoRezultaiApylinkejeItem
from rinkimai.items import ApylinkeItem
from rinkimai.items import KandidatoRezultaiApygardojeItem
import re

class Vienmandate2004Spider(CrawlSpider):
        name = "vienmandate2004_2"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/rinkimai/2004/seimas/rezultatai/rezv_l_20_2.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['rezultatai/rezv_apg'],deny=['rezultatai/rezv_e_','_apg_e_']), 'parse_apygarda', follow=True),
		Rule(SgmlLinkExtractor(allow=['rezultatai/rezv_apl_l_'],deny=['rezultatai/rezv_e_','_apg_e_']), 'parse_apylinke', follow=False),
		Rule(SgmlLinkExtractor(allow=['rezultatai/rezv_uzs_l_'],deny=['_apg_e_']), 'parse_apygarda', follow=True),
                Rule(SgmlLinkExtractor(allow=['rezultatai/rezv_amb_l_'],deny=['_apg_e_']), 'parse_uzsienio_apylinke', follow=False)
			]

        def parse_apygarda(self,response):

                hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//h4')[0].select('text()').extract()[0].encode('UTF8')
		kandidatai = hxs.select('//div')[1].select('table/tr')
		apylinkes = hxs.select('//div')[2].select('table/tr')

		for kan in kandidatai:
			item = KandidatoRezultaiApygardojeItem()
			item['apygarda'] = apygarda
			if len(kan.select('td/a'))>0:
				item['kandidatas'] = (kan.select('td/a/text()').extract())[0].encode('UTF8')
				item['apylinkese'] =  (kan.select('td/text()').extract()[0]).encode('UTF8')
				item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
				item['nuo_rinkeju'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
				yield item
			if len(kan.select('td/b/a'))>0:
                                item['kandidatas'] = (kan.select('td/b/a/text()').extract())[0].encode('UTF8')
                                item['apylinkese'] =  (kan.select('td/text()').extract()[0]).encode('UTF8')
                                item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8')
                                item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
                                item['nuo_rinkeju'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
                                yield item

		for ap in apylinkes:
	                item = ApylinkeItem()
			item['apygarda'] = apygarda
			if len(ap.select('td/a').extract())>0:
				if len(ap.select('td/a/text()'))>0:
                                        item['apylinke'] = re.sub(r'[\d .  ]','',(ap.select('td/a/text()').extract())[0].encode('UTF8'))
                                        item['rinkeju_skaicius']=(ap.select('td/text()').extract())[1].encode('UTF8')
                                        item['dalyvavo'] = (ap.select('td/text()').extract())[2].encode('UTF8')
                                        item['negaliojantys_biuleteniai'] = (ap.select('td/text()').extract())[4].encode('UTF8')

                                else:
                                        item['apylinke'] = (ap.select('td/a/b/text()').extract())[0].encode('UTF8')
                                        item['rinkeju_skaicius']=(ap.select('td/text()').extract())[0].encode('UTF8')
                                        item['dalyvavo'] = (ap.select('td/text()').extract())[1].encode('UTF8')
                                        item['negaliojantys_biuleteniai'] = (ap.select('td/text()').extract())[3].encode('UTF8')
                                yield item



        def parse_uzsienio_apylinke(self,response):
                hxs = HtmlXPathSelector(response)
                apylinke = hxs.select('//h4/text()').extract()[0].encode('UTF8')
                kandidatai = hxs.select('//table[@class="basic"]/tr')
		apygarda = hxs.select('//h5/a/text()')[1].extract()
                for kan in kandidatai:
                        item = KandidatoRezultaiApylinkejeItem()
                        item['apylinke'] = apylinke
			item['apygarda'] = apygarda
                        if len(kan.select('td'))>0:
				if len(kan.select('td/b'))>0:
					item['kandidatas'] = (kan.select('td/b/text()').extract())[0].encode('UTF8')
                                        item['balsadezeje'] =  (kan.select('td/text()').extract()[0]).encode('UTF8')
                                        item['pastu'] = kan.select('td/text()').extract()[1].encode('UTF8')
                                        item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
                                        item['nuo_rinkeju'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
                                        yield item
				else:
	                                item['kandidatas'] = (kan.select('td/text()').extract())[0].encode('UTF8')
        	                        item['balsadezeje'] =  (kan.select('td/text()').extract()[1]).encode('UTF8')
                	                item['pastu'] = (kan.select('td/text()').extract()[2]).encode('UTF8')
                        	        item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
                                	item['nuo_rinkeju'] = (kan.select('td/text()').extract()[5]).encode('UTF8')
	                                yield item

	def parse_apylinke(self,response):
		hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//h5/a/text()')[1].extract()
		apylinke = hxs.select('//h4/text()')[0].extract()

		kandidatas1 = hxs.select('//table[@class="basic"]').select('tr[@class="r1"]')
		if len(kandidatas1) >0:
			kan=kandidatas1[0]
			item = KandidatoRezultaiApylinkejeItem()
                        item['apylinke'] = apylinke
                        item['apygarda'] = apygarda

			item['kandidatas'] = (kan.select('td/b/text()').extract()[0]).encode('UTF8')
                        item['balsadezeje'] =  (kan.select('td/text()').extract()[0]).encode('UTF8')
                        item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8')
                        item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
                        item['nuo_rinkeju'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
                        yield item
		kandidatas1 = hxs.select('//table[@class="basic"]').select('tr[@class="r2"]')
		if len(kandidatas1) >0:
			kan=kandidatas1[0]
			item = KandidatoRezultaiApylinkejeItem()
                        item['apylinke'] = apylinke
                        item['apygarda'] = apygarda

			item['kandidatas'] = (kan.select('td/text()').extract()[0]).encode('UTF8')
                        item['balsadezeje'] =  (kan.select('td/text()').extract()[1]).encode('UTF8')
                        item['pastu'] = (kan.select('td/text()').extract()[2]).encode('UTF8')
			item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
			item['nuo_rinkeju'] = (kan.select('td/text()').extract()[5]).encode('UTF8')	
			yield item
			"""
		for kan in kandidatai:
			item = KandidatoRezultaiApylinkejeItem()
			item['apylinke'] = apylinke
			item['apygarda'] = apygarda
			if len(kan.select('td[@class="r2"])'))>0:

				item['kandidatas'] = (kan.select('td/text()').extract()[0]).encode('UTF8')+"xxx"
				item['balsadezeje'] =  (kan.select('td/text()').extract()[1]).encode('UTF8')
				item['pastu'] = (kan.select('td/text()').extract()[2]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
				item['nuo_rinkeju'] = (kan.select('td/text()').extract()[5]).encode('UTF8')
				yield item
			if len(kan.select('td[@class="r1"]'))>0:

                                item['kandidatas'] = (kan.select('td/b/text()').extract()[0]).encode('UTF8')+"yyy"
                                item['balsadezeje'] =  (kan.select('td/text()').extract()[0]).encode('UTF8')
                                item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8')
                                item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
                                item['nuo_rinkeju'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
                                yield item
			"""
