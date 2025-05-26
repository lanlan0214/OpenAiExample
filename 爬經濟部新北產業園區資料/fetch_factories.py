# 先安裝必要套件：
# pip install requests beautifulsoup4 pandas openpyxl

import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# 全局 Session，重用連線提高效能
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

def fetch_factories(page: int) -> list[dict]:
    """
    抓取第 page 頁的廠商資料，回傳 list of dict
    """
    url = 'https://www.bip.gov.tw/iphw/wuku/factory.do'
    params = {'method': 'list', 'page': page}

    resp = session.get(url, params=params, timeout=10)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    ul = soup.find('ul', class_='list-group')
    if not ul:
        print(f"❗️ 第 {page} 頁找不到 list-group！")
        return []

    items = ul.find_all('li', class_='list-group-item')
    data = []
    for li in items:
        spans = li.select('div.row.mb-1 > span')
        if len(spans) >= 4:
            reg_no  = spans[0].get_text(strip=True)
            name_el = spans[1].find('strong')
            name    = name_el.get_text(strip=True) if name_el else spans[1].get_text(strip=True)
            address = spans[2].get_text(strip=True)
            phone   = spans[3].get_text(strip=True)
            data.append({
                'reg_no':  reg_no,
                'name':    name,
                'address': address,
                'phone':   phone
            })
    print(f"✅ 第 {page} 頁抓到 {len(data)} 筆")
    return data

def get_total_pages() -> int:
    """
    先抓第一頁，解析總筆數並計算總頁數
    """
    url = 'https://www.bip.gov.tw/iphw/wuku/factory.do'
    resp = session.get(url, params={'method':'list','page':1}, timeout=10)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')

    td = soup.find('td', align='right')
    m = re.search(r'共\s*([\d,]+)\s*項資料', td.get_text()) if td else None
    total_items = int(m.group(1).replace(',', '')) if m else 0

    # 抓第一頁實際有幾筆，再算總頁數
    first_page_count = len(fetch_factories(1))
    return math.ceil(total_items / first_page_count) if first_page_count else 1

if __name__ == '__main__':
    print("🏁 開始並行抓取所有頁面的廠商資料…")
    total_pages = get_total_pages()
    print(f"🗂️ 共 {total_pages} 頁")

    all_factories = []
    # 使用最多 10 個執行緒同時請求
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_factories, p): p for p in range(1, total_pages+1)}
        for fut in as_completed(futures):
            page = futures[fut]
            try:
                data = fut.result()
                all_factories.extend(data)
            except Exception as e:
                print(f"❗️ 第 {page} 頁執行錯誤：{e}")

    if all_factories:
        df = pd.DataFrame(all_factories)
        # 以當天日期作為檔名，格式為 YYYYMMDD.xlsx
        date_str = datetime.now().strftime('%Y%m%d')
        output_file = f'{date_str}.xlsx'
        df.to_excel(output_file, index=False)
        print(f"🎉 完成！共抓到 {len(all_factories)} 筆，已匯出到 {output_file}")
    else:
        print("🚫 沒有抓到任何資料，請檢查程式或網路狀態。")
