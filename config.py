\
        from pathlib import Path
        import os, json
        from dotenv import load_dotenv

        load_dotenv()

        TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
        if not TOKEN:
            raise SystemExit("Please set TELEGRAM_TOKEN in .env")

        ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
        LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID")) if os.getenv("LOG_CHANNEL_ID") else None

        DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        BADWORDS_FILE = DATA_DIR / "badwords.txt"
        QUOTES_PENDING_FILE = DATA_DIR / "quotes_pending.txt"
        QUOTES_APPROVED_FILE = DATA_DIR / "quotes_approved.txt"
        QUOTES_REJECTED_FILE = DATA_DIR / "quotes_rejected.txt"
        USERS_JSON = DATA_DIR / "users.json"
        STATS_JSON = DATA_DIR / "stats.json"

        WARN_LIMIT = int(os.getenv("WARN_LIMIT", "3"))
        MUTE_LIMIT = int(os.getenv("MUTE_LIMIT", "3"))
        MUTE_DURATION_SECONDS = int(os.getenv("MUTE_DURATION_SECONDS", str(60*60)))
        AUTO_DELETE_SECONDS = int(os.getenv("AUTO_DELETE_SECONDS", "30"))

        # create default files if missing
        for p in (BADWORDS_FILE, QUOTES_PENDING_FILE, QUOTES_APPROVED_FILE, QUOTES_REJECTED_FILE):
            if not p.exists():
                p.write_text("", encoding="utf-8")
        if not USERS_JSON.exists():
            USERS_JSON.write_text("{}", encoding="utf-8")
        if not STATS_JSON.exists():
            STATS_JSON.write_text(json.dumps({
                "links_deleted":0,"badwords_deleted":0,"warnings_given":0,"mutes_given":0,"bans_given":0,"files_blocked":0
            }), encoding="utf-8")
