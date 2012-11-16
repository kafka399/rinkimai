# Scrapy settings for rinkimai project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'rinkimai'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['rinkimai.spiders']
NEWSPIDER_MODULE = 'rinkimai.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 0.25
ITEM_PIPELINES = ['rinkimai.pipelines.RinkimaiPipeline']
