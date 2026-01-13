from pathlib import Path

files = [Path("frontend/index.html"), Path("frontend/tarot-reader.html")]
changed = []
for p in files:
    if not p.exists():
        continue
    s = p.read_text(encoding="utf-8")
    new = s.replace("tarotdeck-main/art/", "backend/art/")
    new = new.replace("tarotdeck-main/", "backend/")
    if s != new:
        p.write_text(new, encoding="utf-8")
        changed.append(str(p))

if changed:
    print("Updated files:")
    for c in changed:
        print(" -", c)
else:
    print("No files needed changes.")
