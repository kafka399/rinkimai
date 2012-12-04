# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatoDeklaracija
import re

class KandidatoDeklaracijaSpider(CrawlSpider):
        name = "kandidatoDeklaracija2012"
        allowed_domains = ["www.vrk.lt"]
	start_urls = ["http://www.vrk.lt/rinkimai/416_lt/KandidatuSarasai/index.html","http://www.vrk.lt/rinkimai/416_lt/Kandidatai/"]
        rules =[Rule(SgmlLinkExtractor(allow=[r'Kandidato\d+Anketa.html$'],deny=['output_en']), follow=True),
                Rule(SgmlLinkExtractor(allow=['KandidataiApygardos' ]) ,follow=True),
		Rule(SgmlLinkExtractor(allow=[r'Kandidato\d+Deklaracijos.html$' ]),'parse_deklaracija' ,follow=False),
		Rule(SgmlLinkExtractor(allow=['RinkimuOrganizacija' ]) ,follow=True)
                        ]

        def parse_deklaracija(self,response):

                hxs = HtmlXPathSelector(response)

		item = KandidatoDeklaracija()
                item['turtas'] = float(re.sub('[^0-9,]+', '', hxs.select("//table[@class='partydata']/tr/td/table[@class='partydata']")[0].select('tr/td/b/text()').extract()[2].encode('UTF8')).replace(',','.'))
		item['vertybiniai_popieriai'] = float(re.sub('[^0-9,]+', '', hxs.select("//table[@class='partydata']/tr/td/table[@class='partydata']")[0].select('tr/td/b/text()').extract()[3].encode('UTF8')).replace(',','.'))
		item['gryni_pinigai'] = float(re.sub('[^0-9,]+', '', hxs.select("//table[@class='partydata']/tr/td/table[@class='partydata']")[0].select('tr/td/b/text()').extract()[4].encode('UTF8')).replace(',','.'))
		item['suteiktos_paskolos'] = float(re.sub('[^0-9,]+', '', hxs.select("//table[@class='partydata']/tr/td/table[@class='partydata']")[0].select('tr/td/b/text()').extract()[5].encode('UTF8')).replace(',','.'))

		item['gautos_paskolos'] = float(re.sub('[^0-9,]+', '', hxs.select("//table[@class='partydata']/tr/td/table[@class='partydata']")[0].select('tr/td/b/text()').extract()[6].encode('UTF8')).replace(',','.')) 
		item['gautos_pajamos'] = re.sub('[^0-9,]+', '', hxs.select("//table[@class='partydata']/tr/td/table[@class='partydata']")[1].select('tr/td/b/text()').extract()[2].encode('UTF8')).replace(',','.')
		item['mokesciai'] = re.sub('[^0-9,]+', '', hxs.select("//table[@class='partydata']/tr/td/table[@class='partydata']")[1].select('tr/td/b/text()').extract()[3].encode('UTF8')).replace(',','.')
                item['kandidatas'] =hxs.select("//table[@class='partydata']")[0].select('tr')[0].select('td/b/text()')[0].extract().encode('UTF8') 

                yield item
