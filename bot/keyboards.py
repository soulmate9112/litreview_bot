from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_article_keyboard(doi: str, article_id: int) -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой Read More."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📖 Read More", callback_data=f"article_{article_id}"
                )
            ],
            [InlineKeyboardButton(text="🔗 Open DOI", url=doi)],
        ]
    )
