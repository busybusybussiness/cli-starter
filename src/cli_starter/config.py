"""TOML config loading with defaults and validation."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Config:
    greeting: str = "Hello"
    loud: bool = False


def load_config(path: str | None) -> Config:
    if path is None:
        return Config()
    p = Path(path)
    if not p.is_file():
        raise ConfigError(f"config file not found: {p}")
    try:
        data = tomllib.loads(p.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"invalid TOML in {p}: {exc}") from exc
    greeting = data.get("greeting", Config.greeting)
    loud = data.get("loud", Config.loud)
    if not isinstance(greeting, str) or not greeting.strip():
        raise ConfigError("greeting must be a non-empty string")
    if not isinstance(loud, bool):
        raise ConfigError("loud must be true or false")
    return Config(greeting=greeting.strip(), loud=loud)
