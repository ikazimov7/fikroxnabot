\
        import asyncio
        from aiogram import Bot, Dispatcher
        from aiogram.enums import ParseMode
        from config import TOKEN
        from handlers import welcome, moderation, quotes, files, warnings, admin
        from utils import cleanup

        async def main():
            bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
            dp = Dispatcher()

            # register handlers
            welcome.register_handlers(dp)
            moderation.register_handlers(dp)
            quotes.register_handlers(dp)
            files.register_handlers(dp)
            warnings.register_handlers(dp)
            admin.register_handlers(dp)

            # start cleanup background task
            asyncio.create_task(cleanup.cleanup_worker())

            print("Bot started (polling)...")
            await dp.start_polling(bot)

        if __name__ == "__main__":
            asyncio.run(main())
