import time
from email.policy import default

import scrapy
from scrapy_DD.items import ScrapyDdItem



class DdbookSpider(scrapy.Spider):
    name = "DDbook"
    allowed_domains = ["search.dangdang.com"]
    start_urls = ["https://search.dangdang.com/?key=%B6%C0%BC%D2&category_path=01.01.00.00.00.00#J_tab"]

    # 解析分类以及提取分类链接
    def parse(self, response):
        category_list = response.xpath("//li[@dd_name='分类']//div[@class='clearfix']//a")
        for category in category_list:
            category_link = 'https://search.dangdang.com' + category.xpath("./@href").get()

            category_name = category.xpath("./@title").get()
            print(f'分类：{category_name}, 链接{category_link}')
            # print(f'分类数量：{len(category_name)},链接数量{len(category_link)}')
            print('------')
            yield scrapy.Request(url=category_link,
                                 callback=self.parse_category,
                                 method="GET",
                                 headers={
                                     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
                                     'Host':'search.dangdang.com',
                                     'Referer':'https://search.dangdang.com/?key=%B6%C0%BC%D2&category_path=01.01.00.00.00.00'
                                 },
                                 meta={'category_name': category_name}
                                )
    # 解析每一页每本书的名字价格等需要提取的数据
    def parse_category(self, response):
        book_list = response.xpath('//div[@id="search_nature_rg"]/ul/li')
        for book in book_list:
            category_name = response.meta['category_name']
            book_name = book.xpath("./a/@title").get(default='暂无书名').strip()
            description = book.xpath("./p[@class='detail']/text()").get(default='暂无简介').strip()
            price = book.xpath("./p[@class='price']/span[1]/text()").get(default='暂无打折价格').strip()
            price = price.replace('¥','').replace('￥','').strip()  # 去掉特殊符号
            # 有其他店铺以及自营店，要做区分。如果没有检测到其他商家，则默认为自营店
            shang_jia = book.xpath("./p[@class='search_shangjia']/a/text()").get(default='自营').strip()
            # 可能有多名作者，所以用.getall提取所有作者，然后用/来拼接他们
            author_parts = book.xpath("./p[@class='search_book_author']/span[1]/a/text()").getall()
            author = '/'.join(author_parts).strip() if author_parts else '暂无作者信息'
            publisher = book.xpath("./p[@class='search_book_author']/span[3]/a/text()").get(default='暂无出版商').strip()
            # print(book_name,description,price,shang_jia,author,publisher)
            # print(f"书名     : {book_name}  ")
            # print(f"简介     : {description[:100]}")  # 简介太长截断显示
            # print(f"价格     : {price}")
            # print(f"商家     : {shang_jia}")
            # print(f"作者     : {author}")
            # print(f"出版社   : {publisher}\n")
            book = ScrapyDdItem(category_name=category_name,book_name=book_name,
                                author=author,price=price,description=description,
                                shang_jia=shang_jia,publisher=publisher)
            yield book

    # 翻页规则
        # 获取“下一页”按钮的url地址
        next_page_url = response.xpath("//li[@class='next']/a/@href").get()
        next_page = response.urljoin(next_page_url)
        # 如果下一页存在，则
        if next_page :
            category_name = response.meta.get('category_name')
            # 当前从未调用过meta值page,所以如果没有page，则默认为1
            current_page = response.meta.get('page', 1)
            print(f'当前分类是：{category_name}')
            print(f'当前页数是：{current_page}')

            yield scrapy.Request(url=next_page, callback=self.parse_category,
                                meta={'page': current_page + 1,'category_name': category_name})
        # 如果下一页不存在，则
        else:
            category_name = response.meta.get('category_name')
            current_page = response.meta.get('page', 1)
            print(f'已全部爬完,最后一个分类是：{category_name}\n最后一页是：{current_page}页')






