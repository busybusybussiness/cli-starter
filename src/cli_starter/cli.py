"""Argument parsing and dispatch."""
from __future__ import annotations

import argparse
import logging
import sys

from cli_starter import __version__
from cli_starter import commands
from cli_starter.config import ConfigError, load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cli-starter", description="Starter CLI app.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", metavar="PATH", help="TOML config file")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    sub = parser.add_subparsers(dest="command", required=True)

    greet = sub.add_parser("greet", help="print a greeting")
    greet.add_argument("--name", required=True, help="who to greet")
    greet.set_defaults(func=commands.greet)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )
    try:
        config = load_config(args.config)
    except ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return args.func(args, config)
