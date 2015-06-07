from scrapy import Spider
from scrapy.selector import Selector

from stack.items import VideoItem


class StackSpider(Spider):
    name = "youtube"
    allowed_domains = ["youtube.com"]
    start_urls = [
        "https://youtube.com/results?search_query=skatboard&page=1",
    ]

    def parse(self, response):
        print 'url: ', response.url
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
