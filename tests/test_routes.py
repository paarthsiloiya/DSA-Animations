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

ROUTE_ALIASES = [
    "/data-structures",
    "/2d-arrays",
    "/searching-algorithms",
    "/linear-search",
    "/binary-search",
    "/sorting-algorithms",
    "/bubble-sort",
    "/insertion-sort",
    "/selection-sort",
    "/quick-sort",
    "/merge-sort",
    "/heap-sort",
    "/stack-and-queue",
    "/linked-list",
    "/singly-linked-list",
    "/doubly-linked-list",
]

ROUTE_PAIRS = list(zip(
    [
        "/data structures",
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
        "/linked list",
        "/singly linked list",
        "/doubly linked list",
    ],
    ROUTE_ALIASES,
))


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


@pytest.mark.parametrize("route", ROUTE_ALIASES)
def test_alias_route_renders(client, route):
    response = client.get(route)
    assert response.status_code == 200, f"{route!r} returned {response.status_code}"


@pytest.mark.parametrize("old_route, new_route", ROUTE_PAIRS)
def test_alias_renders_same_page(client, old_route, new_route):
    old_response = client.get(quote(old_route))
    new_response = client.get(new_route)
    assert old_response.status_code == new_response.status_code == 200
    assert old_response.data == new_response.data


def test_logout_redirects_anonymous(client):
    response = client.get(quote("/logout"))
    assert response.status_code == 302
