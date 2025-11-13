\
        from utils.json_manager import load_json, save_json, increment_stat
        from config import WARN_LIMIT, MUTE_LIMIT, MUTE_DURATION_SECONDS, LOG_CHANNEL_ID
        from aiogram.types import ChatPermissions
        from datetime import datetime, timedelta

        async def give_warning(message, reason=""):
            uid = str(message.from_user.id)
            users = load_json()
            users.setdefault(uid, {"warns":0,"mutes":0,"bans":0,"quotes":0,"read_rules":False})
            users[uid]["warns"] = users[uid].get("warns",0) + 1
            save_json(users)
            increment_stat("warnings_given")
            warns = users[uid]["warns"]
            if warns >= WARN_LIMIT:
                users[uid]["warns"] = 0
                users[uid]["mutes"] = users[uid].get("mutes",0) + 1
                save_json(users)
                increment_stat("mutes_given")
                try:
                    until = datetime.utcnow() + timedelta(seconds=MUTE_DURATION_SECONDS)
                    await message.bot.restrict_chat_member(message.chat.id, int(uid), permissions=ChatPermissions(can_send_messages=False), until_date=until)
                except Exception:
                    pass
                if users[uid].get("mutes",0) >= MUTE_LIMIT:
                    try:
                        await message.bot.ban_chat_member(message.chat.id, int(uid))
                    except Exception:
                        pass
                    users[uid]["bans"] = users[uid].get("bans",0) + 1
                    save_json(users)
                    increment_stat("bans_given")
                    if LOG_CHANNEL_ID:
                        try:
                            await message.bot.send_message(LOG_CHANNEL_ID, f"🚫 Ban: {message.from_user.full_name} ({uid})")
                        except Exception:
                            pass
