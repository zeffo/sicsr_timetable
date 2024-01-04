from datetime import datetime
from sicsr_timetable.core import fetch, Entry
from tabulate import tabulate
import asyncio
from aiohttp import ClientSession
import re

types = {
    "BCA (IV) - Div. A": [],
    "BCA (IV) - Elective - Group I": ["Creative Writing"],
    "BCA (IV) - Elective - Group II - GroupA": [r"Div\.? ?A"],
}  # types and their corresponding regex rules


async def test():
    async with ClientSession() as s:
        report = list(
            await fetch(datetime(2024, 1, 1), datetime(2024, 1, 7), session=s)
        )
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
            if entry.type in types:
                if types[entry.type] and not any(
                    [re.search(rgx, entry.full_desc) for rgx in types[entry.type]]
                ):
                    continue
                days[entry.start.day - 1 % 7].append(entry)
        for title, items in zip(tags, days):
            print("# ", title)
            entries = [item.dump() for item in items]
            print(tabulate(entries, tablefmt="github", headers="keys"))
            print("\n\n")


asyncio.run(test())
