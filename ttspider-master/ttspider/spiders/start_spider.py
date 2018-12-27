# -*- coding: utf-8 -*-
import os

import scrapy
import xlrd
from scrapy.spiders import Request


class StartSpider(scrapy.Spider):
    name = 'start_spider'
    allowed_domains = ['www.csindex.com.cn']

    # 上证50 1-50 超大： http://www.csindex.com.cn/zh-CN/indices/index-detail/000016
    # 沪深300 1-300 大：http://www.csindex.com.cn/zh-CN/indices/index-detail/000300
    # 中证500 301-800 中：http://www.csindex.com.cn/zh-CN/indices/index-detail/000905
    # 中证1000 801-1800 小：http://www.csindex.com.cn/zh-CN/indices/index-detail/000852
    start_urls = [
        'http://www.csindex.com.cn/zh-CN/indices/index-detail/000016',
        'http://www.csindex.com.cn/zh-CN/indices/index-detail/000300',
        'http://www.csindex.com.cn/zh-CN/indices/index-detail/000905',
        'http://www.csindex.com.cn/zh-CN/indices/index-detail/000852',
    ]

    def parse(self, response):
        # //ul[contains(@class,'download')]//a[text()='成份列表']/@href
        # extract_first 可以在取不到数据时不报错
        chengfen_url = response.xpath("//ul[contains(@class,'download')]//a[text()='成份列表']/@href").extract_first()
        # print(chengfen_url)
        self.log('成份URL: ' + chengfen_url)
        # pass
        yield Request(url=chengfen_url, callback=self.download_parse)

    def download_parse(self, response):
        self.log(response.url)
        self.log(response.body)
        # http://www.csindex.com.cn/uploads/file/autofile/cons/000905cons.xls
        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        wb = xlrd.open_workbook(filename)
        table = wb.sheets()[0]  # 通过索引顺序获取
        # table = data.sheet_by_index(0)  # 通过索引顺序获取
        # table = data.sheet_by_name(u'Sheet1')  # 通过名称获取

        # 获取整行和整列的值（数组）
        # print(table.row_values(0))
        # print(table.col_values(0))

        # 获取行数和列数
        # nrows = table.nrows
        # ncols = table.ncols
        # print(nrows)
        # print(ncols)

        # 循环行列表数据
        # for i in range(nrows):
        #     print(table.row_values(i))

        # 单元格： 第几行，第几列
        # cell_A1 = table.cell(0, 0).value
        # cell_C4 = table.cell(3, 2).value
        # print(cell_A1)
        # print(cell_C4)

        # 使用行列索引
        # cell_A1 = table.row(0)[0].value
        # cell_B2 = table.col(1)[0].value
        # print(cell_A1)
        # print(cell_B2)

        os.remove(filename)

        pass
