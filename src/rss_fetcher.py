# src/rss_fetcher.py

import httpx
import asyncio
from aiolimiter import AsyncLimiter

# 高頻度フィード向けのレートリミッター（例：1分間に1回の実行を保証）
high_freq_limiter = AsyncLimiter(max_rate=1, time_period=60)

# 各フィードURL毎にキャッシュ情報を保持する辞書
# 例: { feed_url: {"last_modified": "Wed, 21 Oct 2015 07:28:00 GMT",
#                   "etag": "abc123", "content": "<xml>...</xml>" } }
cache_info = {}

# ダウンロード済み総バイト数のカウンター（単位：バイト）
total_downloaded_bytes = 0
DOWNLOAD_LIMIT_BYTES = 10 * 1024 * 1024 * 1024  # 10GB

async def fetch_feed(url: str, timeout: float = 10.0, use_limit: bool = True) -> str:
    """
    指定されたURLからRSSフィードを非同期に取得し、XMLデータを文字列として返却します。
    use_limit が True の場合、レートリミッターで制限します。

    Args:
        url (str): RSSフィードの取得先URL
        timeout (float): リクエストタイムアウト（秒）

    Returns:
        str: 取得したRSSフィードのXMLデータ

    Raises:
        httpx.RequestError: リクエストに関するエラー発生時
        httpx.HTTPStatusError: HTTPステータスエラー発生時
    """
    global total_downloaded_bytes

    # ダウンロード量が上限に達している場合、処理を中断
    if total_downloaded_bytes >= DOWNLOAD_LIMIT_BYTES:
        raise Exception("Download limit reached. Skipping feed fetch.")

    # キャッシュ情報を基に、HTTPリクエスト用ヘッダーを組み立てる
    headers = {}
    if url in cache_info:
        if "last_modified" in cache_info[url]:
            headers["If-Modified-Since"] = cache_info[url]["last_modified"]
        if "etag" in cache_info[url]:
            headers["If-None-Match"] = cache_info[url]["etag"]

    if use_limit:
        # レートリミッターを使って制限を適用
        async with high_freq_limiter:
            response = await _fetch(url, timeout)
    else:
        response = await _fetch(url, timeout)

    # 304 Not Modified の場合、キャッシュ済みのコンテンツを利用
    if response.status_code == 304:
        print(f"[Fetch] {url} not modified. Using cached content.")
        if url in cache_info and "content" in cache_info[url]:
            return cache_info[url]["content"]
        else:
            return ""

    # 成功レスポンスの場合
    content_bytes = response.content
    content_length = len(content_bytes)
    total_downloaded_bytes += content_length  # ダウンロード量を加算

    # レスポンスヘッダーからキャッシュ情報を更新
    last_modified = response.headers.get("Last-Modified")
    etag = response.headers.get("ETag")
    text_content = response.text

    cache_info[url] = {
        "last_modified": last_modified,
        "etag": etag,
        "content": text_content,
    }

    return text_content

async def _fetch(url: str, timeout: float, headers: dict) -> httpx.Response:
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response

# デバッグ用：直接実行して動作確認するためのコード
if __name__ == "__main__":
    test_url = "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"
    try:
        result = asyncio.run(fetch_feed(test_url))
        print("RSSフィード取得結果（先頭200文字）:")
        print(result[:200])
    except Exception as e:
        print("フィード取得に失敗しました:", e)
