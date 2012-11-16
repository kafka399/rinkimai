# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy.contrib.exporter import CsvItemExporter

class RinkimaiPipeline(object):
    def __init__(self):
        self.files = {}

    def spider_closed(self, spider):
        for spider, exporters in self.files.items():
            for item, (exporter, f) in exporters.items():
                exporter.finish_exporting()
                f.close()
        self.files.pop(spider)

    def _exporter(self, item, spider):
        if spider.name not in self.files:
            self.files[spider.name] = {}
        name = item.__class__.__name__.lower()
        if name not in self.files[spider.name]:
            f = open('%s_%s.csv' % (spider.name, name), 'w+b')
            exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.files[spider.name][name] = (exporter, f)
        else:
            exporter, f = self.files[spider.name][name]
        return exporter

    def process_item(self, item, spider):
	    self._exporter(item, spider).export_item(item)
	    return item
