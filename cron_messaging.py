from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import telebot
import tzlocal
from settings import BOT_TOKEN, KIDS_GROUP_ID, CONVERSATION_LINK


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)
schedule = BlockingScheduler(timezone=str(tzlocal.get_localzone()))
bot = telebot.TeleBot(BOT_TOKEN)


def instant_message(msg, *args, **kwargs):
    bot.send_message(KIDS_GROUP_ID, msg, *args, **kwargs)
    logging.info(f"Sent instant message '{msg}'")


def first_reminder():
    bot.send_message(
        KIDS_GROUP_ID,
        "*Доброго ранку, друзі\!*\n\n"
        "За 15 хв почнеться наше заняття 👩‍💻",
        parse_mode="MarkdownV2"
    )
    logging.info("Sent first reminder")


def second_reminder():
    bot.send_message(
        KIDS_GROUP_ID,
        "🔔🔔🔔 Саме час приєднатися до уроку, за 5 хв починаємо\n\n"
        f"[Приєднатися до заняття]({CONVERSATION_LINK})",
        disable_web_page_preview=True,
        parse_mode="MarkdownV2"
    )
    logging.info("Sent second reminder")


def main():
    # instant_message("Доброго ранку! Сподіваюся у всіх все чудово "
    #                 "і побачимося з вами завтра на нашому занятті!")
    schedule.add_job(first_reminder, trigger="cron",
                     day_of_week="Sat", hour=11, minute=15)
    schedule.add_job(second_reminder, trigger="cron",
                     day_of_week="Sat", hour=11, minute=25)
    schedule.start()


if __name__ == "__main__":
    main()
