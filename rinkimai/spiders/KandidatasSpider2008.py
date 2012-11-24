# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatasItem
import re

class KandidatasVienmandateSpider(CrawlSpider):
        name = "kandidatas2008"
        allowed_domains = ["www.vrk.lt"]
	start_urls = ["http://www.vrk.lt/rinkimai/400_lt/Kandidatai/index.html"]
	rules =[Rule(SgmlLinkExtractor(allow=['/Kandidatai/Kandidatas'],deny=['output_en']), 'parse_kandidatas', follow=False),
		Rule(SgmlLinkExtractor(allow=['KandidataiApygardos' ]) ,follow=True)
			]

	def parse_kandidatas(self,response):
		hxs = HtmlXPathSelector(response)
		item = KandidatasItem()
		if len(hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td'))>1:
			item['kandidatas'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/text()')[0].extract().encode('UTF8')
		else:
			hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[0].select('b/text()')[0].extract().encode('UTF8')

		if len(hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/a/text()'))>=2:
			item['iskele'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/a/text()')[1].extract().encode('UTF8')
		else:
			item['iskele'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/text()')[2].extract().encode('UTF8')
		if len(hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/text()'))>3:
			item['saraso_numeris'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/text()')[3].extract().encode('UTF8')
		item['apygarda'] = hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[0].select('tr/td')[1].select('b/a/text()')[0].extract().encode('UTF8')
		if len(hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[1].select('tr/td/table'))>0:
			item['issilavinimas'] = ';'.join(hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[1].select('tr/td/table')[0].select('tr/td/b/text()').extract())

		rez=hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[1].select('tr/td').extract()[0].encode('UTF8')
		item['gimimo_data'] = rez[rez.rfind('Gimimo data <b>')+len('Gimimo data <b>'):rez.find('Gimimo data <b>')+10+len('Gimimo data <b>')]
		rez = rez[rez.rfind('gyvenamosios vietos adresas <b>')+len('gyvenamosios vietos adresas <b>'):]
		item['gyvena'] = rez[0:rez.find('</b>')]
		rez=rez[rez.find('8.1 Ar turite nebaigtą atlikti teismo nuosprendžiu paskirtą bausmę?')+len('8.1 Ar turite nebaigtą atlikti teismo nuosprendžiu paskirtą bausmę?  <b>')+14:]
		item['neatlikta_bausme'] = rez[:7]
		rez=rez[rez.find('9.2 Ar buvote po 1990 m. kovo 11 d. Lietuvos Respublikos teismo įsiteisėjusiu nuosprendžiu pripažintas kaltu dėl nusikalstamos veikos?')+len('9.2 Ar buvote po 1990 m. kovo 11 d. Lietuvos Respublikos teismo įsiteisėjusiu nuosprendžiu pripažintas kaltu dėl nusikalstamos veikos?')+13:]
		item['pripazintas_kaltu'] = rez[:2]
		rez=rez[rez.find('9.3 Ar buvote įsiteisėjusiu teismo nuosprendžiu bet kada pripažintas kaltu padaręs sunkų ar labai sunkų nusikaltimą?')+len('9.3 Ar buvote įsiteisėjusiu teismo nuosprendžiu bet kada pripažintas kaltu padaręs sunkų ar labai sunkų nusikaltimą?')+13:]
		item['sunkus_nusikaltimas'] = rez[:2] 

		rez = rez[rez.find('Gimimo vieta <b>')+len('Gimimo vieta <b>'):]
		item['gimimo_vieta'] = rez[0:rez.find('</b>')]
		rez = rez[rez.find('11. Tautyb')+len('11. Tautyb')+6:]
		item['tautybe'] = rez[0:rez.find('\r\n')]
		if rez.find('13. Kokias užsienio kalbas mokate <b>')>0:
			rez = rez[rez.find('13. Kokias užsienio kalbas mokate <b>')+len('13. Kokias užsienio kalbas mokate <b>'):]
			item['uzsienio_kalbos']=rez[0:rez.find('</b>')]
		if rez.find('16. Pagrindin')>0:
			rez = rez[rez.find('16. Pagrindin')+len('16. Pagrindin')+28:]
			item['darboviete'] = rez[0:rez.find('</b>')]
		if rez[rez.find('18. Pom')]>0:
			rez = rez[rez.find('18. Pom')+len('18. Pom')+10:]
			item['pomegiai'] = rez[0:rez.find('</b>')]
		if rez.find('19. Šeiminė padėtis')>0:
			rez = rez[rez.find('19. Šeiminė padėtis')+len('18. Šeiminė padėtis <b>'):]
			item['seimynine_padetis'] = rez[0:rez.find('</b>')]
		yield item

