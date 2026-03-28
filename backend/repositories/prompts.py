from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.prompts import PromptsOrm
from backend.repositories.base import SQLAlchemyRepository


class PromptsRepository(SQLAlchemyRepository):
    model: PromptsOrm = PromptsOrm

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_prompt(self, name: str, text: str) -> int:
        """Create a new prompt and return its ID."""
        obj = PromptsOrm(name=name, content=text, is_active=True)
        self.session.add(obj)
        await self.session.flush()
        await self.deactivate_others(obj.id, name)
        await self.session.commit()
        return obj.id

    async def deactivate_others(self, p_id: int, name: str):
        """Deactivate all prompts with same name except current ID."""
        stmt = (
            update(PromptsOrm)
            .filter(PromptsOrm.name == name, PromptsOrm.id != p_id)
            .values(is_active=False)
        )
        await self.session.execute(stmt)
