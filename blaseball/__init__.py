import requests
import backoff
import logging
import sys
from typing import MutableMapping, List

__version__ = "0.1.0"

_BLASEBALL_BASE_URL = "https://blaseball.com/"
_log = logging.getLogger("blaseball")

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class Entity:
    id: str
    _session: requests.Session

    def __init__(self, session: requests.Session, _id: str) -> None:
        self._session = session
        self.id = _id


class User(Entity):
    email: str
    coins: int
    votes: int
    peanuts: int
    squirrels: int

    _favorite_team_id: str

    def __init__(
        self,
        session: requests.Session,
        _id: str,
        email: str,
        coins: int,
        votes: int,
        peanuts: int,
        squirrels: int,
        favoriteTeam: str,
        **kwargs,
    ) -> None:
        super().__init__(session, _id)
        self.email = email
        self.coins = coins
        self.votes = votes
        self.peanuts = peanuts
        self.squirrels = squirrels
        self._favorite_team_id = favoriteTeam

    def favorite_team(self) -> "Team":
        return Team(self._session, **_get_team(self._session, self._favorite_team_id))


class Player(Entity):
    anticapitalism: float
    base_thirst: float
    buoyancy: float
    chasiness: float
    coldness: float
    continuation: float
    divinity: float
    ground_friction: float
    indulgence: float
    laserlikeness: float
    martyrdom: float
    moxie: float
    musclitude: float
    name: str
    bat: str
    omniscience: float
    overpowerment: float
    patheticism: float
    ruthlessness: float
    shakespearianism: float
    suppression: float
    tenaciousness: float
    thwackability: float
    tragicness: float
    unthwackability: float
    watchfulness: float
    pressurization: float
    total_fingers: int
    soul: int
    deceased: bool
    peanut_allergy: bool
    cinnamon: float
    fate: int

    def __init__(
        self,
        session: requests.Session,
        _id: str,
        anticapitalism: float,
        baseThirst: float,
        buoyancy: float,
        chasiness: float,
        coldness: float,
        continuation: float,
        divinity: float,
        groundFriction: float,
        indulgence: float,
        laserlikeness: float,
        martyrdom: float,
        moxie: float,
        musclitude: float,
        name: str,
        bat: str,
        omniscience: float,
        overpowerment: float,
        patheticism: float,
        ruthlessness: float,
        shakespearianism: float,
        suppression: float,
        tenaciousness: float,
        thwackability: float,
        tragicness: float,
        unthwackability: float,
        watchfulness: float,
        pressurization: float,
        totalFingers: int,
        soul: int,
        deceased: bool,
        peanutAllergy: bool,
        cinnamon: float,
        fate: int,
        **kwargs,
    ) -> None:
        super().__init__(session, _id)
        self.anticapitalism = anticapitalism
        self.base_thirst = baseThirst
        self.buoyancy = buoyancy
        self.chasiness = chasiness
        self.coldness = coldness
        self.continuation = continuation
        self.divinity = divinity
        self.ground_friction = groundFriction
        self.indulgence = indulgence
        self.laserlikeness = laserlikeness
        self.martyrdom = martyrdom
        self.moxie = moxie
        self.musclitude = musclitude
        self.name = name
        self.bat = bat
        self.omniscience = omniscience
        self.overpowerment = overpowerment
        self.patheticism = patheticism
        self.ruthlessness = ruthlessness
        self.shakespearianism = shakespearianism
        self.suppression = suppression
        self.tenaciousness = tenaciousness
        self.thwackability = thwackability
        self.tragicness = tragicness
        self.unthwackability = unthwackability
        self.watchfulness = watchfulness
        self.pressurization = pressurization
        self.total_fingers = totalFingers
        self.soul = soul
        self.deceased = deceased
        self.peanut_allergy = peanutAllergy
        self.cinnamon = cinnamon
        self.fate = fate

    def __str__(self) -> str:
        return f'Player(name="{self.name}")'

    def __repr__(self) -> str:
        return f'Player(name="{self.name}")'


