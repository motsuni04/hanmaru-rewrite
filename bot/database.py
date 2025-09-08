from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # noqa


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
