import argparse
from datetime import datetime
from aiohttp import ClientSession
from yarl import URL


parser = argparse.ArgumentParser(
    prog="SICSR TimeTable Generator",
    description="Generate your SICSR Timetable from your terminal!",
    epilog="Please submit bug reports on GitHub: https://github.com/zeffo/sicsr_timetable",
)


def dt_conv(raw: str) -> datetime:
    return datetime.strptime(raw, "%d-%m-%Y")


parser.add_argument(
    "-s",
    "--start",
    type=dt_conv,
    default=datetime.now(),
    help="Report Start Date (dd-mm-yyyy), defaults to the current date.",
)
parser.add_argument(
    "-e",
    "--end",
    type=dt_conv,
    default=datetime.now(),
    help="Report End Date (dd-mm-yyyy), defaults to the current date.",
)
parser.add_argument(
    "--match-area",
    default="",
    help="Include entries which match this area",
    dest="areamatch",
)
parser.add_argument(
    "--match-room",
    default="",
    help="Include entries which match this room",
    dest="roommatch",
)
parser.add_argument(
    "--match-type",
    default="",
    nargs="*",
    help="Include entries which match this type. The type(s) should exactly as given in the timetable, eg: BCA (IV) - Div. A)",
    dest="typematch",
)
parser.add_argument(
    "--match-brief-desc",
    default="",
    help="Include entries which match this Brief Description.",
    dest="namematch",
)
parser.add_argument(
    "--match-desc",
    "--match-full-desc",
    default="",
    help="Include entries which match this Full Description.",
    dest="descrmatch",
)
parser.add_argument(
    "--match-creator",
    default="",
    help="Include entries created by this entity.",
    dest="creatormatch",
)
parser.add_argument(
    "--confirmation-status", type=int, default=2, dest="matchconfirmed"
)  # 2 includes both confirmed and tentative entries
parser.add_argument(
    "--division",
    default="",
    help="Include entries which match this division (or entries which do not mention a division)",
)
