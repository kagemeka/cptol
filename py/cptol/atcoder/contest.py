from __future__ import annotations

import asyncio
import dataclasses
import datetime
import enum
import logging
import typing

import aiohttp
from cptol.scrape import parse_html
import bs4

from cptol.atcoder import SITE_URL
import cptol.atcoder.scrape

_LOGGER = logging.getLogger(__name__)

CONTESTS_URL = f"{SITE_URL}/contests"
CONTESTS_ARCHIVE_URL = f"{CONTESTS_URL}/archive"
LANGUAGE = "ja"


class AlgoType(enum.Enum):
    DEFINITE = enum.auto()
    HEURISTIC = enum.auto()


class Color(enum.Enum):
    GREEN = enum.auto()
    BLUE = enum.auto()
    ORANGE = enum.auto()
    RED = enum.auto()


COLOR_FROM_STR = {
    "user-green": Color.GREEN,
    "user-blue": Color.BLUE,
    "user-orange": Color.ORANGE,
    "user-red": Color.RED,
}


def color_from_string(color: str) -> Color | None:
    return COLOR_FROM_STR.get(color)


class Status(enum.Enum):
    RUNNING = enum.auto()
    PERMANENT = enum.auto()
    UPCOMING = enum.auto()
    FINISHED = enum.auto()


@dataclasses.dataclass(frozen=False)
class Contest:
    id: str
    title: str
    status: Status | None = None
    color: Color | None = None
    start_datetime: datetime.datetime | None = None
    duration: datetime.timedelta | None = None


async def _get_contest_page(
    session: aiohttp.ClientSession,
    contest_id: str,
) -> aiohttp.ClientResponse:
    url = f"{CONTESTS_URL}/{contest_id}"
    _LOGGER.info(f"get {url}")
    return await session.get(url)


def scrape_contest(html: str) -> Contest:
    soup = parse_html(html)
    section = soup.find(class_="contest-title")
    return Contest(
        id=section.get("href").split("/")[-1],
        title=section.text,
    )


async def _get_contests_page(
    session: aiohttp.ClientSession,
) -> aiohttp.ClientResponse:
    _LOGGER.info(f"get {CONTESTS_URL}")
    return await session.get(
        CONTESTS_URL,
        params={"lang": LANGUAGE},
    )


def _parse_duration(duration: str) -> datetime.timedelta:
    hours, minutes = map(int, duration.split(":"))
    return datetime.timedelta(hours=hours, minutes=minutes)


def _scrape_row(row: bs4.element.Tag) -> Contest:
    infos = row.find_all("td")
    color_texts = infos[1].span.get("class")
    color = None if not color_texts else color_from_string(color_texts[0])
    return Contest(
        id=infos[1].a.get("href").split("/")[-1],
        title=infos[1].a.text.strip(),
        color=color,
        start_datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        duration=_parse_duration(infos[2].text),
    )


def _scrape_running_contests(html: str) -> list[Contest] | None:
    soup = parse_html(html)
    section = soup.find(id="contest-table-action")
    if section is None:
        return None
    contests = []
    for row in section.table.tbody.find_all("tr"):
        contest = _scrape_row(row)
        contest.status = Status.RUNNING
        contests.append(contest)
    return contests


def _scrape_permanent_contests(html: str) -> list[Contest] | None:
    def scrape_row(row: bs4.element.Tag) -> Contest:
        infos = row.find_all("td")
        color_texts = infos[0].span.get("class")
        color = None if not color_texts else color_from_string(color_texts[0])
        return Contest(
            id=infos[0].a.get("href").split("/")[-1],
            title=infos[0].a.text.strip(),
            status=Status.PERMANENT,
            color=color,
        )

    soup = parse_html(html)
    section = soup.find(id="contest-table-permanent")
    if section is None:
        return None
    return [scrape_row(row) for row in section.table.tbody.find_all("tr")]


def _scrape_upcoming_contests(html: str) -> list[Contest] | None:
    soup = parse_html(html)
    section = soup.find(id="contest-table-upcoming")
    if section is None:
        return None
    contests = []
    for row in section.table.tbody.find_all("tr"):
        contest = _scrape_row(row)
        contest.status = Status.UPCOMING
        contests.append(contest)
    return contests


# def _scrape_pagination(html: str) -> atcoder.scrape.Pagination:
#     soup = parse_html(html)
#     pagination = soup.find(class_="pagination")
#     current = int(pagination.find(class_="active").text)
#     last = int(pagination.find_all("li")[-1].text)
#     return atcoder.scrape.Pagination(current, last)


async def finished(
    session: aiohttp.ClientSession,
    page: int,
) -> list[Contest] | None:
    _LOGGER.info(f"get {CONTESTS_ARCHIVE_URL}, page: {page}")
    r = await session.get(
        url=CONTESTS_ARCHIVE_URL,
        params={
            "page": page,
            "lang": LANGUAGE,
        },
    )
    soup = parse_html(await r.text())
    if soup.table is None:
        return None
    contests = []
    for row in soup.table.tbody.find_all("tr"):
        c = _scrape_row(row)
        c.status = Status.FINISHED
        contests.append(c)
    return contests


async def fetch_all_contests(
    session: aiohttp.ClientSession,
) -> typing.AsyncIterator[Contest]:
    get = asyncio.create_task(_get_contests_page(session))
    html = await (await get).text()
    contests = _scrape_upcoming_contests(html)
    if contests is not None:
        for contest in contests:
            yield contest
    contests = _scrape_running_contests(html)
    if contests is not None:
        for contest in contests:
            yield contest
    contests = _scrape_permanent_contests(html)
    if contests is not None:
        for contest in contests:
            yield contest

    page = 1
    while True:
        contests = await finished(session, page)
        if contests is None:
            return
        for contest in contests:
            yield contest
        page += 1


# async def fetch_contest_details() -> None:
#     ...


# async def register() -> None:
#     ...
