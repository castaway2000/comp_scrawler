# -*- coding: utf-8 -*-
import scrapy
import json
import logging

from ..items import BnbtutorialItem


QUERY = 'Seoul--South-Korea'

# class BnbspiderSpider(scrapy.Spider):
class BnbSpider(scrapy.Spider):
    name = "bnbspider"
    # allowed_domains = ["airbnb.com"]
    start_urls = (
        'https://www.airbnb.com/s/'+QUERY,
    )

    def parse(self, response):
        last_page_number = 17
        if last_page_number < 1:
            return
        else:
            page_urls = [response.url + "?section_offset=" + str(pageNumber)
                     for pageNumber in range(last_page_number)]
            for page_url in page_urls:
                yield scrapy.Request(page_url,
                                    callback=self.parse_listing_results_page)


    def parse_listing_results_page(self, response):
        room_url_parts = set(response.xpath('//div/a[contains(@href,"rooms")]/@href').extract())
        for href in list(room_url_parts):
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_listing_contents)


    def parse_listing_contents(self, response):
        item = BnbtutorialItem()

        json_array = response.xpath('//meta[@id="_bootstrap-room_options"]/@content').extract()
        if json_array:
            airbnb_json_all = json.loads(json_array[0])
            airbnb_json = airbnb_json_all['airEventData']
        item['url'] = response.url
        yield item


    def last_pagenumer_in_search(self, response):
        try:  # to get the last page number
            last_page_number = int(response
            					   .xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href')
                                   .extract()[0]
                                   .split('section_offset=')[1]
                                   )
            print(response.xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href'))
            return last_page_number

        except KeyError:  # if there is no page number
            # get the reason from the page
            reason = response.xpath('//p[@class="text-lead"]/text()').extract()
            # and if it contains the key words set last page equal to 0
            if reason and ('find any results that matched your criteria' in reason[0]):
                logging.log(logging.DEBUG, 'No results on page' + response.url)
                return 0
            else:
            # otherwise we can conclude that the page
            # has results but that there is only one page.
                return 1
