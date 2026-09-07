import requests
from bs4 import BeautifulSoup
import time

# 1. 設定要爬取的股票代號列表
stock_list = ["1101", "2330", "1102"]

# 2. Telegram Bot 設定 (請替換為你的實際 Token 與 Chat ID)
BOT_TOKEN = "輸入你的 bot token"      # 範例: "6062324742:AAE..."
CHAT_ID = "輸入你的 telegram id"      # 範例: "123456789"

# 3. 標頭設定：模擬真實瀏覽器 Request，避免被 Yahoo 股市擋爬蟲
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def send_telegram_message(message):
    """發送訊息至 Telegram Bot"""
    if BOT_TOKEN == "輸入你的 bot token" or CHAT_ID == "輸入你的 telegram id":
        print("【警告】未設定 Telegram BOT_TOKEN 或 CHAT_ID，跳過發送訊息。")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print(f"成功發送至 Telegram: {message}")
        else:
            print(f"Telegram 發送失敗 (HTTP {response.status_code}): {response.text}")
    except Exception as e:
        print(f"發送 Telegram 訊息時發生網路錯誤: {e}")

# 4. 主程式：迴圈依序爬取股價
print("開始爬取股票價格...")

for stockid in stock_list:
    try:
        target_url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
        
        # 發送 HTTP 請求
        response = requests.get(target_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尋找 Yahoo 股市的股價數字標籤 (匹配多個可能變動的 CSS class)
        price_tag = soup.find('span', class_=[
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"
        ])
        
        if price_tag:
            price = price_tag.getText().strip()
            msg = f"股票 {stockid} 即時股價為：{price}"
            print(msg)
            send_telegram_message(msg)
        else:
            print(f"【提醒】股票 {stockid} 爬取失敗，無法定位股價 HTML 標籤。")

    except Exception as e:
        print(f"【錯誤】處理股票 {stockid} 時發生例外狀況: {e}")

    # 每次爬取間隔 3 秒，避免請求過於頻繁
    time.sleep(3)

print("爬取任務完成！")
