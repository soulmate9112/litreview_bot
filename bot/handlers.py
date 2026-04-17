from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from config import CHAT_ID
from crud.saved_article_repository import get_saved_article_repository
from crud.sent_article_repository import get_sent_article_repository
from bot.keyboards import get_article_keyboard

router = Router()


def format_articles_message(articles) -> str:
    """Форматирует список статей в одно сообщение."""
    if not articles:
        return "📭 Нет новых статей для отправки."

    message = "📚 **Новые статьи:**\n\n"
    for i, article in enumerate(articles, 1):
        message += f"**{i}. {article.title}**\n"
        message += f"👥 *Авторы:* {article.authors}\n"
        message += f"📅 *Год:* {article.publication_year}\n"
        message += f"🔗 DOI: `{article.doi}`\n\n"

    return message


@router.message(F.text == "/start")
async def start_command(message: Message):
    """Обработчик команды /start."""
    await message.answer(
        "👋 Привет! Я бот для рассылки научных статей.\n\n"
        "📅 Новые статьи публикуются каждые 3 дня.\n"
        "🔔 Я автоматически отправляю их в этот чат."
    )


@router.message(F.text == "/send_articles")
async def send_articles_command(message: Message):
    """Ручная команда для отправки статей (для тестирования)."""
    await send_pending_articles(message)


async def send_pending_articles(message: Message = None):
    """Отправляет все непрочитанные статьи."""
    saved_repo = get_saved_article_repository()
    sent_repo = get_sent_article_repository()
    unsent_articles = saved_repo.get_unsent_articles()

    if not unsent_articles:
        if message:
            await message.answer("Новые статьи отсутствуют.")
        return

    message_text = format_articles_message(unsent_articles)

    # Отправляем сообщение
    target_chat = message.chat.id if message else int(CHAT_ID)

    # Отправляем одно сообщение со всеми статьями
    await message.bot.send_message(
        chat_id=target_chat, text=message_text, parse_mode=ParseMode.MARKDOWN
    )

    # Отмечаем статьи как отправленные
    sent_repo.put_unsent_articles(unsent_articles)

    print(f"✅ Отправлено {len(unsent_articles)} статей")


@router.callback_query(F.data.startswith("article_"))
async def article_details(callback: CallbackQuery):
    """Показывает детали статьи при нажатии Read More."""
    article_id = int(callback.data.split("_")[1])

    saved_repo = get_saved_articles_repository()
    article = saved_repo.get_article_by_id(article_id)

    if article:
        details = (
            f"📄 **{article.title}**\n\n"
            f"👥 **Авторы:** {article.authors}\n"
            f"📅 **Год:** {article.publication_year}\n"
            f"🔗 **DOI:** `{article.doi}`\n\n"
            f"📝 **Аннотация:**\n{article.abstract[:500]}..."
        )

        await callback.message.answer(
            details, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

    await callback.answer()
