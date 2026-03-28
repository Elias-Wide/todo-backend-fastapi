from sqladmin import ModelView

from backend.models.prompts import PromptsOrm


class PromptsAdmin(ModelView, model=PromptsOrm):
    column_list = [
        PromptsOrm.id,
        PromptsOrm.name,
        PromptsOrm.is_active,
        PromptsOrm.updated_at,
    ]
    column_searchable_list = [PromptsOrm.name]
    column_sortable_list = [PromptsOrm.updated_at]
    form_columns = [PromptsOrm.name, PromptsOrm.content, PromptsOrm.is_active]
    column_searchable_list = [PromptsOrm.name]
    column_formatters = {
        PromptsOrm.content: lambda m, a: (
            m.content[:50] + '...' if len(m.content) > 50 else m.content
        )
    }


admin_views: tuple[ModelView] = (PromptsAdmin,)