class Team(Entity):
    full_name: str
    location: str
    nickname: str
    emoji: str
    season_shames: int
    season_shamings: int
    shame_runs: int
    total_shames: int
    total_shamings: int
    slogan: str
    championships: int

    _lineup_ids: List[str]
    _rotation_ids: List[str]
    _bullpen_ids: List[str]
    _bench_ids: List[str]

    def __init__(
        self,
        session: requests.Session,
        _id: str,
        fullName: str,
        nickname: str,
        location: str,
        emoji: str,
        seasonShames: int,
        seasonShamings: int,
        shameRuns: int,
        totalShames: int,
        totalShamings: int,
        slogan: str,
        championships: int,
        lineup: List[str],
        rotation: List[str],
        bullpen: List[str],
        bench: List[str],
        **kwargs,
    ) -> None:
        super().__init__(session, _id)
        self.full_name = fullName
        self.location = location
        self.nickname = nickname
        self.emoji = emoji
        self.season_shames = seasonShames
        self.season_shamings = seasonShamings
        self.shame_runs = shameRuns
        self.total_shames = totalShames
        self.total_shamings = totalShamings
        self.slogan = slogan
        self.championships = championships
        self._lineup_ids = lineup
        self._rotation_ids = rotation
        self._bullpen_ids = bullpen
        self._bench_ids = bench

    def lineup(self) -> List[Player]:
        return [
            Player(self._session, **p)
            for p in _get_players(self._session, self._lineup_ids)
        ]

    def rotation(self) -> List[Player]:
        return [
            Player(self._session, **p)
            for p in _get_players(self._session, self._rotation_ids)
        ]

    def bullpen(self) -> List[Player]:
        return [
            Player(self._session, **p)
            for p in _get_players(self._session, self._bullpen_ids)
        ]

    def bench(self) -> List[Player]:
        return [
            Player(self._session, **p)
            for p in _get_players(self._session, self._bench_ids)
        ]

    def __str__(self) -> str:
        return f'Team(name="{self.full_name}")'

    def __repr__(self) -> str:
        return f'Team(name="{self.full_name}")'


class Blaseball:
    _session: requests.Session
    _entity_map: MutableMapping

    def __init__(self, username: str, password: str) -> None:
        self._session = requests.Session()
        self._entity_map = {}
        _login(self._session, username, password)

    def user(self) -> User:
        return User(self._session, **_get_user(self._session))

    def teams(self) -> List[Team]:
        return [Team(self._session, **t) for t in _get_all_teams(self._session)]


def _api_route(path: str) -> str:
    return _BLASEBALL_BASE_URL + path


@backoff.on_exception(backoff.expo, requests.HTTPError, logger="blaseball", max_tries=5)
def _login(session: requests.Session, username: str, password: str) -> None:
    url = _api_route("auth/local")
    resp = session.post(
        url, json={"username": username, "password": password, "isLogin": True,}
    )
    resp.raise_for_status()


@backoff.on_exception(backoff.expo, requests.HTTPError, logger="blaseball", max_tries=5)
def _get_user(session: requests.Session) -> dict:
    url = _api_route("api/getUser")
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json()


@backoff.on_exception(backoff.expo, requests.HTTPError, logger="blaseball", max_tries=5)
def _get_players(session: requests.Session, players: List[str]) -> list:
    url = _api_route("database/players")
    ids = ",".join(players)
    resp = session.get(url, params={"ids": ids,})
    resp.raise_for_status()
    return resp.json()


@backoff.on_exception(backoff.expo, requests.HTTPError, logger="blaseball", max_tries=5)
def _get_all_teams(session: requests.Session) -> list:
    url = _api_route("database/allTeams")
    resp = session.get(url)
    resp.raise_for_status()
    return resp.json()


@backoff.on_exception(backoff.expo, requests.HTTPError, logger="blaseball", max_tries=5)
def _get_team(session: requests.Session, id: str) -> dict:
    url = _api_route("database/team")
    resp = session.get(url, params={"id": id})
    resp.raise_for_status()
    return resp.json()
