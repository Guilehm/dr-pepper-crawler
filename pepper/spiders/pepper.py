import os

import scrapy

from pepper.items import PepperItem


class PepperSpider(scrapy.Spider):
    name = 'pepper'
    start_urls = ['https://blog.drpepper.com.br']

    def parse(self, response):
        images = response.xpath(
            './/img[contains(@class,"size-full")]'
        )
        images += response.xpath(
            './/img[contains(@class,"alignnone")]'
        )
        images += response.xpath(
            './/img[contains(@src,"/tirinhas/")]'
        )
        images = set(images)

        for img in images:
            link = img.xpath('./@src').get()
            yield PepperItem(
                name=os.path.basename(link),
                description=img.xpath('./parent::p/text()').get(),
                link=link,
                image_urls=[link],
            )

        current_page = response.xpath('//span[@class="page-numbers current"]')
        next_page = current_page.xpath('./parent::li/following-sibling::li[1]/a/@href').get()

        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)
