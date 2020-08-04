import pytest
import responses
import requests

from blaseball import __version__, _api_route, Blaseball


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_version():
    assert __version__ == "0.1.0"


def test_login(mocked_responses):
    mocked_responses.add(responses.POST, _api_route("auth/local"), status=302)
    Blaseball("foo", "bar")


def test_user(mocked_responses):
    mocked_responses.add(responses.POST, _api_route("auth/local"), status=302)
    mocked_responses.add(
        responses.GET,
        _api_route("api/getUser"),
        status=200,
        json={
            "_id": "some-uuid",
            "email": "foo@bar.com",
            "coins": 42,
            "votes": 99,
            "peanuts": 420,
            "squirrels": 69,
            "favoriteTeam": "some-other-uuid",
        },
    )

    u = Blaseball("foo", "bar").user()
    assert u.email == "foo@bar.com"
    assert u.coins == 42
    assert u.votes == 99
    assert u.peanuts == 420
    assert u.squirrels == 69
