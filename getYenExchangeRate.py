import urllib.request
from bs4 import BeautifulSoup


# 余分な文字列の削除
def replace_str(s):
    s = s.replace('\r\n', '')
    s = s.replace(' ', '')
    s = s.replace(u'\xa0', '')
    return s


# 日経新聞の為替・金利のページへアクセスしてhtml取得
url = 'https://www.nikkei.com/markets/kawase/'
html = urllib.request.urlopen(url)

# 各相場のリスト
yen_exchange_rate_list = {}

soup = BeautifulSoup(html, 'html.parser')

# 円相場(ドル)部分
divs = soup.find('div', class_='mkc-prices')

# 通貨名
currency_name = 'ドル'

# 円相場
yen_exchange_rate = divs.find('div', class_='mkc-stock_prices').text

# 前日比
day_before_rate_div = divs.find('div', class_='cmn-minus')
if day_before_rate_div is None:
    day_before_rate = divs.find('div', class_='cmn-plus').text
else:
    day_before_rate = day_before_rate_div.text

# 円相場(ドル)部分の円相場と前日比を格納
yen_exchange_rate_list[currency_name] = [
    replace_str(yen_exchange_rate),
    replace_str(day_before_rate)
]

# ユーロ～豪ドルのテーブル部分
table = soup.find('table', class_='cmn-table_style1')
table_rows = table.find_all('tr')

for row in table_rows:
    # 通貨名
    currency_name = row.find('a').text

    # 円相場
    yen_exchange_rate = row.find('td', class_='mkc-number').text

    # 前日比
    # クラス名が「cmn-minus」「cmn-plus」どちらかのため、
    # 「cmn-minus」が見つからなければ「cmn-plus」の値を取得
    day_before_rate_row = row.find('span', class_='cmn-minus')
    if day_before_rate_row is None:
        day_before_rate = row.find('span', class_='cmn-plus').text
    else:
        day_before_rate = day_before_rate_row.text

    # ユーロ～豪ドルのテーブル部分の通貨名、円相場、前日比を格納
    yen_exchange_rate_list[currency_name] = [
        replace_str(yen_exchange_rate),
        replace_str(day_before_rate)
    ]

# 表示
for dic in yen_exchange_rate_list.items():
    print(dic)
