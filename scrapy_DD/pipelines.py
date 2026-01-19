# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from enum import unique

from itemadapter import ItemAdapter
import csv
import os
import time



class ScrapyDdPipeline:
    def __init__(self):
        self.files = {}
        self.writers = {}
        self.headers = ['类别', '书名', '作者', '价格', '出版社', '商家', '简介']
        self.total_count = 0 # 统计总书籍数
        self.seen = set()

    # def open_spider(self, spider):
    #     self.books = []
    #     self.file = open('青春文学类书籍.csv', 'w',encoding='utf-8-sig',newline='')
    #     self.headers = ['类别','书名','作者','价格','出版社','商家','简介']
    #     self.write = csv.DictWriter(self.file,fieldnames=self.headers)
    #     self.write.writeheader()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # ！！！！若以书籍名称来命名，那么该名称中不能有/或\，不然文件名不合规范，直接不处理
        category = adapter.get('category_name').replace('/','、').strip() # 获取分类名字
        if category not in self.files:
            filename = f'{category}_{time.strftime("%Y%m%d_%H%M%S")}.csv' # 文件名+时间戳，防止
            filepath = os.path.join('output', filename)  # 拼接路径：
            # 创建文件夹'output'
            # 如果文件夹已经存在，不会报错(exist_ok = True)
            # 如果不存在，就自动创建。
            # 相当于“确保文件夹在写入文件前一定存在”。
            os.makedirs('output', exist_ok=True) # 因为要确保文件存在，所以创建一个文件夹叫output
            file_exist = os.path.exists(filepath) # 括号里的内容是你的文件路径，这行用来检测文件是否存在
            f = open(filepath, 'a', newline='',encoding='utf-8-sig')
            csv_writer = csv.DictWriter(f, fieldnames=self.headers)

            if not file_exist:
                csv_writer.writeheader()

            # self.files是一个字典(在init中我们命名的就是)
            # key：分类名（category，比如"青春文学"）
            # value：打开的文件对象f（open()返回的那个文件句柄）
            self.files[category] = f
            self.writers[category] = csv_writer

        dic = {
                '类别':adapter.get('category_name').strip(),
                '书名':adapter.get('book_name').strip(),
                '作者':adapter.get('author').strip(),
                '价格':adapter.get('price').strip(),
                '出版社':adapter.get('publisher').strip(),
                '商家':adapter.get('shang_jia').strip(),
                '简介':adapter.get('description').strip(),
        }
        # 去重
        unique_key = (dic['书名'],dic['作者'],dic['商家'],dic['价格'])
        if unique_key in self.seen:
            print(f'跳过重复')
            return item

        self.seen.add(unique_key)
        self.writers[category].writerow(dic)
        self.total_count += 1


        return item

    def close_spider(self, spider):
        # 关闭所有文件  字典遍历要.item
        for category,f in self.files.items():
            f.close()
            # 针对每一个分类，在关闭该分类的 CSV 文件时，打印一条日志，告诉你这个分类的数据保存到了哪个具体文件。
            spider.logger.info(f'分类{category}，已存入到{f.name}中')
        # # 在整个爬虫全部结束时，打印一条总结日志，告诉你一共爬到了多少本书。
        spider.logger.info(f'爬取结束，共获取{self.total_count}本书')

