#!/usr/bin/env python

from pathlib import Path

import mkdocs_gen_files

for path in Path("braincube_connector").glob("**/*.py"):
    if "__init__" in path.name:
        continue

    doc_path = Path("reference", path.relative_to(".")).with_suffix(".md")

    with mkdocs_gen_files.open(doc_path, "w") as f:
        ident = ".".join(path.relative_to(".").with_suffix("").parts)
        print("::: " + ident, file=f)

    mkdocs_gen_files.set_edit_path(doc_path, Path("..", path))
