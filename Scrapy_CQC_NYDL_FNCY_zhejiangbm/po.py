import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}
for num in range(1,4):
    url = "http://sthjt.zj.gov.cn/module/xxgk/search.jsp?standardXxgk=0&isAllList=1&texttype=0&fbtime=-1&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={0}&sortfield=,compaltedate:0".format(num)


    data = {
        'infotypeId': 'B001AC001',
        'jdid': '1756',
        'area': '002482429',
        'divid': 'div1474328',
        'vc_title': '',
        'vc_number': '',
        'sortfield': ',compaltedate:0',
        'currpage': str(num),
        'vc_filenumber': '',
        'vc_all': '',
        'texttype': '0',
        'fbtime': '-1',
        'standardXxgk': '0',
        'isAllList': '1',
        'texttype': '0',
        'fbtime': '-1',
        'vc_all': '',
        'vc_filenumber': '',
        'vc_title': '',
        'vc_number': '',
        'currpage': str(num),
        'sortfield': ',compaltedate:0',
    }

    res_text = requests.post(url=url,data=data,headers=headers).text
    print(res_text)