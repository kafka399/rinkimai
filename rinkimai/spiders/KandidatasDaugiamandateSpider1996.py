# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatasItem
import re

class KandidatasDaugiamandateSpider(CrawlSpider):
        name = "kandidatasDaugiamandate1996"
        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/n/rinkimai/seim96/rdl.htm"]
	rules =[Rule(SgmlLinkExtractor(allow=['kandvl.htm']), 'parse_kandidatas', follow=False),
		Rule(SgmlLinkExtractor(allow=['rkreitl.htm' ]) ,follow=True),

			]

	def parse_kandidatas(self,response):
		hxs = HtmlXPathSelector(response)
		item = KandidatasItem()
		item['kandidatas'] = hxs.select("//p/font/b/text()").extract()[0].encode('UTF8')
		p=hxs.select("//blockquote").extract()
		for t in p:
                        t = t.encode('UTF8')
                        ln =t.find('Apygarda')
                        if ln > -1:
                                t=t[ln+len('Apygarda: <b>'):]
                                if t.find('<a href')==0:
                                        t = t[t.find('">')+len('">'):]
                                        item['apygarda'] = t[:t.find('</a>')]
                                else:
                                        item['apygarda'] = t[:t.find('</b>')]

		for t in p:
                        t = t.encode('UTF8')
                        ln =t.find('Iškėlė')
                        if ln > -1:
                                t=t[ln+len('Iškėlė:'):]
                                # if t.find('<a href')<15:
                                t = t[t.find('<b>')+len('<b>'):]
                                item['iskele'] =  t[:t.find('</b>')]
                                #else:
                                 #       item['iskele'] = t[:t.find('</b>')]

#		item['apygarda'] = hxs.select("//b/a")[0].select('text()').extract()[0].encode('UTF8')
		#if len(hxs.select("//b/a"))>2:
		#	item['iskele'] = hxs.select("//b/a")[1].select('text()').extract()[0].encode('UTF8')
		#else:
		#	item['iskele'] = hxs.select("//b")[2].select('text()').extract()[0].encode('UTF8')
		p_block = hxs.select("//blockquote/p")
		#p_text =  hxs.select("//blockquote/p/b/text()")
		for p in p_block:
			if (p.extract().encode('UTF8').find('Šeimyninė padėtis:'))>0:
				item['seimynine_padetis'] = p.select('b/text()').extract()[0].encode('UTF')
			if (p.extract().encode('UTF8').find('Užsienio kalbos:'))>0:
				item['uzsienio_kalbos']=";".join(p.select('b/text()').extract()).encode('UTF')
			if (p.extract().encode('UTF8').find('Išsilavinimas:'))>0:
				item['issilavinimas']= p.select('b/text()').extract()[0].encode('UTF')
		yield item
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
			item['uzsienio_kalbos']=hxs.select("//td[@class='bigcell']/table/tr/td[@class='lt']")[i].select('b/text()').extract()[0].encode('UTF8')
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

