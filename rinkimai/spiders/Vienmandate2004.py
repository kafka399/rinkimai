from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatoRezultaiApylinkejeItem
from rinkimai.items import ApylinkeItem
from rinkimai.items import KandidatoRezultaiApygardojeItem
import re

class VienmandateSpider(CrawlSpider):
        name = "vienmandate2004"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/rinkimai/2004/seimas/rezultatai/rezv_l_20_1.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['rezultatai/rezv_apg'],deny=['_apg_e_']), 'parse_apygarda', follow=True),
		Rule(SgmlLinkExtractor(allow=['/rezultatai_vienmand_apygardose/rezultatai_apylinke'],deny=['_apg_e_']), 'parse_apygarda_rez', follow=False),
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
			if len(kan.select('td/a/text()').extract())>0:
				item['kandidatas'] = (kan.select('td/a/text()').extract())[0].encode('UTF8')
				item['apylinkese'] =  (kan.select('td/text()').extract()[0]).encode('UTF8')
				item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
				item['nuo_rinkeju'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
				yield item
		
		for ap in apylinkes:
	                item = ApylinkeItem()
			item['apygarda'] = apygarda
			if len(ap.select('td/a'))>0:
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
		for kan in kandidatai:
			item = KandidatoRezultaiApylinkejeItem()
			item['apylinke'] = apylinke
			if len(kan.select('td'))>0:
				item['kandidatas'] = (kan.select('td/text()').extract())[0].encode('UTF8')
                                item['balsadezeje'] =  (kan.select('td/text()').extract()[1]).encode('UTF8')
                                item['pastu'] = (kan.select('td/text()').extract()[2]).encode('UTF8')
                                item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
                                item['nuo_rinkeju'] = (kan.select('td/text()').extract()[5]).encode('UTF8')
                                yield item	

	def parse_apygarda_rez(self,response):
		hxs = HtmlXPathSelector(response)
		apylinke = hxs.select('//h2')[0].select('text()').extract()[0].encode('UTF8')
		kandidatai = hxs.select('//table[@class="partydata"]')[1].select('tr')
		for kan in kandidatai:
			item = KandidatoRezultaiApylinkejeItem()
			item['apylinke'] = apylinke
			if len(kan.select('td/a/text()').extract())>0:
				item['kandidatas'] = (kan.select('td/a/text()').extract())[0].encode('UTF8')
				item['balsadezeje'] =  (kan.select('td/text()').extract()[0]).encode('UTF8')
				item['pastu'] = (kan.select('td/text()').extract()[1]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
				item['nuo_rinkeju'] = (kan.select('td/text()').extract()[4]).encode('UTF8')
				yield item
