"""Allow `python -m md_ddl` as an alias for the `md-ddl` command."""

import sys

from md_ddl.cli import main

if __name__ == "__main__":
    sys.exit(main())
