import asyncio
import json
from pathlib import Path

from sqlalchemy import select

from ..core.db import async_session, Base, engine
from ..core.security import get_password_hash
from ..models import settings as settings_model
from ..models import user as user_model


async def seed():
    seed_path = Path(__file__).with_suffix('.json')
    payload = json.loads(seed_path.read_text())

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        for user in payload.get("users", []):
            existing = await session.execute(select(user_model.User).where(user_model.User.email == user["email"]))
            if existing.scalar_one_or_none():
                continue
            session.add(
                user_model.User(
                    name=user["name"],
                    email=user["email"],
                    role=user["role"],
                    password_hash=get_password_hash(user["password"]),
                )
            )

        for key, value in payload.get("settings", {}).items():
            existing = await session.execute(select(settings_model.Setting).where(settings_model.Setting.key == key))
            setting = existing.scalar_one_or_none()
            if setting:
                setting.value = json.dumps(value)
            else:
                session.add(settings_model.Setting(key=key, value=json.dumps(value)))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
