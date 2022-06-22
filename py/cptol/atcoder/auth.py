from __future__ import annotations

import dataclasses
import http
import logging

import requests

from cptol.option import unwrap
from cptol.atcoder import SITE_URL
from cptol.result import Result, Err
from cptol.scrape import parse_html

LOGIN_URL = f"{SITE_URL}/login"
_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class Cred:
    username: str
    password: str


def input_cred() -> Cred:
    import getpass

    return Cred(
        username=input("username: "),
        password=getpass.getpass("password: "),
    )


def is_logged_in(sess: requests.Session) -> bool:
    from cptol.atcoder.contest import _CONTESTS_URL

    return (
        sess.get(
            url=f"{_CONTESTS_URL}/abc001/submit",
            allow_redirects=False,
        ).status_code
        == 200
    )


def login(cred: Cred) -> Result[requests.Session, str]:
    def scrape_csrf(html: str) -> str:
        from cptol.atcoder.scrape import _csrf_in_form

        return unwrap(_csrf_in_form(parse_html(html).find_all("form")[1]))

    sess = requests.session()
    resp = sess.post(
        LOGIN_URL,
        {
            **dataclasses.asdict(cred),
            "csrf_token": scrape_csrf(sess.get(LOGIN_URL).text),
        },
    )
    if not is_logged_in(sess):
        return Err(
            "Cannot login to atcoder.jp, please check your credentials.",
        )
    _LOGGER.info(
        f"login to atcoder: {http.client.responses.get(resp.status_code)}"
    )
    return sess
