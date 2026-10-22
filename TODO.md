# TODO — azioni condivise di Darkglassd3v

Richiesta dell'utente (2026-10-22): pubblicare le release di tutti i progetti senza
artefatti delle Actions (lo spazio si esaurisce; gli asset delle release no).

## In corso

- [ ] `actions/release`: azione composita (gira nel job del progetto, niente artefatti)

## Da fare

### R1 — azione `actions/release`
- [x] RED `tests/test_release.py`: note brevi dal changelog (una riga per voce, gruppi `###`, intestazione con la versione anche dentro un titolo, versione `-SNAPSHOT` sulla sezione base, sezione mancante = errore); controllo dei file (versione nel nome, guida PDF dentro ogni zip, oppure PDF accanto all'APK, glob senza file = errore)
- [ ] GREEN `actions/release/release.py` + `action.yml` (controlli, note, `gh release create/upload`, solo dai tag salvo `publish`)
- [ ] CI: test e prova dell'azione su Ubuntu e Windows, senza pubblicare
- [ ] Repo pubblico `Darkglassd3v/.github`, tag `v1`

### R2 — progetti
- [ ] dierre: ultimo passo di `build-windows-exe.yml` con l'azione (solo lo zip, la guida è dentro; note da `docs/InventarioApp.md`)
- [ ] artnet-android: release con l'azione (APK + PDF accanto; la guida PDF di PocketDMX non esiste ancora)
- [ ] iptv-core-suite: niente `upload-artifact` in `build.yml`; release firmata manuale con l'azione

## Regole

Vedi `CLAUDE.md`.
