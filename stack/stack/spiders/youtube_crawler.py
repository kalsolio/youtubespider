# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from stack.items import StackItem
from stack.items import VideoItem


class QuestionsSpider(CrawlSpider):
    name = 'youtube_crawler'
    allowed_domains = ['youtube.com']
    start_urls = [
        'https://youtube.com/results?search_query=skateboard&page=1'
    ]
    rules = [
        Rule(LinkExtractor(allow=r'results\?search_query=skateboard&page=[0-9]'),
             callback='parse_item_new', follow=True)
    ]

    def parse_item(self, response):
        print '=====> url: ', response.url
        questions = response.xpath('//div[@class="summary"]/h3')
        print '=====> question size: ', len(questions)
        for question in questions:
            item = StackItem()
            item['url'] = question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            yield item

    def parse_item_new(self, response):
        print '==========> url: ', response.url
        video_list = Selector(response).xpath('//div[@class="yt-lockup-byline"]')
        print 'size: ', len(video_list)
        my_domain = self.get_domain_from_url(response.url)
        for video in video_list:
            item = VideoItem()
            item['author'] = video.xpath('a/text()').extract()[0]
            item['url'] = my_domain + video.xpath('a/@href').extract()[0]
            yield item

    def get_domain_from_url(self, url):
        from urlparse import urlparse
        parsed_uri = urlparse(url)
        my_domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return my_domain