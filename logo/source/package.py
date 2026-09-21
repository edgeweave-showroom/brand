#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Technologies Edgeweave
# SPDX-License-Identifier: MIT
"""Bundle the logo files for people who will not clone the repository.

    ./package.py v1.0        write dist/edgeweave-logo.zip, for release v1.0

The zip unpacks to a single edgeweave-logo/ directory: symbol/ and full/ as
they are under logo/, the terms of use as LICENSE.txt, and a README made of a
short header and the "Picking a file" section of logo/README.md. Sources,
generator and ASCII rendering stay in the repository; the zip is the finished
marks only. CI builds it on every pull request, and publishes a release with
it whenever a push to main changes any of its content, so the latest one is
always at releases/latest/download/edgeweave-logo.zip.
"""

import argparse
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOGO = HERE.parent
ROOT = LOGO.parent
NAME = "edgeweave-logo"
DIRS = ("symbol", "full")
TERMS = ROOT / "LICENSES" / "LicenseRef-Edgeweave-Brand.txt"
GUIDE = "Picking a file"
REPO = "https://github.com/edgeweave-showroom/brand"

HEADER = """\
# Edgeweave logo

Release {version}: the symbol and the full logo of Edgeweave, in every
variant. Sources, generator and later releases are at
{repo}.

## Terms of use

Short version; the full terms are in LICENSE.txt.

- Use the marks as provided to refer to Edgeweave: articles, talks,
  documentation, "works with Edgeweave" notices, banners in tools that
  integrate with it.
- Do not alter them, do not make them part of your own branding, do not imply
  endorsement.

"""


def guide() -> str:
    """Cut the "Picking a file" section out of logo/README.md, heading included."""
    readme = LOGO / "README.md"
    for section in readme.read_text(encoding="utf-8").split("\n## ")[1:]:
        if section.startswith(f"{GUIDE}\n"):
            return f"## {section}"
    sys.exit(f"{readme}: no '## {GUIDE}' section")


def main() -> None:
    """Write the zip, named after the release given on the command line."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("version", help="the release tag, written into the README")
    version: str = parser.parse_args().version

    files = sorted(p for d in DIRS for p in (LOGO / d).rglob("*") if p.is_file())
    out = ROOT / "dist" / f"{NAME}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as bundle:
        readme = HEADER.format(version=version, repo=REPO) + guide()
        bundle.writestr(f"{NAME}/README.md", readme)
        bundle.write(TERMS, f"{NAME}/LICENSE.txt")
        for path in files:
            bundle.write(path, f"{NAME}/{path.relative_to(LOGO).as_posix()}")
    sys.stdout.write(f"{len(files) + 2} files in {out}\n")


if __name__ == "__main__":
    main()
