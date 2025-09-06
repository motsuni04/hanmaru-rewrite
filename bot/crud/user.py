from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


async def register_user(session: AsyncSession, discord_user):
    user = User(
        id=discord_user.id,
        username=discord_user.global_name or discord_user.name,
        avatar_url=discord_user.display_avatar.url
    )
    await session.merge(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, discord_id: int):
    result = await session.execute(
        select(User)
        .where(User.id == discord_id)
    )
    return result.scalar_one_or_none()


async def get_a_user_by_username_ordered_by_level(session: AsyncSession, username: str):
    result = await session.execute(
        select(User)
        .filter(User.username == username)
        .order_by(User.level.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def add_token(session: AsyncSession, discord_id: int, amount: int) -> bool:
    user = (await session.execute(
        select(User)
        .where(User.id == discord_id)
        .with_for_update()
    )).scalar_one_or_none()
    if not user:
        raise ValueError("User not found")
    if user.token + amount < 0:
        return False
    await session.execute(
        update(User)
        .where(User.id == discord_id)
        .values(token=User.token + amount)
    )
    await session.commit()
    return True
