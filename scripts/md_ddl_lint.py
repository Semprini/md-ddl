#!/usr/bin/env python3
"""
Compatibility shim for the MD-DDL linter.

The linter now lives in the installable package at `src/md_ddl/lint.py` and is
exposed as `md-ddl lint`. This wrapper keeps the documented in-repo invocation
working from a plain source checkout, with no install step:

    python scripts/md_ddl_lint.py <path> [<path> ...] [options]

Requires: Python 3.9+, pyyaml   (pip install pyyaml)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from md_ddl.lint import main

if __name__ == "__main__":
    sys.exit(main(prog="python scripts/md_ddl_lint.py"))
