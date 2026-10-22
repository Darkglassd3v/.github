# TODO — azioni condivise di Darkglassd3v

Richiesta dell'utente (2026-10-22): pubblicare le release di tutti i progetti senza
artefatti delle Actions (lo spazio si esaurisce; gli asset delle release no).

## In corso

- [x] R1.1 (v1.1.0): voci su più righe e gruppi in grassetto (`**Merge**`, come nella guida di dierre)
  - [x] RED `tests/test_release.py`
  - [x] GREEN `release.py` (righe unite, gruppi in grassetto, limite a 180 caratteri), tag `v1.1.0`, `v1` spostato
- [x] R1.2 (v1.1.1): su Windows la console stampa in cp1252: una nota con «→» fermava l'azione (visto nel log della prova di dierre: «è» diventava «�»)
  - [x] RED `tests/test_release.py` (`PYTHONIOENCODING=cp1252`)
  - [x] GREEN: stdout in UTF-8, tag `v1.1.1`, `v1` spostato
- [x] R2: dierre e openset usano `Darkglassd3v/.github/actions/release@v1` (openset PR #6 unita; dierre su `release/v2.9.20`, provata con la run 39867875177 senza pubblicare)

## Da fare

### R1 — azione `actions/release`
- [x] RED `tests/test_release.py`: note brevi dal changelog (una riga per voce, gruppi `###`, intestazione con la versione anche dentro un titolo, versione `-SNAPSHOT` sulla sezione base, sezione mancante = errore); controllo dei file (versione nel nome, guida PDF dentro ogni zip, oppure PDF accanto all'APK, glob senza file = errore)
- [x] GREEN `actions/release/release.py` + `action.yml` (controlli, note, `gh release create/upload`, solo dai tag salvo `publish`)
- [x] CI: test e prova dell'azione su Ubuntu, Windows e macOS, senza pubblicare (`.github/workflows/ci.yml`)
- [x] Repo pubblico `Darkglassd3v/.github`, tag `v1` e `v1.0.0` (CI verde su Ubuntu, Windows, macOS)

### R2 — progetti
- [x] dierre: ultimo passo di `build-windows-exe.yml` con l'azione (solo lo zip, la guida è dentro; note da `docs/InventarioApp.md`)
- [x] openset: `release.yml` usa l'azione al posto di `scripts/release-notes.js` + `softprops/action-gh-release`

## Esclusi

- artnet-android, iptv-core-suite, sciclub-donbosco e gli altri: vecchi o non servono (utente, 2026-10-22); i progetti principali sono dierre e openset

## Regole

Vedi `CLAUDE.md`.
