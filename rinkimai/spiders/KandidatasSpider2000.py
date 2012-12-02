# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatasItem
import re

class KandidatasSpider(CrawlSpider):
        name = "kandidatas2000"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/n/rinkimai/20001008/kandapgsarl.htm-13.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['kandvl.htm']), 'parse_kandidatas', follow=False),
		Rule(SgmlLinkExtractor(allow=['kandapgl.htm' ]) ,follow=True)
			]

	def parse_kandidatas(self,response):
		hxs = HtmlXPathSelector(response)
		item = KandidatasItem()
		item['kandidatas'] = hxs.select("//p/font/b/text()").extract()[0].encode('UTF8')
		p=hxs.select("//table/tr[@valign='bottom']/td/p/b/text()").extract()
		issikele = False
		for i in p:
			if i.encode('UTF8').find('Išsikėlė')>-1:		

				item['apygarda'] = (hxs.select("//table/tr[@valign='bottom']/td/p")).select('b/a/text()')[0].extract().encode('UTF8')
				item['iskele'] =i.encode('UTF8')# (hxs.select("//table/tr[@valign='bottom']/td/p/b/text()"))[1].extract().encode('UTF8')#(hxs.select("//table/tr[@valign='bottom']/td/p")).select('b/text()')[3].extract().encode('UTF8')
				issikele = True
				break
		if issikele == False:
			#if (hxs.select("//table/tr[@valign='bottom']/td/p")).select('b/a/text()')[0].extract().encode('UTF8')=='Daugiamandatė':
			if (hxs.select("//table/tr[@valign='bottom']/td/p")).select('b')[0].extract().encode('UTF8').find('Daugiamandatė')>-1:
				p=(hxs.select("//table/tr[@valign='bottom']/td/p"))[1:]
				for i in p:
					if i.extract().encode('UTF8').find('Apygarda')>-1:
						item['apygarda'] = i.select('b/a/text()')[0].extract().encode('UTF8')
				for i in p:
					if i.extract().encode('UTF8').find('Iškėlė')>-1:
						item['iskele'] = i.select('b/a/text()')[1].extract().encode('UTF8')
		
#				item['apygarda'] = (hxs.select("//table/tr[@valign='bottom']/td/p"))[1].select('b/a/text()')[1].extract().encode('UTF8')#(hxs.select("//table/tr[@valign='bottom']/td/p")).select('b/a/text()')[2].extract().encode('UTF8')
			else:
				item['apygarda'] = (hxs.select("//table/tr[@valign='bottom']/td/p")).select('b/a/text()')[0].extract().encode('UTF8')		
				item['iskele'] = hxs.select("//table/tr/td/p/b/a/text()")[1].extract().encode('UTF8')
		p=(hxs.select("//table/tr[@valign='bottom']/td/p"))
		for i in p:
			if i.extract().encode('UTF8').find('Gimimo data:')>-1:
				item['gimimo_data'] = i.select('b/text()')[0].extract().encode('UTF8')
				if len(i.select('b/text()'))>1:
					item['gyvena'] = i.select('b/text()')[1].extract().encode('UTF8')
		p=(hxs.select("//blockquote/p"))
		
		for i in p:
			if i.extract().encode('UTF8').find('Išsilavinimas:')>-1:
				item['issilavinimas']=";".join(i.select('b/text()').extract()).encode('UTF8')
			elif i.extract().encode('UTF8').find('Užsienio kalbos:')>-1:
				item['uzsienio_kalbos']=i.select('b/text()')[0].extract().encode('UTF8')
			elif i.extract().encode('UTF8').find('Šeimyninė padėtis')>-1:
				item['seimynine_padetis'] = i.select('b/text()')[0].extract().encode('UTF8')
			elif i.extract().encode('UTF8').find('Pomėgiai')>-1:
                                item['pomegiai'] = i.select('b/text()')[0].extract().encode('UTF8')	
			elif i.extract().encode('UTF8').find('Pagrindinė darbovietė')>-1:
                                item['darboviete'] = i.select('b/text()')[0].extract().encode('UTF8')
	
		item['neatlikta_bausme'] =(hxs.select("//p/font"))[1].select('b/text()')[0].extract().encode('UTF8') 
		item['sunkus_nusikaltimas']=(hxs.select("//p/font"))[1].select('b/text()')[6].extract().encode('UTF8')
		item['pripazintas_kaltu']=(hxs.select("//p/font"))[1].select('b/text()')[5].extract().encode('UTF8')

		yield item
