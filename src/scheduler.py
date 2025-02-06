# src/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from src import rss_fetcher, rss_parser, db_saver, config

async def fetch_and_save_feed(feed_url: str, category: str, frequency_type: str):
    """
    指定されたRSSフィードを取得し、解析してDBに保存する非同期タスク
    """
    try:
        xml_data = await rss_fetcher.fetch_feed(feed_url)
        feed_info, entries = rss_parser.parse_rss(xml_data)
        await db_saver.save_feed_data(feed_url, feed_info, entries, category, frequency_type)
        print(f"[Scheduler] Feed update successful for {feed_url}")
    except Exception as e:
        print(f"[Scheduler] Error updating feed {feed_url}: {e}")

def start_scheduler():
    """
    スケジューラーを起動し、各RSSフィードに対して定期ジョブを登録する
    """
    scheduler = AsyncIOScheduler()

    # 高頻度フィード（毎分更新）のジョブ登録
    for category, feed_url in config.HIGH_FREQ_FEEDS.items():
        scheduler.add_job(fetch_and_save_feed, 'interval', minutes=1,
                          args=[feed_url, category, "高頻度"],
                          id=f"high_{category}")

    # 長期フィード（毎時更新）のジョブ登録
    for category, feed_url in config.LONG_TERM_FEEDS.items():
        scheduler.add_job(fetch_and_save_feed, 'interval', hours=1,
                          args=[feed_url, category, "長期"],
                          id=f"long_{category}")

    scheduler.start()
    print("Scheduler started")
