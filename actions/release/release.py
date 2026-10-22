"""Checks the files of a release and writes its short notes from the changelog.

usage: python release.py check <version> <guide> <list-out> <patterns, one per line>
       python release.py notes <version> <guide> <changelog> <notes-out>
guide: inside (a PDF guide in every zip), beside (a PDF among the files, next to
an APK), none. Standard library only: it runs on every GitHub runner as is.
"""
import glob
import os
import re
import sys
import zipfile


class ReleaseError(Exception):
    pass


GUIDE_LINE = {
    "inside": "La guida PDF è dentro ogni zip.",
    "beside": "La guida PDF è accanto all'APK.",
    "none": "",
}


def _section(md, version):
    # the first "## " heading holding the version as a whole word;
    # "1.13-SNAPSHOT" falls back to the "1.13" section
    for v in dict.fromkeys([version, version.split("-")[0]]):
        head = re.search(r"^##\s.*(?<![\w.])" + re.escape(v) + r"(?![\w.]).*$", md, re.M)
        if head:
            body = md[head.end():]
            end = re.search(r"^##\s", body, re.M)
            return body[: end.start()] if end else body
    raise ReleaseError(f"changelog has no section for {version}")


def _clause(text):
    # first clause, at most ~180 characters, never ending inside `code` or *italics*
    c = re.split(r";\s|\.\s|\.$", text.strip())[0].strip()
    if len(c) > 180:
        c = re.sub(r"\s+\S*$", "", c[:180])
        for mark in ("`", "*"):
            if c.count(mark) % 2:
                c = c[: c.rindex(mark)].strip()
        c = re.sub(r"[,;:]$", "", c) + "…"
    return c


def _short(item):
    m = re.match(r"^\*\*(.+?)\*\*(:?)\s*(.*)$", item)
    if not m:
        return _clause(item)
    rest = _clause(m.group(3))
    return f"**{m.group(1)}**" + ((": " if m.group(2) else " ") + rest if rest else "")


def notes(md, version, guide="inside"):
    groups = []
    item = False  # the last line belongs to an item: indented lines continue it
    for line in _section(md, version).splitlines():
        bold = re.fullmatch(r"\*\*(.+?)\*\*:?", line.strip())
        if line.startswith("### ") or bold:
            groups.append([line[4:].strip() if line.startswith("### ") else bold.group(1).strip(), []])
            item = False
        elif line.startswith("- "):
            if not groups:
                groups.append(["", []])
            groups[-1][1].append(line[2:].strip())
            item = True
        elif item and line[:1].isspace() and line.strip():
            groups[-1][1][-1] += " " + line.strip()
        else:
            item = False
    parts = [(f"### {title}\n\n" if title else "") + "\n".join(f"- {_short(i)}" for i in items) for title, items in groups if items]
    if GUIDE_LINE[guide]:
        parts.append(GUIDE_LINE[guide])
    return "\n\n".join(parts) + "\n"


def check(patterns, version, guide="inside"):
    files = []
    for pattern in patterns:
        found = sorted(glob.glob(pattern))
        if not found:
            raise ReleaseError(f"no file matches {pattern}")
        files += found
    for f in files:
        name = os.path.basename(f)
        if version not in name:
            raise ReleaseError(f"version {version} missing in {name}")
        if guide == "inside" and name.lower().endswith(".zip"):
            with zipfile.ZipFile(f) as z:
                if not any(n.lower().endswith(".pdf") for n in z.namelist()):
                    raise ReleaseError(f"no PDF guide inside {name}")
    if guide == "beside" and not any(f.lower().endswith(".pdf") for f in files):
        raise ReleaseError("no PDF guide among the files")
    return files


def main(argv):
    cmd, version, guide = argv[1], argv[2], argv[3]
    if guide not in GUIDE_LINE:
        raise ReleaseError(f"guide must be inside, beside or none, not {guide}")
    if cmd == "check":
        patterns = [p.strip() for p in argv[5].splitlines() if p.strip()]
        files = check(patterns, version, guide)
        with open(argv[4], "w", encoding="utf-8", newline="\n") as out:
            out.write("".join(f + "\n" for f in files))
        print("Release files:\n" + "".join(f"  {f}\n" for f in files), end="")
    elif cmd == "notes":
        with open(argv[4], encoding="utf-8") as f:
            md = notes(f.read(), version, guide)
        with open(argv[5], "w", encoding="utf-8", newline="\n") as out:
            out.write(md)
        print(md, end="")
    else:
        raise ReleaseError(f"unknown command {cmd}")


if __name__ == "__main__":
    # Windows runners print with cp1252: notes in Italian (è, →) go to the log as UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main(sys.argv)
    except ReleaseError as e:
        print(f"::error::{e}")
        sys.exit(1)
