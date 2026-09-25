"""Smoke test: every current route responds with the expected status."""

import sys
from pathlib import Path
from urllib.parse import quote

import pytest

ROUTES_200 = [
    "/",
    "/dsa",
    "/data structures",
    "/algorithms",
    "/arrays",
    "/2D arrays",
    "/searching algorithms",
    "/linear search",
    "/binary search",
    "/sorting algorithms",
    "/bubble sort",
    "/insertion sort",
    "/selection sort",
    "/quick sort",
    "/merge sort",
    "/heap sort",
    "/stack and queue",
    "/stack",
    "/queue",
    "/linked list",
    "/singly linked list",
    "/doubly linked list",
    "/login",
    "/signup",
]


@pytest.fixture(scope="module")
def client():
    website_dir = Path(__file__).resolve().parents[1] / "Website"
    if str(website_dir) not in sys.path:
        sys.path.insert(0, str(website_dir))
    from website import create_app

    return create_app().test_client()


@pytest.mark.parametrize("route", ROUTES_200)
def test_route_renders(client, route):
    response = client.get(quote(route))
    assert response.status_code == 200, f"{route!r} returned {response.status_code}"


def test_logout_redirects_anonymous(client):
    response = client.get(quote("/logout"))
    assert response.status_code == 302
