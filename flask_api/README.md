# Flask och API – Programmering 2

Avslutade kursprojekt och lektionsmaterial som tidigare låg i repot `flask_api`.

- [BörsLexikon](examination/README.md) – examinationsprojekt med aktiedata från Marketstack.
- [ElprisApp](grupparbete2/README.md) – grupparbete med elpriser och pandas.
- [Lektionsövningar](lektioner/README.md) – undervisningsexempel med varierande färdigställandegrad.

## Gemensam miljö
Kör från den här mappen:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Varje app startas separat enligt sin README. Vanliga tester körs utan externa API-anrop. Integrationstester aktiveras uttryckligen och kräver fungerande externa tjänster.
