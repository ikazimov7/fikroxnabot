\
        import json
        from pathlib import Path
        from threading import Lock
        from config import USERS_JSON, STATS_JSON

        _lock = Lock()

        def load_json(path=USERS_JSON):
            p = Path(path)
            if not p.exists():
                return {}
            try:
                return json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                return {}

        def save_json(data, path=USERS_JSON):
            p = Path(path)
            with _lock:
                p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        def ensure_user(uid):
            users = load_json()
            k = str(uid)
            if k not in users:
                users[k] = {"warns":0,"mutes":0,"bans":0,"quotes":0,"read_rules":False}
                save_json(users)

        def save_user_field(uid, field, value):
            users = load_json()
            users.setdefault(str(uid), {"warns":0,"mutes":0,"bans":0,"quotes":0,"read_rules":False})
            users[str(uid)][field] = value
            save_json(users)

        def increment_stat(key):
            stats = load_json(path=STATS_JSON)
            stats[key] = stats.get(key,0)+1
            save_json(stats, path=STATS_JSON)
