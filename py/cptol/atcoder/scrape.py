from __future__ import annotations

import dataclasses
import typing

import bs4
from cptol.scrape import parse_html


def _strip_unit(measured_value: str) -> int:
    # strip unit like "ms" or "kB"
    return int(measured_value.split()[0])


def _scrape_options(
    html: str,
    id: str,
) -> list[str] | None:
    soup = parse_html(html)
    section = soup.find("select", id)
    if section is None:
        return None
    return list(
        map(
            typing.cast(
                typing.Callable[[bs4.element.Tag], str],
                lambda elm: elm.get("value"),
            ),
            section.find_all("option")[1:],
        )
    )


def _csrf_in_form(form: bs4.element.Tag) -> str | None:
    section = form.find(attrs={"name": "csrf_token"})
    if section is None:
        return None
    return typing.cast(
        str,
        section.get("value"),
    )


@dataclasses.dataclass
class Pagination:
    cur: int
    last: int
