from backend.config import APP_DIR
from backend.core.constants.ai_services import GROQ_TEXT_PROMPT_KEY
from backend.db.database import get_session
from backend.repositories.prompts import PromptsRepository

PROMPT_PATH = APP_DIR / 'static' / 'prompts' / 'system_prompt.md'


def get_system_prompt():
    with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
        return f.read()


prompt_text = get_system_prompt()


async def create_system_prompt():
    """Initialize system prompt if it does not exist."""
    async for session in get_session():
        repo = PromptsRepository(session)
        existing = await repo.get_one_by_field(
            attr_name='name', attr_value=GROQ_TEXT_PROMPT_KEY
        )

        if not existing:
            try:
                content = get_system_prompt()
                await repo.create_prompt(
                    name=GROQ_TEXT_PROMPT_KEY, text=content
                )
                await repo.session.close()
                return
            except FileNotFoundError:
                return
