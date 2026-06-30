import io
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, send_file, jsonify
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


@app.route("/")
def index():
    return render_template("naver_news.html")


@app.route("/crawl")
def crawl():
    all_news = []
    for page in range(1, 10):
        all_news.extend(crawl_page(page))
    return jsonify({"total": len(all_news), "news": all_news})


@app.route("/download")
def download():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "네이버증권뉴스"
    ws.append(["page", "뉴스제목", "뉴스URL"])

    for page in range(1, 10):
        for item in crawl_page(page):
            ws.append([item["page"], item["뉴스제목"], item["뉴스URL"]])

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)

    return send_file(
        buf,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="naver_finance_news.xlsx",
    )


if __name__ == "__main__":
    app.run(debug=True)
