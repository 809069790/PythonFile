import json
import requests
from lxml import etree

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
}

response = requests.get('http://www.qianmu.org/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D', headers=headers)

html = etree.HTML(response.text)

def University():
    # 成功数
    success = 0
    # 失败数
    errors = 0
    # 获取学校链接
    allSchool = html.xpath('//*[@id="content"]/table/tbody/tr/td[2]//a/@href')
    # 学校名 地址 本科人数 研究生人数  师生比 国际学生比例 网址
    for url in allSchool:
        try:
            a = {'学校名': "", '地址': ""}
            response_info = requests.get(url, headers=headers)
            info = etree.HTML(response_info.text)
            # 获取学校名字
            SchoolName = info.xpath('//div[@class="wikiContent"]/h1/text()')
            print()
            a['学校名'] = SchoolName
            # 详细信息
            location_list = info.xpath('//div[@class="infobox"]//tr/td[2]/p//text()')
            # 大学信息
            university_info ={}
            for i in range(1, (len(location_list)-2) ):
                str_1 = str( info.xpath('//div[@class="infobox"]//tr[%s]/td[1]/p//text()' %(str(i) ) ) )
                str_2 = str( info.xpath('//div[@class="infobox"]//tr[%s]/td[2]/p//text()' %(str(i) ) ) )
                university_info[str(str_1[2:-2])] = str(str_2[2:-2])

            for key in university_info:
                if key in ['国家','州省','城市']:
                    a['地址'] += university_info[key]
                elif key in ['网址', '本科生人数', '研究生人数', '国际学生比例', '师生比']:
                    a[key] = university_info[key]
                else:
                    pass
            if a.get("本科生人数"):
                print(a)
                with open('school_info.json', 'a', encoding='utf-8') as  f:
                    json.dump(a, f)
                    success += 1
            else:
                continue
        except:
            errors += 1
            pass
        # with open('school_info.json','rb') as f:
        #     print(json.load(f))

    print('成功数：%d，失败数：%d' % (success, errors))

if __name__ == '__main__':
    University()