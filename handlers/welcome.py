\
        from aiogram import types
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
        from config import LOG_CHANNEL_ID
        from utils.json_manager import ensure_user, save_user_field
        import asyncio

        WELCOME_TEXT = (
            "👋 Salom, {name}!\n\n"
            "Guruhga xush kelibsiz!\n"
            "Iltimos, avval 📜 Qoidalarni o‘qib chiqing va pastdagi ✅ O‘qidim tugmasini bosing.\n\n"
            "Qoidalarni o'qiganingizni tasdiqlamaguningizcha yozish huquqingiz bo'lmaydi."
        )

        async def on_new_members(message: types.Message):
            for user in message.new_chat_members:
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton("📜 Qoidalar", url="https://telegra.ph/Fikrxona-Guruh-Qoidalari-09-15"),
                    InlineKeyboardButton("✅ O‘qidim", callback_data=f"read_rules:{user.id}")
                ]])
                sent = await message.chat.send_message(WELCOME_TEXT.format(name=user.full_name), reply_markup=kb)
                try:
                    await message.chat.restrict(user.id, permissions=ChatPermissions(can_send_messages=False))
                except Exception:
                    pass
                await ensure_user(user.id)
                save_user_field(user.id, "read_rules", False)
            try:
                await message.delete()
            except Exception:
                pass

        async def on_read_rules(call: types.CallbackQuery):
            data = call.data or ""
            if not data.startswith("read_rules:"):
                return
            try:
                uid = int(data.split(":",1)[1])
            except Exception:
                await call.answer("Xato", show_alert=True)
                return
            if call.from_user.id != uid and call.from_user.id not in []:
                pass
            try:
                await call.message.chat.restrict(uid, permissions=ChatPermissions(can_send_messages=True))
            except Exception:
                pass
            save_user_field(uid, "read_rules", True)
            try:
                await call.message.delete()
            except Exception:
                pass
            await call.answer("✅ Rahmat! Endi yozishingiz mumkin.")
            if LOG_CHANNEL_ID:
                await call.bot.send_message(LOG_CHANNEL_ID, f"✅ {call.from_user.full_name} ({call.from_user.id}) qoidalarni o‘qidi.")

        def register_handlers(dp):
            dp.message.register(on_new_members, types.MessageType.NEW_CHAT_MEMBERS)
            dp.callback_query.register(on_read_rules, lambda c: c.data and c.data.startswith("read_rules:"))
