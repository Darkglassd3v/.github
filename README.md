# Azioni condivise di Darkglassd3v

## `actions/release`

Pubblica la release di un progetto **senza artefatti delle Actions** (lo spazio degli
artefatti si esaurisce, gli asset delle release no). Si usa come ultimo passo del job
che costruisce i file:

```yaml
permissions:
  contents: write

jobs:
  release:
    runs-on: windows-latest
    steps:
      # … build: zip con la versione nel nome e la guida PDF dentro …
      - uses: Darkglassd3v/.github/actions/release@v1
        with:
          version: 2.9.20
          files: |
            InventarioApp-win-x64-2.9.20.zip
          changelog: docs/InventarioApp.md
```

Cosa fa:

1. **Controlla i file**: ogni nome contiene la versione; con `guide: inside` (predefinito)
   ogni zip contiene la guida PDF, con `guide: beside` un PDF sta accanto (APK Android),
   `guide: none` non controlla.
2. **Scrive le note brevi**: dalla sezione del changelog con la versione nel titolo
   (`## 2.9.20 — …`, `## Novità della versione 2.9.20`; per `1.13-SNAPSHOT` vale `## 1.13`),
   una riga per voce, divise per `### Novità` / `### Correzioni`, più dove sta la guida.
3. **Pubblica** con `gh` solo quando il workflow gira per un tag (`publish: auto`).
   Sulle pull request fa solo i controlli. `replace: true` aggiorna una release esistente
   (build snapshot); le versioni con `-` (es. `1.13-SNAPSHOT`) sono pre-release.

Input: `version`, `files` (un glob per riga), `changelog`, `guide`, `tag`
(predefinito `v<versione>`), `title`, `prerelease`, `publish`, `replace`.

Test: `python3 -m unittest discover -s tests`.
