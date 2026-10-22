# Azioni condivise di Darkglassd3v — istruzioni per Claude

Repo pubblico con le azioni usate da tutti i progetti dell'utente. Leggi `TODO.md`.

- `actions/release`: azione composita che controlla i file di una release, scrive
  le note brevi dal changelog e li allega alla release con `gh`. Gira dentro il job
  del progetto: **mai** `actions/upload-artifact` (lo spazio delle Actions si esaurisce,
  gli asset delle release no).
- Solo libreria standard di Python (gira su Ubuntu, macOS e Windows senza installare nulla).
- Test: `python3 -m unittest discover -s tests`. Flusso TDD: commit RED e GREEN separati,
  `TODO.md` aggiornato in ogni commit, messaggi Conventional Commits con l'evidenza.
- Commenti nel codice in inglese, documentazione in italiano.
- Versioni dell'azione con i tag `v1`, `v1.x.y`: i progetti usano `@v1`.
