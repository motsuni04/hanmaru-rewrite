from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


async def register_user(session: AsyncSession, discord_id: int, username: str):
    user = User(id=discord_id, username=username)
    await session.merge(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, discord_id: int):
    result = await session.execute(
        select(User)
        .where(User.id == discord_id)
    )
    return result.scalar_one_or_none()


async def add_token(session: AsyncSession, discord_id: int, amount: int):
    await session.execute(
        update(User)
        .where(User.id == discord_id)
        .values(token=User.token + amount)
    )
    await session.commit()
