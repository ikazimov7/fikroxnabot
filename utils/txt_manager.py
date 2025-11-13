\
        from pathlib import Path
        from threading import Lock

        _lock = Lock()

        def read_lines(path):
            p = Path(path)
            if not p.exists():
                return []
            with p.open("r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]

        def append_line(path, text):
            p = Path(path)
            with _lock:
                with p.open("a", encoding="utf-8") as f:
                    f.write(text.rstrip("\n") + "\n")

        def remove_line(path, keyword):
            p = Path(path)
            if not p.exists():
                return
            with _lock:
                lines = read_lines(p)
                new = [l for l in lines if keyword.lower() not in l.lower()]
                p.write_text("\\n".join(new) + ("\\n" if new else ""), encoding="utf-8")
