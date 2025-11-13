\
        from aiogram import types
        from aiogram.types import ChatPermissions
        from utils.json_manager import load_json, save_json, increment_stat
        from config import WARN_LIMIT, MUTE_LIMIT, MUTE_DURATION_SECONDS, LOG_CHANNEL_ID
        import asyncio
        from datetime import datetime, timedelta

        async def give_warning(message: types.Message, reason: str = ""):
            uid = str(message.from_user.id)
            users = load_json()
            users.setdefault(uid, {"warns":0,"mutes":0,"bans":0,"quotes":0,"read_rules":False})
            users[uid]["warns"] = users[uid].get("warns",0) + 1
            save_json(users)
            increment_stat("warnings_given")
            warns = users[uid]["warns"]
            try:
                msg = await message.reply(f"⚠️ {message.from_user.full_name} ogohlantirildi ({warns}/{WARN_LIMIT}).\\nSabab: {reason}")
                await asyncio.sleep(8)
                await msg.delete()
            except Exception:
                pass
            if warns >= WARN_LIMIT:
                users[uid]["warns"]=0
                users[uid]["mutes"]=users[uid].get("mutes",0)+1
                save_json(users)
                increment_stat("mutes_given")
                try:
                    until = datetime.utcnow() + timedelta(seconds=MUTE_DURATION_SECONDS)
                    await message.bot.restrict_chat_member(message.chat.id, int(uid), permissions=ChatPermissions(can_send_messages=False), until_date=until)
                except Exception:
                    pass
                try:
                    m2 = await message.reply(f"🔇 {message.from_user.full_name} mute qilindi.")
                    await asyncio.sleep(8)
                    await m2.delete()
                except Exception:
                    pass
                if users[uid].get("mutes",0) >= MUTE_LIMIT:
                    try:
                        await message.bot.ban_chat_member(message.chat.id, int(uid))
                    except Exception:
                        pass
                    users[uid]["bans"] = users[uid].get("bans",0)+1
                    save_json(users)
                    increment_stat("bans_given")
                    if LOG_CHANNEL_ID:
                        try:
                            await message.bot.send_message(LOG_CHANNEL_ID, f"🚫 Ban: {message.from_user.full_name} ({uid})")
                        except Exception:
                            pass

        def register_handlers(dp):
            async def cmd_info(message: types.Message):
                uid = str(message.from_user.id)
                users = load_json()
                data = users.get(uid, {"warns":0,"mutes":0,"bans":0,"quotes":0})
                try:
                    m = await message.reply(
                        f"👤 Siz haqingizda:\\n⚠️ Ogohlantirishlar: {data.get('warns',0)}\\n🔇 Mutes: {data.get('mutes',0)}\\n💬 Iqtiboslar: {data.get('quotes',0)}"
                    )
                    await asyncio.sleep(30)
                    await m.delete()
                except Exception:
                    pass
            dp.message.register(cmd_info, commands=["info"])
