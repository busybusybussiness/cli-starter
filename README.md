# cli-starter

A small, zero-dependency Python command-line app template. Clone it, rename the package, and start adding commands.

- Python 3.11+ (stdlib only: argparse, tomllib, logging, unittest)
- Subcommands with a tested dispatch table
- Config from a TOML file with defaults and validation
- Unit tests and a GitHub Actions CI workflow

## Quick start

    # from the repo root (Windows PowerShell: $env:PYTHONPATH="src")
    PYTHONPATH=src python -m cli_starter --help
    PYTHONPATH=src python -m cli_starter greet --name Ada
    PYTHONPATH=src python -m cli_starter --config examples/config.toml greet --name Ada
    python -m unittest discover -s tests -v

## Layout

    src/cli_starter/
      __init__.py     version
      __main__.py     python -m entry point
      config.py       TOML loading + validation
      cli.py          argparse parser and command dispatch
      commands.py     command implementations (add yours here)
    tests/            unittest suite
    examples/config.toml

## Adding a command

1. Write a function in `commands.py` that takes `(args, config)` and returns an int exit code.
2. Register it in `cli.py` with `sub.add_parser(...)` and `set_defaults(func=...)`.
3. Add a test in `tests/`.

## License

MIT. See LICENSE.
