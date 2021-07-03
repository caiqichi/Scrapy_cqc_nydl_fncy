
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
}

# 521状态码:中华人民共和国公安部，无法使用之间的方法破解
url = 'http://www.mps.gov.cn/n2253534/n2253535/index.html'
response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)