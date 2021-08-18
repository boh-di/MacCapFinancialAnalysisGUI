#Title: Scanner.py
#Authors: Wanderer and Bohdi
#Date: 02/29/2021
#Purpose:	
# Provide a basic scanner that accepts a ticker input
# and returns the following:
#	- previous close 
# 	- previous open
# 	- days range
# 	- 52 week range
# 	- volume
# 	- avg volume
# 	- mkt cap
# 	- 5y monthly beta
# 	- next earnings date

#import modules
import scrapy
from scrapy.crawler import CrawlerProcess
import Items

class Scanner(scrapy.Spider):
    name = "scanner"

    def parseSum(self, response):
        #Declare the item objects
        items = Items.YahooscrapingItem()
        #Save the extracted data in the item objects
        items['stock_name'] = response.xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1').css('::text').extract()
        items['prev_close'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[1]/td[2]/span').css('::text').extract()
        items['prev_open'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[2]/td[2]/span').css('::text').extract()
        items['range_day'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[5]/td[2]').css('::text').extract()
        items['range_52weeks'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[6]/td[2]').css('::text').extract()
        items['volume'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[7]/td[2]/span').css('::text').extract()
        items['avg_volume'] = response.xpath('//*[@id="quote-summary"]/div[1]/table/tbody/tr[8]/td[2]/span').css('::text').extract()
        items['market_cap'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span').css('::text').extract()
        items['beta_5yr_monthly'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[2]/td[2]/span').css('::text').extract()
        items['earnings_date'] = response.xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[5]/td[2]').css('::text').extract()

        yield items

    def scrapeSum(self):
        symbol = 'AAPL'
        yield scrapy.Request(url=f'https://finance.yahoo.com/quote/{symbol}?p={symbol}', callback=self.parseSum)

#End of Scanner class

if __name__ == "__main__":
    crawler = CrawlerProcess()
    crawler.crawl(Scanner, -o stock.csv)
    crawler.start()