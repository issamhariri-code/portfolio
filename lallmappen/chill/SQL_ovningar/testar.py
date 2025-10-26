from pathlib import Path

BASE = Path(__file__).parent        # mappen där testar.py ligger
TXT = BASE / "enlitentext.txt"      # filen bredvid skriptet

with TXT.open("r", encoding="utf-8") as file_obj:
    innehåll = file_obj.read().split()  # .split() tar bort \n automatiskt
    print(innehåll)
