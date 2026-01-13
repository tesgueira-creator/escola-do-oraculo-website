from pathlib import Path
import shutil

src = Path("backend/art")
dst = Path("frontend/assets/art")
if not src.exists():
    print("Source does not exist:", src)
else:
    dst.mkdir(parents=True, exist_ok=True)
    files = 0
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, dst / f.name)
            files += 1
    print(f"Copied {files} files to {dst}")
