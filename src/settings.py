import tomllib
from typing import TypedDict


class Paths(TypedDict):
    source: str
    output: str


class Watermark(TypedDict):
    path: str
    transparency_percent: int


class Settings(TypedDict):
    paths: Paths
    watermark: Watermark


with open("settings.toml", mode="rb") as fp:
    settings: Settings = tomllib.load(fp)
