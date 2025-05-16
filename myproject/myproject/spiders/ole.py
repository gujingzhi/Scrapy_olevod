import time
import scrapy
import json
from urllib.parse import quote
from myproject.items import MyprojectItem
import hashlib

class oleSpider(scrapy.Spider):
    name = "ole"
    allowed_domains = ["olevod.com/update"]
    # encoded_path = quote("电影/全部地区/全部年份/全部类型/全部/全部/最新.html", safe="/")
    #只爬取动作电影的前100页

    #valid_key
    timestamp = str(int(time.time())*1000)
    secret_key = "www.olevod.com" # 需要继续破解secret_key
    raw_string = timestamp + secret_key
    sign = hashlib.md5(raw_string.encode()).hexdigest()


    for i in range(1,74):
        start_urls = ["https://api.olelive.com/v1/pub/vod/list/true/3/0/0/1/0/0/update/"+str(i)+"/48?_vv=dba0183b4a71c13a3fc164cb10537576"for i in range(1, 74)]#sign]
    print("start_url is :",start_urls)

    # def start(self):
    #     for i in range(1, 74):
    #         url = "https://api.olelive.com/v1/pub/vod/list/true/3/0/0/1/0/0/update/"+ str(i) + "/48?_vv=" + "dba0183b4a71c13a3fc164cb10537576"#sign
    #         print("url: ",url)
    #         yield scrapy.Request(
    #             url=url,
    #             callback=self.parse,
    #             meta={"page_num": i}
    #         )

    def parse(self, response):
        
        # print(f"正在处理第 {self.i} 页: ")

        json_data = response.json()
        print("json_data, ",json_data)
        data_list = json_data.get("data", {}).get("list", [])
        print("data_list, ",data_list)
        for item in data_list:
            itemPip = MyprojectItem()
            yield {
                "id": item.get("id"),
                "name": item.get("name"),
                "actor": item.get("actor"),
                "score": item.get("score"),
                "area": item.get("area"),
                "year": item.get("year"),
                "blurb": item.get("blurb"),
                "cover": "https://www.olevod.com/" + item.get("pic")  # 补全封面图路径
            }
            itemPip['id']= item.get("id")
            itemPip['name'] = item.get("name")
            itemPip['picture'] = "https://www.olevod.com/" + item.get("pic")
            itemPip['score'] = item.get("score")
            itemPip['year'] = item.get("year")
            itemPip['country'] = item.get("area")
            itemPip['intro'] = item.get("blurb")
            yield itemPip
        
        
        
