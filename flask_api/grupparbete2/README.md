# ElprisApp

Grupparbete med Flask och pandas som hämtar elpriser och visar dem i en tabell.

Installera miljön enligt [Flask-guiden](../README.md). Kör från `flask_api/grupparbete2/`:
```bash
python -m flask --app ElprisApp.app run
```

Öppna http://127.0.0.1:5000. Prisuppslag kräver den externa elpris-tjänsten.

## Tester
```bash
python -m pytest -q
```
Tester mot den externa tjänsten:
```bash
python -m pytest -q -m integration
```

Tester ligger i `tests/`. De lokala ändringarna i databehandlingen har bevarats.
