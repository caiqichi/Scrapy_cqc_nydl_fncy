import requests

url = 'https://www.miit.gov.cn/search-front-server/api/search/info?websiteid=110000000000000&scope=basic&q=&pg=10&cateid=58&pos=title_text%2Cinfocontent%2Ctitlepy&_cus_eq_typename=&_cus_eq_publishgroupname=&_cus_eq_themename=&begin=&end=&dateField=deploytime&selectFields=title,content,deploytime,_index,url,cdate,infoextends,infocontentattribute,columnname,filenumbername,publishgroupname,publishtime,metaid,bexxgk,columnid,xxgkextend1,xxgkextend2,themename,typename,indexcode,createdate&group=distinct&highlightConfigs=%5B%7B%22field%22%3A%22infocontent%22%2C%22numberOfFragments%22%3A2%2C%22fragmentOffset%22%3A0%2C%22fragmentSize%22%3A30%2C%22noMatchSize%22%3A145%7D%5D&highlightFields=title_text%2Cinfocontent%2Cwebid&level=6&sortFields=%5B%7B%22name%22%3A%22deploytime%22%2C%22type%22%3A%22desc%22%7D%5D&p=9'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Cookie": "_ud_=ccdacf0929a542028896dee0f3aee8d2; _city=%E5%B9%BF%E5%B7%9E%E5%B8%82%E5%A4%A9%E6%B2%B3%E5%8C%BA; jsessionid=rBQdDhroYNmcWIa6Vo3rKUk3i6X1daTtVNgA; __jsluid_h=7f08cc72bf598a0cdce78d533ba01642; __jsluid_s=baa238ebe6e9c00ff3f62215138d2b17; __jsl_clearance_s=1624874070.368|0|12mX5%2BHoE%2F0oNu5YL7G%2B6%2BRvrXE%3D"

}
res = requests.get(url=url, headers=headers)
print(res.text)
print(res.status_code)

# import re
# def get_521_content():
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
#         "cookies":"_ud_=ccdacf0929a542028896dee0f3aee8d2; _city=%E5%B9%BF%E5%B7%9E%E5%B8%82%E5%A4%A9%E6%B2%B3%E5%8C%BA; jsessionid=rBQLnhroYNlG2ncxa5W_jEcEldOs_k2NgYYA; __jsluid_h=7f08cc72bf598a0cdce78d533ba01642; __jsluid_s=baa238ebe6e9c00ff3f62215138d2b17; __jsl_clearance_s=1624852047.396|0|iRjvG9mVstnPkDinnlPXXJ%2FrnM4%3D"
#     }
#     req = requests.get(url, headers=headers)
#     cookies = req.cookies
#
#     cookies = '; '.join(['='.join(item) for item in cookies.items()])
#     txt_521 = req.text
#     txt_521 = ''.join(re.findall('<script>document\.cookie=(.*?)\;location\.href=location\.pathname\+location\.search</script>', txt_521))
#     return (txt_521, cookies)
#
#
# text = get_521_content()[0]
# cookies = get_521_content()[1]
# print(cookies)
#
# import execjs
# js_cookie = text
# # print(execjs.eval(js_cookie))  # execjs.eval执行js代码。即使加密也能显示
# real_js_cookie = str(execjs.eval(js_cookie)).split(';')[0]
# print(real_js_cookie)
#
# # session = requests.session()
# # headers1 = {
# #     "cookies":real_js_cookie
# # }
# # print(session.get(url,headers=headers1).text)
#
# #
# #
# # headers1 = {
# #              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
# #              'Cookie':cookies+';'+real_js_cookie,
# # }
# #
# # code = requests.get(url,headers=headers1).text
# # print(code)
# #
