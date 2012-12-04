# coding: utf-8

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from rinkimai.items import KandidatasItem
from rinkimai.items import KandidatoDeklaracija
import re

class KandidatoDeklaracijaSpider(CrawlSpider):
        name = "kandidatoDeklaracija2000"

        allowed_domains = ["www3.lrs.lt"]
	start_urls = ["http://www3.lrs.lt/n/rinkimai/20001008/partsarl.htm-13.htm","http://www3.lrs.lt/n/rinkimai/20001008/kandapgsarl.htm-13.htm"]
        rules =[Rule(SgmlLinkExtractor(allow=['kandvl.htm']), 'parse_kandidatas', follow=False),
                Rule(SgmlLinkExtractor(allow=['kandapgl.htm' ]) ,follow=True),
		Rule(SgmlLinkExtractor(allow=['kandpartl.htm' ]) ,follow=True)
                        ]

        def parse_kandidatas(self,response):
                hxs = HtmlXPathSelector(response)
                item = KandidatoDeklaracija()
                item['turtas'] = float(hxs.select("//table")[3].select('tr')[1].select('td/b/text()')[2].extract().replace(' Lt',''))
                item['kandidatas'] = hxs.select("//p/font/b/text()").extract()[0].encode('UTF8')
                item['gautos_pajamos'] = float(hxs.select("//table")[2].select('tr')[2].select('td/b/text()')[0].extract().replace(' Lt',''))
                item['mokesciai'] = float(hxs.select("//table")[2].select('tr')[2].select('td/b/text()')[1].extract().replace(' Lt',''))

                yield item

