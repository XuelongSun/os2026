from pathlib import Path

p = Path("hello.txt")

p.write_text("Hello OS\n", encoding="utf-8")
print(p.read_text(encoding="utf-8"), end="")
p.unlink()
