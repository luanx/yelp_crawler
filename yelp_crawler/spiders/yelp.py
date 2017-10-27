from scrapy import Spider, Selector, Request

from yelp_crawler.items import YelpItem
from yelp_crawler.utils.select_result import list_first_item, clean_url


class YelpSpider(Spider):

    name = "yelp"
    allowed_domains = ["yelp.com"]
    start_urls = [
        "https://www.yelp.com/search?find_desc=outdoor+gear&find_loc=San+Francisco%2C+CA&ns=1"
    ]

    def parse(self, response):

        response_selector = Selector(response)
        next_link = list_first_item(response_selector.xpath(u'//div[@class="arrange_unit"]/a[contains(@class,"u-decoration-none next pagination-links_anchor")]/@href').extract())
        if next_link:
            next_link = clean_url(response.url, next_link, response.encoding)
            yield Request(url=next_link, callback=self.parse)

        for detail_link in response_selector.xpath(u'//a[contains(@class, "biz-name js-analytics-click")]/@href').extract():
            if detail_link:
                detail_link = clean_url(response.url, detail_link, response.encoding)
                yield Request(url=detail_link, callback=self.parse_detail)


    def parse_detail(self, response):
        yelp_item = YelpItem()

        response_selector = Selector(response)
        yelp_item['name'] = list_first_item(response_selector.xpath(u'//h1[contains(@class, "biz-page-title embossed-text-white shortenough")][1]/text()').extract())
        yelp_item['url'] = list_first_item(response_selector.xpath(u'//span[@class="biz-website js-add-url-tagging"][1]/a/text()').extract())

        yield yelp_item