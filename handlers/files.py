\
        from aiogram import types
        from utils.moderation import give_warning
        from utils.json_manager import increment_stat
        from config import LOG_CHANNEL_ID
        import asyncio

        BLOCKED = (".exe", ".apk")

        def is_blocked(filename: str) -> bool:
            if not filename:
                return False
            fname = filename.lower()
            for ext in BLOCKED:
                if fname.endswith(ext) or ext + "." in fname:
                    return True
            return False

        async def on_document(message: types.Message):
            if message.from_user and message.from_user.is_bot:
                return
            if message.from_user and message.from_user.id in []:
                return
            doc = message.document
            if not doc:
                return
            if is_blocked(doc.file_name or ""):
                try:
                    await message.delete()
                except Exception:
                    pass
                await give_warning(message, reason="Taqiqlangan fayl yuborildi")
                await increment_stat("files_blocked")
                try:
                    m = await message.reply("⛔️ .exe va .apk fayllar yuborish taqiqlangan.")
                    await asyncio.sleep(10)
                    await m.delete()
                except Exception:
                    pass
                if LOG_CHANNEL_ID:
                    try:
                        await message.bot.send_message(LOG_CHANNEL_ID, f"⛔️ Blocked file: {doc.file_name} from {message.from_user.full_name} ({message.from_user.id})")
                    except Exception:
                        pass

        def register_handlers(dp):
            dp.message.register(on_document, content_types=["document"])
