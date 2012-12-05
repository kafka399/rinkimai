# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatasItem
import re

class KandidatasDaugiamandateSpider(CrawlSpider):
        name = "kandidatasDaugiamandate2004"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/rinkimai/2004/seimas/kandidatai/part_sar_l_20.htm"]

	rules =[Rule(SgmlLinkExtractor(allow=['kandidatai/kand_anketa_l_']), 'parse_kandidatas', follow=False),
		Rule(SgmlLinkExtractor(allow=['kand_part_l_' ]) ,follow=True)
			]

	def parse_kandidatas(self,response):
		
		hxs = HtmlXPathSelector(response)
		item = KandidatasItem()
		item['kandidatas'] = hxs.select("//h4")[1].select('text()')[0].extract().encode('UTF8')
		td= hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']/table/tr/td").extract()
		for t in td:
			t = t.encode('UTF8')
			ln =t.find('Apygarda')
			if ln > -1:
			        t=t[ln+len('Apygarda: <b>'):]
				if t.find('<a href')==0:
                                        t = t[t.find('.htm">')+len('.htm">'):]
					item['apygarda'] = t[:t.find('</a>')]
				else:
					item['apygarda'] = t[:t.find('</b>')]
		
		for t in td:
			t = t.encode('UTF8')
			ln =t.find('Iškėlė')
			if ln > -1:
        	                t=t[ln+len('Iškėlė: <b>'):]
				if t.find('<a href')<15:
	                                t = t[t.find('.htm">')+len('.htm">'):]
        	                        item['iskele'] =  t[:t.find('</a>')]
				else:
                	        	item['iskele'] = t[:t.find('</b>')]

		"""
		if len(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']/table/tr/td")[1].select('b/a/text()'))>1:
			item['iskele'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']/table/tr/td")[1].select('b/a/text()')[1].extract().encode('UTF8')
			item['apygarda'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']/table/tr/td/b/a/text()")[1].extract().encode('UTF8')
		else:
			item['iskele'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']/table/tr/td")[1].select('b/text()')[1].extract().encode('UTF8')
			item['apygarda'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']/table/tr/td/b/a/text()")[0].extract().encode('UTF8')
		"""
		#if len(hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[1].select('tr/td/table'))>0:
		#	item['issilavinimas'] = ';'.join(hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[1].select('tr/td/table')[0].select('tr/td/b/text()').extract())

		#rez=hxs.select("//div[@class='candidateInfo']/table[@class='partydata']")[1].select('tr/td').extract()[0].encode('UTF8')
		#rez=str(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']").extract()).encode('UTF8')

		item['gimimo_data'] =hxs.select("//td[@class='bigcell']/table/tr[@class='r1']/td[@class='lt']")[0].select('b/text()').extract()[0].encode('UTF8')
		item['gyvena'] =hxs.select("//td[@class='bigcell']/table/tr[@class='r2']/td[@class='lt']")[0].select('b/text()').extract()[0].encode('UTF8')

		i=3	
		
		if re.search('^\r\n\d{1,2}\.',hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('text()').extract()[0].encode('UTF8')) ==None:
			i+=1
		item['neatlikta_bausme'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')
		
		i+=5
		if re.search('^\r\n\d{1,2}\.',hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('text()').extract()[0].encode('UTF8')) ==None:
			i+=1
		item['pripazintas_kaltu']=hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')
		i+=1

		if re.search('^\r\n\d{1,2}\.',hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('text()').extract()[0].encode('UTF8')) ==None:
			i+=1
		item['sunkus_nusikaltimas']=hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')
		i+=1
		if re.search('^\r\n\d{1,2}\.',hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('text()').extract()[0].encode('UTF8')) ==None:
			i+=1
		item['gimimo_vieta']=hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8') 
		i+=1

		if re.search('^\r\n\d{1,2}\.',hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('text()').extract()[0].encode('UTF8')) ==None:
			i+=1

		item['tautybe'] =hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')
		i+=1

		if len(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('table/tr'))>0:
			item['issilavinimas']=";".join(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('table/tr').select('td[@class="ltb"]/b/text()').extract()).encode('UTF8')
		i+=1

		if len(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()'))>0:
			item['uzsienio_kalbos']=";".join(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()).encode('UTF8')
		i+=3

		if len(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()'))>0:
			item['darboviete'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')
		i+=2	
		if len(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()'))>0:
			item['pomegiai'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')
		i+=1
		if len(hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()'))>0:
			item['seimynine_padetis'] = hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')


		"""
		f rez.find('13. Kokias užsienio kalbas mokate <b>')>0		if rez.find('16. Pagrindin')>0:
			rez = rez[rez.find('16. Pagrindin')+len('16. Pagrindin')+28:]
			item['darboviete'] = rez[0:rez.find('</b>')]
		if rez.find('18. Pom')>0:
			rez = rez[rez.find('18. Pom')+len('18. Pom')+10:]
			item['pomegiai'] = rez[0:rez.find('</b>')]
		if rez.find('19. Šeiminė padėtis')>0:
			rez = rez[rez.find('19. Šeiminė padėtis')+len('18. Šeiminė padėtis <b>'):]
			item['seimynine_padetis'] = rez[0:rez.find('</b>')]
		"""
		yield item

