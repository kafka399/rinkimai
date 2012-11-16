from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatoRezultaiApylinkejeItem
from rinkimai.items import ApylinkeItem
from rinkimai.items import KandidatoRezultaiApygardojeItem
import re

class ApylinkeSpider(CrawlSpider):
        name = "apylinke"
        allowed_domains = ["www.vrk.lt"]
	start_urls = ["http://www.vrk.lt/2012_seimo_rinkimai/output_lt/rezultatai_vienmand_apygardose/rezultatai_vienmand_apygardose1turas.html"]
	rules =[Rule(SgmlLinkExtractor(allow=['/rezultatai_vienmanate_apygarda'],deny=['output_en']), 'parse_apygarda', follow=True),
		Rule(SgmlLinkExtractor(allow=['/rezultatai_vienmand_apygardose/rezultatai_apylinke'],deny=['output_en']), 'parse_apygarda_rez', follow=False)

			]

        def parse_apygarda(self,response):

                hxs = HtmlXPathSelector(response)
		apygarda = hxs.select('//h2')[0].select('text()').extract()[0].encode('UTF8')
		apylinkes = hxs.select('//table[@class="partydata"]')[3].select('tr')
		kandidatai = hxs.select('//table[@class="partydata"]')[2].select('tr')
		for kan in kandidatai:
			item = KandidatoRezultaiApygardojeItem()
			item['apygarda'] = apygarda
			if len(kan.select('td/a/text()').extract())>0:
				item['kandidatas'] = (kan.select('td/a/text()').extract())[0].encode('UTF8')
				item['apylinkese'] =  (kan.select('td/text()').extract()[2]).encode('UTF8')
				item['pastu'] = (kan.select('td/text()').extract()[3]).encode('UTF8')
				item['nuo_galiojanciu_biuleteniu'] = (kan.select('td/text()').extract()[5]).encode('UTF8')
				item['nuo_rinkeju'] = (kan.select('td/text()').extract()[6]).encode('UTF8')
				yield item

		for ap in apylinkes:
	                item = ApylinkeItem()
			item['apygarda'] = apygarda
			if len(ap.select('td/a/text()').extract())>0:
				item['apylinke'] = re.sub(r'[\d .  ]','',(ap.select('td/a/text()').extract())[0].encode('UTF8'))
				item['rinkeju_skaicius']=(ap.select('td/text()').extract())[2].encode('UTF8')
				item['dalyvavo'] = (ap.select('td/text()').extract())[3].encode('UTF8')
				item['negaliojantys_biuleteniai'] = (ap.select('td/text()').extract())[5].encode('UTF8')
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
