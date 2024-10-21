import requests
from lxml import etree
import time
import os
class mengtu_spider:
    def __init__(self):
        self.headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                      'cookie':'_gid=GA1.2.248229906.1728745265; Hm_lvt_8f6576f1c707a7b6b7a3b499135768e6=1728745265,1728784284; HMACCOUNT=AB0C41409C75FEA3; Hm_lpvt_8f6576f1c707a7b6b7a3b499135768e6=1728786166; _gat_gtag_UA_120802358_2=1; _ga_EBCMBTS3TV=GS1.1.1728784285.2.1.1728786165.0.0.0; _ga=GA1.1.1622760043.1728744566',
                      'content-type':'application/x-www-form-urlencoded'
                      }
    # 获取响应数据
    def get_page(self,url):
        return requests.get(url=url,headers=self.headers)
    def post_page(self,url,data):
        return requests.post(url=url,headers=self.headers,data=data)
    # 获取总页数
    def get_max_page(self):
        page = self.get_page('https://moetu.club/category/illustration')
        r=etree.HTML(page.content.decode())
        return r.xpath('//div[@class="b2-pagenav post-nav box mg-t b2-radius "]/@data-max')

    def get_list(self,max_page):
        title_list = []
        url_list=[]
        for paged in range(1,int(max_page)+1):
            data={
                "post_type": "post-1",
                "post_order": "new",
                "post_row_count": "4",
                "post_count": "24",
                "post_thumb_width": "190",
                "post_thumb_ratio_pc": "1/0.74",
                "post_thumb_width_mobile": "100",
                "post_thumb_ratio_mobile": "1/0.6",
                "post_title_row": "1",
                "post_title_row_mobile": "2",
                "post_thumb_ratio": "4/3",
                "post_open_type": "1",
                "post_paged": paged,
                "post_load_more": "0",
                "post_cat[0]": "13",
                "show_sidebar": "0",
                "width": "1100",
                "no_rows": "false",
                "paged": paged
                }
            # 获取响应信息
            page=self.post_page('https://moetu.club/wp-json/b2/v1/getPostList',data)
            r=etree.HTML(page.json()['data'])
            # 获取标题
            title_list.extend(r.xpath('//div[@class="post-info"]/h2/a/text()'))
            # 获取url
            url_list.extend(r.xpath('//div[@class="post-info"]/h2/a/@href'))
            # time.sleep(1) # 防止源站黑ip
        return dict(zip(title_list,url_list))
    # 获取图片信息
    def get_img(self,dict_list):
        for title,url in dict_list.items():
            print(title,url)
            page=self.get_page(url)
            r=etree.HTML(page.content.decode())
            imgs_list=r.xpath('//div[@class="entry-content"]/p/img/@data-src')
            self.save_img(title,imgs_list)
            # time.sleep(1) # 防止源站黑ip

    def save_img(self, title, imgs_list):
        # 使用 os.makedirs 以确保父目录自动创建
        dir_path = './img/{}'.format(title)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f'不存在文件夹 {title}，已自动创建')

        for i, url in enumerate(imgs_list):
            response = requests.get(url)
            # time.sleep(1) # 防止源站黑ip
            if response.status_code == 200:
                file_path = '{}/{}.jpg'.format(dir_path, i + 1)
                with open(file_path, 'wb') as f:
                    print('正在保存第 {} 张图片'.format(i + 1))
                    f.write(response.content)
            else:
                print(f'无法下载图片: {url}，状态码: {response.status_code}')


    # 实现主要逻辑
    def run(self):
        max_page=self.get_max_page()[0]
        dict_list=self.get_list(max_page)
        self.get_img(dict_list)


if __name__ == '__main__':
    mengtu_spider().run()