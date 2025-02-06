# src/db_saver.py

from src.database import async_session
from src import models
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
import asyncio

async def save_feed_data(feed_url: str, feed_info: dict, entries: list, category: str, frequency_type: str):
    """
    feed_info, entries を元に、DBにフィード情報と各エントリを保存します。
    既に存在するエントリは重複登録を避ける処理を含みます。
    """
    async with async_session() as session:
        # まず、feed_meta の存在確認。feed_id_in_atom が一意であれば、それを利用。
        stmt = select(models.FeedMeta).where(models.FeedMeta.feed_url == feed_url)
        result = await session.execute(stmt)
        feed_meta = result.scalar_one_or_none()

        if not feed_meta:
            # 新規の場合、feed_meta を作成
            feed_meta = models.FeedMeta(
                feed_url=feed_url,
                feed_title=feed_info.get("feed_title"),
                feed_subtitle=feed_info.get("feed_subtitle"),
                feed_updated=feed_info.get("feed_updated"),
                category=category,
                frequency_type=frequency_type,
                last_fetched=feed_info.get("feed_updated"),  # 例として
            )
            session.add(feed_meta)
            await session.flush()  # feed_meta.id を確定させるため

        # 各エントリの保存。重複チェックは entry_id_in_atom をキーに行う。
        for entry in entries:
            stmt = select(models.FeedEntry).where(models.FeedEntry.entry_id_in_atom == entry["entry_id_in_atom"])
            result = await session.execute(stmt)
            existing_entry = result.scalar_one_or_none()
            if not existing_entry:
                new_entry = models.FeedEntry(
                    feed_id=feed_meta.id,
                    entry_id_in_atom=entry["entry_id_in_atom"],
                    entry_title=entry.get("entry_title"),
                    entry_updated=entry.get("entry_updated"),
                    entry_author=entry.get("entry_author"),
                    entry_link=entry.get("entry_link"),
                    entry_content=entry.get("entry_content"),
                    inserted_at=entry.get("inserted_at"),
                )
                session.add(new_entry)
        await session.commit()
