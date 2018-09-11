# -*- coding: utf-8 -*-
import js2py
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CnnCrawlerSpider(CrawlSpider):
    name = 'cnn_crawler'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com']

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 60,
        'DOWNLOAD_DELAY': 0.25,
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    rules = (
        Rule(LinkExtractor(allow=r''), callback='parse', follow=True),
    )

    def parse(self, response):
        try:
            script = response.xpath('//script[contains(., "publishDate")]/text()').extract_first()
            context = js2py.EvalJs()
            context.execute(script)
            publish_date = context.CNN.contentModel.analytics.publishDate
        except Exception as e:
            print(e)
            publish_date = None

        i = {'title': response.xpath('//h1[@class="pg-headline"]/text()').extract_first() or \
                      response.xpath('//h1[@class="PageHead__title"]/text()').extract_first() or '',
             'url': response.url, 'publish_date': publish_date}
        if i['title']:
            yield i

        for next_page in response.css('a.nav-section__submenu-item'):
            to = next_page.css('::attr(href)').extract_first()
            if to:
                yield response.follow(response.urljoin(to), self.parse)

        for next_page in response.css('.cd--article h3 a'):
            to = next_page.css('::attr(href)').extract_first()
            if to:
                yield response.follow(response.urljoin(to), self.parse)

        try:
            script = response.xpath('//script[contains(., "articleList")]/text()').extract_first()
            if script is not None:
                context = js2py.EvalJs()
                context.execute(script)
                article_list = context.CNN.contentModel.siblings.articleList
            else:
                article_list = []
        except Exception as e:
            article_list = []

        for next in article_list:
            yield response.follow(response.urljoin(next['uri']), callback=self.parse)


