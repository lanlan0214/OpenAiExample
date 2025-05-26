from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def fetch_factories(page=1):
    """
    用 Selenium 抓取第 page 頁的廠商資料
    """
    print(f"➡️ 開始 fetch_factories，第 {page} 頁")
    # 1. 啟動 headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        url = f"https://www.bip.gov.tw/iphw/wuku/factory.do?method=list&page={page}"
        driver.get(url)

        # 2. 等待 table 出現
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table_basic'))
        )

        # 3. 取得完整 HTML
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_='table_basic')

        rows = table.find_all('tr')[1:]
        print(f"   • 找到 {len(rows)} 筆 <tr>（不含表頭）")

        data = []
        for tr in rows:
            cols = [td.get_text(strip=True) for td in tr.find_all('td')]
            if len(cols) >= 5:
                data.append({
                    'reg_no':  cols[0],
                    'name':    cols[1],
                    'owner':   cols[2],
                    'phone':   cols[3],
                    'address': cols[4]
                })
        return data

    except Exception as e:
        print(f"❗️ 發生錯誤：{e}")
        return []

    finally:
        driver.quit()

if __name__ == '__main__':
    print("🏁 fetch_factories_selenium.py 執行中…")
    all_factories = []
    for p in range(1, 6):
        farms = fetch_factories(page=p)
        if not farms:
            break
        all_factories.extend(farms)

    if not all_factories:
        print("🚫 尚未抓到任何資料，請檢查上方錯誤訊息。")
    else:
        print(f"✅ 總共抓到 {len(all_factories)} 筆資料：")
        for f in all_factories:
            print(f)
