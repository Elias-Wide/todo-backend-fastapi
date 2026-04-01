from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from db.database import Model


class PromptsOrm(Model):
    __tablename__ = 'system_prompts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        UniqueConstraint('name', 'is_active', name='_one_active_prompt_uc'),
    )
