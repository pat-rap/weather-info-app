# integration_test.py

import asyncio
from src import rss_fetcher, rss_parser, db_saver

async def integration_test():
    # テスト対象のRSSフィードURL
    feed_url = "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"
    # サンプルとして、カテゴリと更新頻度を指定（実際の仕様に合わせて調整してください）
    category = "天気概況"
    frequency_type = "高頻度"  # 例：高頻度（毎分更新）のフィード

    try:
        print("1. RSSフィードの取得を開始します...")
        xml_data = await rss_fetcher.fetch_feed(feed_url)
        print("　→ RSSフィードの取得完了。")

        print("2. 取得したXMLデータの解析を開始します...")
        feed_info, entries = rss_parser.parse_rss(xml_data)
        print("　→ 解析完了。")
        
        print("3. 解析結果をDBに保存します...")
        await db_saver.save_feed_data(feed_url, feed_info, entries, category, frequency_type)
        print("　→ DBへの保存が完了しました。")
        
        print("統合テストが正常に完了しました。")
    except Exception as e:
        print("統合テスト中にエラーが発生しました:", e)

if __name__ == "__main__":
    asyncio.run(integration_test())
