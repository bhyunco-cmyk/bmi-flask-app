import io
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_file, jsonify, request
from openai import OpenAI
import openpyxl

app = Flask(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
}

BASE_URL = "https://finance.naver.com/news/mainnews.naver?&page={page}"

SYSTEM_PROMPT = (
    "주어진 뉴스 기사 제목을 분석하여 해당 기사의 전반적인 감정을 "
    "'긍정', '부정', 또는 '중립' 중 하나로 판단한 뒤, 결과를 아래 형식으로만 답하세요.\n\n"
    "기사 감정 판단 근거: [근거 한 줄]\n"
    "최종 감정 판단: [긍정/부정/중립]"
)


def crawl_page(page: int) -> list[dict]:
    url = BASE_URL.format(page=page)
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.encoding = "euc-kr"
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for item in soup.select(".articleSubject"):
        a_tag = item.find("a")
        if not a_tag:
            continue
        title = a_tag.get_text(strip=True)
        href = a_tag.get("href", "")
        if href.startswith("/"):
            href = "https://finance.naver.com" + href
        results.append({"page": page, "뉴스제목": title, "뉴스URL": href})
    return results


def analyze_sentiment(title: str, api_key: str) -> dict:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": title},
        ],
        max_tokens=150,
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()

    sentiment = "중립"
    reason = ""
    for line in raw.splitlines():
        if "최종 감정 판단:" in line:
            val = line.split(":", 1)[-1].strip()
            if "긍정" in val:
                sentiment = "긍정"
            elif "부정" in val:
                sentiment = "부정"
            else:
                sentiment = "중립"
        if "기사 감정 판단 근거:" in line:
            reason = line.split(":", 1)[-1].strip()

    return {"sentiment": sentiment, "reason": reason}


@app.route("/")
def index():
    return render_template("naver_news.html")


@app.route("/crawl")
def crawl():
    all_news = []
    for page in range(1, 10):
        all_news.extend(crawl_page(page))
    return jsonify({"total": len(all_news), "news": all_news})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    api_key = data.get("api_key", "").strip()
    news_list = data.get("news", [])

    if not api_key:
        return jsonify({"error": "API 키를 입력해주세요."}), 400

    results = []
    counts = {"긍정": 0, "부정": 0, "중립": 0}

    for item in news_list:
        try:
            result = analyze_sentiment(item["뉴스제목"], api_key)
        except Exception as e:
            result = {"sentiment": "중립", "reason": f"분석 오류: {str(e)}"}
        counts[result["sentiment"]] += 1
        results.append({**item, **result})

    return jsonify({"news": results, "counts": counts})


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    news_list = data.get("news", [])

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "네이버증권뉴스감성분석"
    ws.append(["page", "뉴스제목", "뉴스URL", "감성", "판단근거"])
    for item in news_list:
        ws.append([
            item.get("page", ""),
            item.get("뉴스제목", ""),
            item.get("뉴스URL", ""),
            item.get("sentiment", ""),
            item.get("reason", ""),
        ])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return send_file(
        buf,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="naver_finance_news_sentiment.xlsx",
    )


if __name__ == "__main__":
    app.run(debug=True)
