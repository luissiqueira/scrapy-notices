import scrapy
import js2py


class GloboSpider(scrapy.Spider):
    name = 'globo-spider'
    start_urls = ['https://g1.globo.com/']

    def parse(self, response):
        script = response.xpath('//script[contains(., "RESOURCE")]/text()').extract_first()

        try:
            context = js2py.EvalJs()
            context.execute(script)
            publish_date = context.cdaaas.SETTINGS.RESOURCE.ISSUED
        except Exception as e:
            print(e)
            publish_date = None

        for block in response.css('.content-head__title'):
            yield {'title': block.css('::text').extract_first(),
                   'url': response.url,
                   'publish_date': publish_date}

        for next_page in response.css('.feed-post-body a'):
            yield response.follow(next_page, self.parse)
