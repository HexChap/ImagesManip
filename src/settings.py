import tomllib
from pathlib import Path
from typing import TypedDict

settings_path = Path(__file__).parent.parent / "settings.toml"


class Paths(TypedDict):
    source: str
    output: str


class Watermark(TypedDict):
    path: str
    transparency_percent: int


class Settings(TypedDict):
    paths: Paths
    watermark: Watermark


def load_settings() -> Settings:
    with open(settings_path, mode="rb") as fp:
        return tomllib.load(fp)


settings = load_settings()
