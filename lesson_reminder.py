from apscheduler.schedulers.blocking import BlockingScheduler
import telebot
import tzlocal
from settings import BOT_TOKEN, KIDS_GROUP_ID, CONVERSATION_LINK


schedule = BlockingScheduler(timezone=str(tzlocal.get_localzone()))
bot = telebot.TeleBot(BOT_TOKEN)


def first_reminder():
    bot.send_message(
        KIDS_GROUP_ID,
        "*Доброго ранку, друзі\!*\n\n"
        "За 15 хв почнеться наше заняття 👩‍💻",
        parse_mode="MarkdownV2"
    )


def second_reminder():
    bot.send_message(
        KIDS_GROUP_ID,
        "🔔🔔🔔 Саме час приєднатися до уроку, за 5 хв починаємо\n\n"
        f"[Приєднатися до заняття]({CONVERSATION_LINK})",
        disable_web_page_preview=True,
        parse_mode="MarkdownV2"
    )


def main():
    schedule.add_job(first_reminder, trigger="cron",
                     day_of_week="Sat", hour=11, minute=15)
    schedule.add_job(second_reminder, trigger="cron",
                     day_of_week="Sat", hour=11, minute=25)
    print("Have set two cron jobs...")
    schedule.start()


if __name__ == "__main__":
    main()
