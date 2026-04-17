import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta
from bot.handlers import send_pending_articles

scheduler = AsyncIOScheduler()


def schedule_article_dispatch(bot: Bot):
    """Настраивает периодическую отправку статей (каждые 3 дня)."""

    # Запускаем каждые 3 дня
    scheduler.add_job(
        send_pending_articles,
        trigger=IntervalTrigger(days=3),
        kwargs={"message": None},  # None означает использовать CHAT_ID из конфига
        id="dispatch_articles",
        name="Отправка новых статей",
        replace_existing=True,
    )

    scheduler.start()
