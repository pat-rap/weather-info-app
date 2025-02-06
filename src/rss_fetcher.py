# src/rss_fetcher.py

import httpx
import asyncio
from aiolimiter import AsyncLimiter

# 高頻度フィード向けのレートリミッター（例：1分間に1回の実行を保証）
high_freq_limiter = AsyncLimiter(max_rate=1, time_period=60)

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
    if use_limit:
        # レートリミッターを使って制限を適用
        async with high_freq_limiter:
            return await _fetch(url, timeout)
    else:
        return await _fetch(url, timeout)

async def _fetch(url: str, timeout: float = 10.0) -> str:
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # HTTPエラーがあれば例外発生
            return response.text
        except httpx.RequestError as e:
            print(f"RSSフィードの取得中にリクエストエラーが発生しました: {e}")
            raise
        except httpx.HTTPStatusError as e:
            print(f"HTTPステータスエラー: {e.response.status_code} - {e.response.text}")
            raise

# デバッグ用：直接実行して動作確認するためのコード
if __name__ == "__main__":
    test_url = "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"
    try:
        result = asyncio.run(fetch_feed(test_url))
        print("RSSフィード取得結果（先頭200文字）:")
        print(result[:200])
    except Exception as e:
        print("フィード取得に失敗しました:", e)
