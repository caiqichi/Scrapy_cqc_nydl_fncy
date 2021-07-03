
import requests
# headers = {
# #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
# #     'Cookie': '__jsluid_h=8351fe64d4d72f86b478a32b211b8444; __jsl_clearance=1565627168.852|0|BzQ0ORmiyxYiKqLC5Dyn8qE4Avo%3D'
# #     # 通过删除其余非必须字段验证者这个字段是必须的。
# # }
# #
# # url = 'http://www.mps.gov.cn/n2253534/n2253535/index.html'
# # response = requests.get(url, headers=headers)
# #
# # print(response.status_code)


# headers = {
# #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
# # }
# #
# # url = 'http://www.mps.gov.cn/n2253534/n2253535/index.html'
# # response = requests.get(url, headers=headers)
# #
# # print(response.status_code)
# # # print(response.text)
# #
# # print(response.headers['Set-Cookie'])
# #
# # first_cookie = response.headers['Set-Cookie'].split(';')[0]
# # print(first_cookie)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
}

url = 'http://www.mps.gov.cn/n2253534/n2253535/index.html'
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)