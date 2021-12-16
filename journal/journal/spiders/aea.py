import scrapy
from journal.items import JournalItem

class AeaSpider(scrapy.Spider):
    name = 'aea'
    allowed_domains = ['aeaweb.org']
    start_urls = ['https://www.aeaweb.org/journals']

    # 解析一级页面url并传给下一个方法
    def parse(self, response):
        journal_link_list = response.xpath('//section/article/h2/a/@href').getall()
        for journal_link in journal_link_list:
            # 交给调度器
            journal_full_link = "https://www.aeaweb.org"+journal_link
            yield scrapy.Request(
                url = journal_full_link,
                callback= self.parse_journal_html
            )
        
    
    def parse_journal_html(self, response):
        item = JournalItem() #JournalItem实例化
        # 提取journal_name和current_issue的url
        item['journal_name']=response.xpath('//section/h1/text()').get()
        current_issue_full_link = "https://www.aeaweb.org"+response.xpath('//section/div/a/@href').get()
        item['current_issue_link'] = current_issue_full_link
        yield scrapy.Request(
            url = item['current_issue_link'],
            meta = {'item': item},
            callback = self.parse_issue_html
        )

    def parse_issue_html(self, response):
        article_link_list = response.xpath('//article/h3/a/@href').getall()
        for article_link in article_link_list:
            item = response.meta['item']
            article_full_link = "https://www.aeaweb.org"+article_link
        
            yield scrapy.Request(
                url = article_full_link,
                meta = {'item': item},
                callback = self.parse_article_html
            )

    def parse_article_html(self, response):
        item = response.meta['item']
        item['article_link'] = response.url
        item['title'] = response.xpath('//section/h1/text()').get()
        item['abstract'] = response.xpath('normalize-space(//section[@class="article-information abstract"]/text()[2])').get()
        item['doi']  = response.xpath('//span[@class="doi"]/text()').get()
        item['current_issue_index'] = response.xpath('normalize-space(//span[@class = "vol"]/text()[1])').get()

        author_list = response.xpath('//section/ul/li[@class="author"]/text()').getall()
        author_clean_list = [x.strip() for x in author_list if x.strip() != '']
        item['authors'] = '; '.join(author_clean_list)
        

        yield item