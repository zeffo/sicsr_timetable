import asyncio
import tomllib
import re
import sys
import pathlib
from pydantic import BaseModel
from datetime import datetime, timedelta
from aiohttp import ClientSession
from tabulate import tabulate

from .core import fetch, Entry


class Type(BaseModel):
    name: str  # name of the type
    rules: list[str]  # regex rules to apply to the type


class Config(BaseModel):
    types: dict[str, Type]
    format: str = "heavy_grid"


conf_path = pathlib.Path("config.toml")
if not conf_path.exists():
    print("Please create a config.toml file!")
    sys.exit(0)

with conf_path.open("rb") as f:
    conf = tomllib.load(f)
    config = Config(**conf)


start = datetime.now()
end = start + timedelta(days=6)


async def get_reports():
    async with ClientSession() as session:
        report = list(await fetch(start, end, session=session))
        types = config.types.values()
        days: list[list[Entry]] = [
            [] for _ in range(7)
        ]  # 7 buckets for each day of the week
        tags = (
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        )
        for entry in report:
            for t in types:
                if re.search(t.name, entry.type):
                    if t.rules and not any(
                        [re.search(rgx, entry.full_desc) for rgx in t.rules]
                    ):
                        continue
                    days[(entry.start.weekday()) % 7].append(entry)
        for title, items in zip(tags, days):
            print("# ", title)
            entries = [item.dump() for item in items]
            print(tabulate(entries, tablefmt=config.format, headers="keys"))
            print("\n\n")


async def main():
    await get_reports()


if __name__ == "__main__":
    asyncio.run(get_reports())
