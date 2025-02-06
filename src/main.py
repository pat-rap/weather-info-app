# src/main.py

from fastapi import FastAPI, HTTPException, Query
import asyncio
from src import rss_fetcher

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/fetch_feed")
async def fetch_feed_endpoint(
    url: str = Query(..., description="RSSフィードのURLを指定してください")
):
    """
    指定されたURLからRSSフィードを取得し、結果を返します。
    """
    try:
        xml_data = await rss_fetcher.fetch_feed(url)
        # 取得したXMLデータの先頭部分をレスポンスに含める例
        snippet = xml_data[:500]  # 先頭500文字を返す（必要に応じて調整）
        return {"feed_snippet": snippet, "full_length": len(xml_data)}
    except Exception as e:
        # エラー発生時はHTTPステータスコード500でエラーメッセージを返す
        raise HTTPException(status_code=500, detail=f"フィード取得エラー: {str(e)}")
