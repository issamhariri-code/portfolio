# Teknisk översikt

## Teknisk stack

- **Språk:** Python 3
- **Spelmotor/Bibliotek:** Pygame
- **Versionskontroll:** Git + GitHub
- **Projektledning:** Scrum - GitHub Projects + dokument i `scrum/`

---

## Projektstruktur - root

- `game/` - all spelkod
  - `src/` - Pythonmoduler för spelet  
    - `main.py` - startpunkt, skapar fönster och kör game loop  
    - `config.py` - konfiguration: fönsterstorlek, FPS, titel, färger  
    - `function.py` - hjälpfunktioner (t.ex. rita bakgrund)  
    - `player.py` - logik för spelaren  
    - `tests/` - tester för spelets moduler
  - `assets/` - spelresurser  
    - `maps/` - kartor/banor  
    - `sprites/` - bilder för spelare och objekt  
    - `tilesets/` - tiles för kartor  
    - `sounds/` - ljudeffekter och musik
- `scrum/` - dokument för projektstyrning  
  - `product_vision.md` - övergripande mål för spelet  
  - `product_backlog.md` - samlad backlog med user stories  
  - `sprint_backlog.md` - utvalda stories/tasks för sprinten  
  - `daily-standups/` - dagliga rapporter  
  - `common_evals.md` - gemensamma referenspunkter/utvärdering  
  - `ideas.md`, `tech_overview.md` m.fl. - stöd-dokument för planering
- `docs/` - övrig dokumentation och guider
- `.venv/` - lokal Python-miljö (ignoreras i Git)
- `.github/` - CI/workflows och repo-konfiguration
- `requirements.txt` - lista på Pythonberoenden 

---

## Game loop och flöde

1. Projektet startas via `main.py`.
2. `pygame` initieras och fönstret skapas med värden från `config.py`.
3. Huvudloopen:
    - Lyssnar på events, t.ex. stänga fönster
    - ritar bakgrund via `draw_background()` i `function.py`
    - uppdaterar spelare, poäng och andra objekt
4. Skärmen uppdateras varje varv i loopen med `pygame.display.flip()` och begränsas av FPS från `config.py`.

Den här översikten används som stöd för både utveckling och redovisning så att hela gruppen har samma bild av den tekniska strukturen.
