# init_db.py
import asyncio
from src.database import init_db

async def create_tables():
    print("データベースのテーブル作成を開始します...")
    await init_db()
    print("テーブル作成完了！")

if __name__ == "__main__":
    asyncio.run(create_tables())
