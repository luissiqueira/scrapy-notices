import scrapy
import js2py
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class GloboCrawlerSpider(CrawlSpider):
    name = 'globo-spider'
    allowed_domains = ['g1.globo.com']
    start_urls = ['https://g1.globo.com/']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 100,
        'DOWNLOAD_DELAY': 0.25,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    rules = (
        Rule(LinkExtractor(allow=r'/\d+/\d+/\d+/((\w+)-?)*'), callback='parse', follow=True),
    )

    def parse(self, response):

        try:
            script = response.xpath('//script[contains(., "RESOURCE")]/text()').extract_first()
            context = js2py.EvalJs()
            context.execute(script)
            publish_date = context.cdaaas.SETTINGS.RESOURCE.ISSUED
        except Exception as e:
            print(e)
            publish_date = None

        for block in response.css('.content-head__title'):
            if publish_date:
                yield {'title': block.css('::text').extract_first(),
                       'url': response.url,
                       'publish_date': publish_date}

        for next_page in response.css('.feed-post-body a'):
            to = next_page.css('::attr(href)').extract_first()
            if to:
                yield response.follow(to, self.parse)

        for next_page in response.css('.mc-article-body a'):
            to = next_page.css('::attr(href)').extract_first()
            if to:
                yield response.follow(to, self.parse)
