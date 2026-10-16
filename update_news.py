import os
import json
import urllib.request
from datetime import datetime, timezone, timedelta

API_KEY = os.environ.get("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

topics = {
    'economy': '정부 경제 정책 및 금리',
    'realestate-trend': '전국 부동산 및 아파트 가격 변동',
    'realestate-policy': '최신 부동산 규제 및 정책'
}

kst = datetime.now(timezone.utc) + timedelta(hours=9)
news_data = {
    "last_updated": kst.strftime("%Y년 %m월 %d일 %H시 %M분"),
    "economy": [],
    "realestate-trend": [],
    "realestate-policy": []
}

for key, topic in topics.items():
    prompt = f"최근 하루 동안의 '{topic}' 관련 대한민국 주요 뉴스 3가지를 요약해줘. 반드시 아래 JSON 배열 형식으로만 대답해.\n[\n  {{\"title\": \"뉴스 제목\", \"summary\": \"1~2줄 요약\", \"details\": \"상세 배경 및 수치\", \"source\": \"언론사 이름\", \"url\": \"실제 기사 링크\"}}\n]"

    data = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(URL, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = text.replace('```json', '').replace('```', '').strip()
            news_data[key] = json.loads(text)
    except Exception as e:
        print(f"Error fetching {key}: {e}")

with open("news_data.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)
