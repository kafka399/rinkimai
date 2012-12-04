# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatasItem
from rinkimai.items import KandidatoDeklaracija
import re

class KandidatoDeklaracijaSpider(CrawlSpider):
        name = "kandidatoDeklaracija1996"

        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/n/rinkimai/seim96/apgseiml.htm-1.htm"]
        rules =[Rule(SgmlLinkExtractor(allow=['kpdl.htm']), 'parse_deklaracija', follow=False),
                Rule(SgmlLinkExtractor(allow=['kandvl.htm' ]) ,follow=True),
		Rule(SgmlLinkExtractor(allow=['apgtl.htm' ]) ,follow=True)

                        ]

        def parse_deklaracija(self,response):
                hxs = HtmlXPathSelector(response)
                item = KandidatoDeklaracija()
                item['turtas'] = float((hxs.select("//table/tr")[4].select('td/b/text()')[1]).extract().encode('UTF8').replace(' Lt','')) 
                item['kandidatas'] = hxs.select('//blockquote/p/b/text()')[0].extract().encode('UTF8') 
                item['gautos_pajamos'] = float((hxs.select("//table/tr")[2].select('td/b/text()')[0]).extract().encode('UTF8'))
		item['mokesciai'] =float((hxs.select("//table/tr")[2].select('td/b/text()')[1]).extract().encode('UTF8'))

                yield item

