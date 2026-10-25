"""Command implementations. Each takes (args, config) and returns an exit code."""
from __future__ import annotations

from cli_starter.config import Config


def greet(args, config: Config) -> int:
    name = args.name.strip()
    if not name:
        print("error: --name must not be empty")
        return 2
    message = f"{config.greeting}, {name}!"
    if config.loud:
        message = message.upper()
    print(message)
    return 0
