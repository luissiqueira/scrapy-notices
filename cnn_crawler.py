import scrapy
import js2py


class CNNSpider(scrapy.Spider):
    name = 'cnn-spider'
    start_urls = ['https://money.cnn.com/technology/startups/']

    def parse(self, response):
        script = response.xpath('//script[contains(., "cnnPublishDate")]/text()').extract_first()

        try:
            context = js2py.EvalJs()
            context.execute(script)
            publish_date = context.cnnPublishDate
        except Exception as e:
            print(e)
            publish_date = None

        for block in response.css('.article-title a'):
            yield {'title': block.css('::text').extract_first(),
                   'url': response.url,
                   'publish_date': publish_date}

        for next_page in response.css('.eq-summary-large a'):
            yield response.follow(next_page, self.parse)
