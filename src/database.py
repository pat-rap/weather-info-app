# src/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from src import models  # models.py をインポート

# 接続文字列は環境変数などから取得するのが望ましいです。
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/weatherdb")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
