import requests
from bs4 import BeautifulSoup
import time

# 要爬取的股票代號列表
stock = ["1101", "2330", "1102"]

# Telegram Bot 設定 (請替換為你的實際 Token 與 Chat ID)
token = "你的_BOT_TOKEN"      # 範例: "6062324742:AAE..."
chat_id = "你的_TELEGRAM_ID"  # 範例: "123456789"

# 加入 User-Agent 標頭，避免被 Yahoo 擋爬蟲
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 迴圈依序爬取股價
for stockid in stock:
    try:
        url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
        
        # 發送 HTTP 請求
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 定位股價標籤
        price_tag = soup.find('span', class_=[
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"
        ])
        
        if price_tag:
            price = price_tag.getText().strip()
            message = f"股票 {stockid} 即時股價為 {price}"
            
            # 使用 POST 發送 Telegram 訊息
            telegram_url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message
            }
            requests.post(telegram_url, data=payload)
            print(f"成功發送: {message}")
        else:
            print(f"無法取得股票 {stockid} 的股價標籤")

    except Exception as e:
        print(f"處理股票 {stockid} 時發生錯誤: {e}")

    # 每次請求間隔 3 秒
    time.sleep(3)
