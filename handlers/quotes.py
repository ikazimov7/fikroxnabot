\
        from aiogram import types
        from config import QUOTES_APPROVED_FILE, QUOTES_PENDING_FILE, QUOTES_REJECTED_FILE, LOG_CHANNEL_ID, AUTO_DELETE_SECONDS
        from utils.txt_manager import read_lines, append_line
        from utils.json_manager import load_json, save_json
        import random, asyncio, time
        from pathlib import Path

        def generate_qid():
            return f"{int(time.time()*1000)}_{random.randint(100,999)}"

        async def cmd_quote(message: types.Message):
            quotes = read_lines(QUOTES_APPROVED_FILE)
            if not quotes:
                m = await message.reply("📭 Tasdiqlangan iqtiboslar yo'q.")
                await asyncio.sleep(AUTO_DELETE_SECONDS)
                try:
                    await m.delete()
                except Exception:
                    pass
                return
            q = random.choice(quotes)
            m = await message.reply(f"💬 {q}")
            await asyncio.sleep(AUTO_DELETE_SECONDS)
            try:
                await m.delete()
            except Exception:
                pass

        async def cmd_aq(message: types.Message):
            text = message.get_args().strip()
            if not text and message.reply_to_message and message.reply_to_message.text:
                text = message.reply_to_message.text.strip()
            if not text:
                m = await message.reply("✍️ /aq <iqtibos matni> yoki /aq ga javob orqali yuboring.")
                await asyncio.sleep(AUTO_DELETE_SECONDS)
                try:
                    await m.delete()
                except Exception:
                    pass
                return
            qid = generate_qid()
            record = f"{qid}|{message.from_user.id}|{message.from_user.username or message.from_user.full_name}|{text.replace('|','/|')}|{time.time()}"
            append_line(QUOTES_PENDING_FILE, record)
            await message.reply("📨 Iqtibosingiz adminlarga yuborildi.")
            if LOG_CHANNEL_ID:
                await message.bot.send_message(LOG_CHANNEL_ID, f"🆕 New quote {qid} from {message.from_user.full_name} ({message.from_user.id})\\n{text}\\n/qa_{qid} or /qr_{qid}")

        async def cmd_qa(message: types.Message):
            from config import ADMIN_IDS
            if message.from_user.id not in ADMIN_IDS:
                return
            text = message.text.strip()
            if not text.startswith("/qa_"):
                return
            qid = text.split("_",1)[1]
            pend = read_lines(QUOTES_PENDING_FILE)
            found = None
            rest = []
            for line in pend:
                if line.startswith(qid+"|"):
                    found = line
                else:
                    rest.append(line)
            Path(QUOTES_PENDING_FILE).write_text("\\n".join(rest)+("\\n" if rest else ""), encoding="utf-8")
            if found:
                parts = found.split("|",4)
                qtext = parts[3]
                append_line(QUOTES_APPROVED_FILE, f"{qtext} | @{parts[2]}")
                # increment user's quote count
                try:
                    users = load_json()
                    uid = parts[1]
                    users.setdefault(uid, {"warns":0,"mutes":0,"bans":0,"quotes":0,"read_rules":False})
                    users[uid]["quotes"] = users[uid].get("quotes",0)+1
                    save_json(users)
                except Exception:
                    pass
                await message.reply("✅ Iqtibos tasdiqlandi.")
                if LOG_CHANNEL_ID:
                    await message.bot.send_message(LOG_CHANNEL_ID, f"✅ Quote {qid} approved by {message.from_user.full_name}")
            else:
                await message.reply("❌ Topilmadi.")

        async def cmd_qr(message: types.Message):
            from config import ADMIN_IDS
            if message.from_user.id not in ADMIN_IDS:
                return
            text = message.text.strip()
            if not text.startswith("/qr_"):
                return
            qid = text.split("_",1)[1]
            pend = read_lines(QUOTES_PENDING_FILE)
            found = None
            rest = []
            for line in pend:
                if line.startswith(qid+"|"):
                    found = line
                else:
                    rest.append(line)
            Path(QUOTES_PENDING_FILE).write_text("\\n".join(rest)+("\\n" if rest else ""), encoding="utf-8")
            if found:
                append_line(QUOTES_REJECTED_FILE, found)
                await message.reply("❌ Iqtibos rad etildi.")
                if LOG_CHANNEL_ID:
                    await message.bot.send_message(LOG_CHANNEL_ID, f"❌ Quote {qid} rejected by {message.from_user.full_name}")
            else:
                await message.reply("❌ Topilmadi.")

        async def cmd_myq(message: types.Message):
            uid = str(message.from_user.id)
            pend = read_lines(QUOTES_PENDING_FILE)
            appr = read_lines(QUOTES_APPROVED_FILE)
            rej = read_lines(QUOTES_REJECTED_FILE)
            pending_user = [p for p in pend if f"|{uid}|" in p]
            from utils.json_manager import load_json
            users = load_json()
            count = users.get(uid, {}).get("quotes",0)
            text = f"📚 Sizning iqtiboslaringiz:\\n✅ Tasdiqlangan: {count}\\n⏳ Kutilayotgan: {len(pending_user)}\\n❌ Rad etilgan: {len([r for r in rej if uid in r])}"
            m = await message.reply(text)
            await asyncio.sleep(AUTO_DELETE_SECONDS)
            try:
                await m.delete()
            except Exception:
                pass

        def register_handlers(dp):
            dp.message.register(cmd_quote, commands=["quote"])
            dp.message.register(cmd_aq, commands=["aq"])
            dp.message.register(cmd_qa, lambda m: m.text and m.text.startswith("/qa_"))
            dp.message.register(cmd_qr, lambda m: m.text and m.text.startswith("/qr_"))
            dp.message.register(cmd_myq, commands=["myq"])
