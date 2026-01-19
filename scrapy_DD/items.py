# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDdItem(scrapy.Item):
    category_name = scrapy.Field() # 青春文学分类
    # category_link = scrapy.Field()# 青春文学分类链接
    book_name = scrapy.Field() # 书名
    author = scrapy.Field() # 作者
    price = scrapy.Field()  # 价格
    publisher = scrapy.Field()
    description = scrapy.Field() # 简介
    shang_jia = scrapy.Field() # 商家




    pass
