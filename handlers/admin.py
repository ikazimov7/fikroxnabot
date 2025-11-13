\
        from aiogram import types
        from utils.txt_manager import append_line, remove_line, read_lines
        from config import BADWORDS_FILE, LOG_CHANNEL_ID
        import asyncio

        async def cmd_abw(message: types.Message):
            from config import ADMIN_IDS
            if message.from_user.id not in ADMIN_IDS:
                return
            arg = message.get_args().strip()
            if not arg:
                await message.reply("Usage: /abw <so'z>")
                return
            lines = read_lines(BADWORDS_FILE)
            if arg.lower() in [l.lower() for l in lines]:
                await message.reply("So'z allaqachon mavjud.")
                return
            append_line(BADWORDS_FILE, arg.strip())
            await message.reply(f"✅ '{arg}' qo'shildi.")
            if LOG_CHANNEL_ID:
                await message.bot.send_message(LOG_CHANNEL_ID, f"✅ Badword added: {arg} by {message.from_user.full_name}")

        async def cmd_dbw(message: types.Message):
            from config import ADMIN_IDS
            if message.from_user.id not in ADMIN_IDS:
                return
            arg = message.get_args().strip()
            if not arg:
                await message.reply("Usage: /dbw <so'z>")
                return
            remove_line(BADWORDS_FILE, arg.strip())
            await message.reply(f"✅ '{arg}' o'chirildi (agar mavjud bo'lsa).")
            if LOG_CHANNEL_ID:
                await message.bot.send_message(LOG_CHANNEL_ID, f"❌ Badword removed: {arg} by {message.from_user.full_name}")

        async def cmd_bwl(message: types.Message):
            from config import ADMIN_IDS
            if message.from_user.id not in ADMIN_IDS:
                return
            lines = read_lines(BADWORDS_FILE)
            text = "📜 Bad Words List:\\n" + ("\\n".join(f"{i+1}. {w}" for i,w in enumerate(lines)) if lines else "— (bo'sh)")
            if LOG_CHANNEL_ID:
                await message.bot.send_message(LOG_CHANNEL_ID, text)
            await message.reply("✅ Ro'yxat log kanalga yuborildi.")
            await asyncio.sleep(5)
            try:
                await message.delete()
            except Exception:
                pass

        def register_handlers(dp):
            dp.message.register(cmd_abw, commands=["abw"])
            dp.message.register(cmd_dbw, commands=["dbw"])
            dp.message.register(cmd_bwl, commands=["bwl"])
