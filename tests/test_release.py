# Tests for actions/release/release.py. Run: python3 -m unittest discover -s tests
import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "actions", "release"))
import release  # noqa: E402

CHANGELOG = """# Changelog

## 2.0.0 — 2026-11-01

### Novità

- **Modalità di salto**: il brano scelto va in coda e parte a fine sezione; `J` salta subito.
- Nuovo tasto per il loop.

### Correzioni

- **Motore**: con il loop acceso non salta più al brano dopo.

## 1.9.0 — 2026-10-01

- Vecchia funzione.
"""

DIERRE = """# Guida

## Novità della versione 2.9.20

- Inventario: le quantità doppie di agosto non si sommano più due volte. Dettagli nel capitolo 4.

## Novità della versione 2.9.19

- Vecchio.
"""

# dierre's guide: bold paragraphs as groups, items wrapped on several lines
WRAPPED = """## Novità della versione 2.9.20

**Versione e download**

- La versione si vede nel nome dell'exe (`InventarioApp-2.9.20.exe`), nel titolo della finestra di avvio e in
  questa guida, che ora è nello zip.
- Lo zip è più leggero, da 63 a 43 MB: non contiene più WPF, che l'app non usa.

**Merge**

- I doppioni uguali si contano una volta.
"""

SNAPSHOT = """## 1.13

- **DMX**: universi oltre il 4 corretti.
"""


class NotesTest(unittest.TestCase):
    def test_one_short_line_per_item_grouped(self):
        md = release.notes(CHANGELOG, "2.0.0", guide="inside")
        self.assertIn("### Novità", md)
        self.assertIn("### Correzioni", md)
        self.assertIn("- **Modalità di salto**: il brano scelto va in coda e parte a fine sezione\n", md)
        self.assertIn("- Nuovo tasto per il loop\n", md)
        self.assertIn("- **Motore**: con il loop acceso non salta più al brano dopo\n", md)
        self.assertNotIn("Vecchia funzione", md)
        self.assertIn("La guida PDF è dentro ogni zip.", md)

    def test_long_items_are_cut(self):
        long = "## 1.0.0\n\n- " + "parola " * 80 + "\n"
        line = [l for l in release.notes(long, "1.0.0", guide="none").splitlines() if l.startswith("- ")][0]
        self.assertLessEqual(len(line), 190)  # "- " + 180 characters + "…"
        self.assertTrue(line.endswith("…"))

    def test_version_inside_a_heading_and_snapshot_versions(self):
        self.assertIn("- Inventario: le quantità doppie di agosto non si sommano più due volte\n",
                      release.notes(DIERRE, "2.9.20", guide="inside"))
        md = release.notes(SNAPSHOT, "1.13-SNAPSHOT", guide="beside")
        self.assertIn("- **DMX**: universi oltre il 4 corretti\n", md)
        self.assertIn("La guida PDF è accanto all'APK.", md)

    def test_wrapped_items_and_bold_paragraph_groups(self):
        md = release.notes(WRAPPED, "2.9.20", guide="inside")
        self.assertIn("### Versione e download\n\n", md)
        self.assertIn("### Merge\n\n- I doppioni uguali si contano una volta\n", md)
        self.assertIn("- La versione si vede nel nome dell'exe (`InventarioApp-2.9.20.exe`), nel titolo della finestra di avvio e in questa guida, che ora è nello zip\n", md)
        self.assertIn("- Lo zip è più leggero, da 63 a 43 MB: non contiene più WPF, che l'app non usa\n", md)

    def test_missing_section_is_an_error(self):
        with self.assertRaisesRegex(release.ReleaseError, "no section for 3.0.0"):
            release.notes(CHANGELOG, "3.0.0", guide="inside")
        # 2.0.0 must not match 12.0.0
        with self.assertRaises(release.ReleaseError):
            release.notes("## 12.0.0\n\n- x\n", "2.0.0", guide="none")


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(lambda: __import__("shutil").rmtree(self.dir))

    def zip(self, name, members):
        path = os.path.join(self.dir, name)
        with zipfile.ZipFile(path, "w") as z:
            for m in members:
                z.writestr(m, "x")
        return path

    def file(self, name):
        path = os.path.join(self.dir, name)
        open(path, "w").close()
        return path

    def test_zips_with_the_version_and_the_guide_inside(self):
        self.zip("app-2.0.0-win-x64.zip", ["app-2.0.0.exe", "App-2.0.0-Guida.pdf"])
        self.zip("app-2.0.0-linux-x64.zip", ["bin/app-2.0.0", "docs/App-2.0.0-Guida.pdf"])
        files = release.check([os.path.join(self.dir, "*.zip")], "2.0.0", guide="inside")
        self.assertEqual(sorted(os.path.basename(f) for f in files), ["app-2.0.0-linux-x64.zip", "app-2.0.0-win-x64.zip"])

    def test_a_zip_without_the_guide_is_refused(self):
        self.zip("app-2.0.0-win-x64.zip", ["app-2.0.0.exe"])
        with self.assertRaisesRegex(release.ReleaseError, "no PDF guide inside app-2.0.0-win-x64.zip"):
            release.check([os.path.join(self.dir, "*.zip")], "2.0.0", guide="inside")

    def test_names_must_carry_the_version(self):
        self.zip("app-win-x64.zip", ["app.exe", "Guida.pdf"])
        with self.assertRaisesRegex(release.ReleaseError, "version 2.0.0 missing in app-win-x64.zip"):
            release.check([os.path.join(self.dir, "*.zip")], "2.0.0", guide="inside")

    def test_android_apk_with_the_guide_beside(self):
        apk = self.file("PocketDMX-v1.13.apk")
        with self.assertRaisesRegex(release.ReleaseError, "no PDF guide among the files"):
            release.check([apk], "1.13", guide="beside")
        pdf = self.file("PocketDMX-1.13-Guida.pdf")
        self.assertEqual(release.check([apk, pdf], "1.13", guide="beside"), [apk, pdf])

    def test_a_pattern_without_files_is_an_error(self):
        with self.assertRaisesRegex(release.ReleaseError, "no file matches"):
            release.check([os.path.join(self.dir, "*.zip")], "2.0.0", guide="none")


if __name__ == "__main__":
    unittest.main()
