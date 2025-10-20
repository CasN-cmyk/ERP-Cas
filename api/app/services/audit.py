import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.audit import AuditLog


async def log_audit(session: AsyncSession, *, entity: str, entity_id: str, action: str, before: Any = None, after: Any = None, actor_id: int | None = None) -> None:
    entry = AuditLog(
        entity=entity,
        entity_id=str(entity_id),
        action=action,
        before=json.dumps(before, default=str) if before is not None else None,
        after=json.dumps(after, default=str) if after is not None else None,
        actor_id=actor_id,
    )
    session.add(entry)
