\
        from aiogram import types
        from config import BADWORDS_FILE, LOG_CHANNEL_ID
        from utils.txt_manager import read_lines
        from utils.moderation import give_warning
        from utils.json_manager import increment_stat
        import re, asyncio

        LINK_RE = re.compile(r"(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+|joinchat/\S+)", re.IGNORECASE)
        MENTION_RE = re.compile(r"@\w+", re.IGNORECASE)

        def contains_link(text: str) -> bool:
            if not text:
                return False
            return bool(LINK_RE.search(text))

        def contains_badword(text: str, badwords: list[str]) -> tuple[bool,str]:
            if not text:
                return False, ""
            t = text.lower()
            for w in badwords:
                pattern = rf"(?<!\w){re.escape(w)}(?!\w)"
                if re.search(pattern, t):
                    return True, w
            return False, ""

        async def handle_text(message: types.Message):
            text = message.text or ""
            user = message.from_user
            if user.is_bot:
                return
            from config import ADMIN_IDS
            if user.id in ADMIN_IDS:
                return
            if text.strip().startswith("/"):
                try:
                    await message.delete()
                except Exception:
                    pass
                return
            if contains_link(text):
                if MENTION_RE.fullmatch(text.strip()):
                    return
                try:
                    await message.delete()
                except Exception:
                    pass
                await give_warning(message, reason="Link yuborish taqiqlangan")
                await increment_stat("links_deleted")
                if LOG_CHANNEL_ID:
                    await message.bot.send_message(LOG_CHANNEL_ID, f"🔗 Link o'chirildi: {user.full_name} ({user.id})\\n{text}")
                return
            badwords = read_lines(BADWORDS_FILE)
            bad, w = contains_badword(text, badwords)
            if bad:
                try:
                    await message.delete()
                except Exception:
                    pass
                await give_warning(message, reason=f"Yomon so'z: {w}")
                await increment_stat("badwords_deleted")
                if LOG_CHANNEL_ID:
                    await message.bot.send_message(LOG_CHANNEL_ID, f"🚫 Badword: {user.full_name} ({user.id}) -> {w}\\n{text}")

        def register_handlers(dp):
            dp.message.register(handle_text, content_types=["text"])
