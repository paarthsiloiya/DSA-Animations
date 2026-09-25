"""The link checker must report no broken links beyond the recorded baseline."""

from tools.link_check import run


def test_no_new_broken_links():
    _, new, _ = run()
    assert new == [], f"{len(new)} new broken links:\n" + "\n".join(new)
