# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JournalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    journal_name = scrapy.Field()
    current_volume_name = scrapy.Field()
    current_issue_index = scrapy.Field()
    current_issue_link = scrapy.Field()
    article_link = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    abstract = scrapy.Field()
    doi = scrapy.Field()

    



