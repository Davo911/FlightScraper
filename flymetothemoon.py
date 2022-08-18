import scrapy
import selenium
import sys

# Input paramters
if sys.argv < 5:
    print("Usage: python3 flymetothemoon.py <origin-code> <destination-code> <start-date:YYMMDD> <end-date:YYMMDD> <tolerance>")
    print("Example usage: python3 flymetothemoon.py FFM HAN 221121 221130 5")
    sys.exit(1)

base_url = "https://www.skyscanner.de/transport/fluge/"
origin = sys.argv[1]
destination = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]
tolerance = sys.argv[5]
urls = []

for i in range(tolerance):
    urls.append(base_url + origin + "/" + destination + "/" + start_date + "/" + end_date)

#visit website and scrape data
class SkyscannerSpider(scrapy.Spider):
    name = "skyscanner"
    start_urls = urls

    def parse(self, response):
        for flight in response.css('div.flight-list-item'):
            yield {
                'price': flight.css('div.price::text').extract_first(),
                'departure': flight.css('div.departure::text').extract_first(),
                'arrival': flight.css('div.arrival::text').extract_first(),
                'duration': flight.css('div.duration::text').extract_first(),
                'airline': flight.css('div.airline::text').extract_first(),
                'url': response.url,
            }
            

#https://www.skyscanner.de/transport/fluge/fra/han/221121/221130/?inboundaltsenabled=true&outboundaltsenabled=true&ref=home
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')