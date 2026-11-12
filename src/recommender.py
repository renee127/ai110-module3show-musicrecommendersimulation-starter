import csv
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import asdict, dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: int = 2020
    mood_tags: str = ""
    language: str = "English"
    instrumentalness: float = 0.5

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_popularity: Optional[float] = None
    preferred_release_decade: Optional[int] = None
    preferred_mood_tags: Optional[List[str]] = None
    preferred_language: Optional[str] = None
    target_instrumentalness: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return songs ranked with the functional scorer's default weights."""
        if k < 0:
            raise ValueError("k must be non-negative")

        user_prefs = asdict(user)
        _validate_energy(user_prefs["target_energy"], "target_energy")
        scored_songs = [
            (song, score_song(user_prefs, asdict(song))[0])
            for song in self.songs
        ]
        return [
            song
            for song, _ in sorted(
                scored_songs,
                key=lambda recommendation: recommendation[1],
                reverse=True,
            )[:k]
        ]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain a song's score using the functional scorer's default weights."""
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert their numeric fields."""
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        songs = []
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for feature in ("energy", "valence", "danceability", "acousticness"):
                row[feature] = float(row[feature])
            row["popularity"] = int(row["popularity"])
            row["release_decade"] = int(row["release_decade"])
            row["instrumentalness"] = float(row["instrumentalness"])
            songs.append(row)
    return songs


def _validate_energy(value: object, name: str) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not 0.0 <= value <= 1.0
        or not math.isfinite(value)
    ):
        raise ValueError(
            f"{name} must be a finite number between 0.0 and 1.0; "
            f"got {value!r}"
        )


def _validate_range(value: object, name: str, minimum: float, maximum: float) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or not minimum <= value <= maximum
    ):
        raise ValueError(
            f"{name} must be a finite number between {minimum:g} and {maximum:g}; "
            f"got {value!r}"
        )


def _validate_decade(value: object, name: str) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value % 10 != 0
        or not 1900 <= value <= 2100
    ):
        raise ValueError(
            f"{name} must be a decade from 1900 to 2100; got {value!r}"
        )


def _normalize_tags(value: object, name: str) -> set[str]:
    if isinstance(value, str):
        tags = value.split("|")
    elif isinstance(value, (list, tuple, set)):
        tags = value
    else:
        raise ValueError(f"{name} must be a pipe-separated string or list of tags")

    if any(not isinstance(tag, str) for tag in tags):
        raise ValueError(f"{name} must contain only strings")
    normalized = {tag.strip().casefold() for tag in tags if tag.strip()}
    if not normalized:
        raise ValueError(f"{name} must contain at least one non-empty tag")
    return normalized


def score_song(
    user_prefs: Dict,
    song: Dict,
    weight_shift: bool = False,
) -> Tuple[float, List[str]]:
    """Score a song against user preferences and explain each contribution."""
    song_energy = song["energy"]
    target_energy = user_prefs["target_energy"]
    _validate_energy(song_energy, "song energy")
    _validate_energy(target_energy, "target_energy")

    genre_match = (
        song["genre"].strip().casefold()
        == user_prefs["favorite_genre"].strip().casefold()
    )
    mood_match = (
        song["mood"].strip().casefold()
        == user_prefs["favorite_mood"].strip().casefold()
    )
    energy_similarity = max(
        0.0, 1.0 - abs(song_energy - target_energy)
    )

    genre_weight = 1.0 if weight_shift else 2.0
    energy_weight = 2.0 if weight_shift else 1.0
    genre_points = genre_weight if genre_match else 0.0
    mood_points = 1.0 if mood_match else 0.0
    energy_points = energy_weight * energy_similarity
    score = genre_points + mood_points + energy_points
    reasons = [
        f"Genre {'matches' if genre_match else 'does not match'} "
        f"{user_prefs['favorite_genre']} (+{genre_points:.1f}/{genre_weight:.0f})",
        f"Mood {'matches' if mood_match else 'does not match'} "
        f"{user_prefs['favorite_mood']} (+{mood_points:.1f}/1)",
        f"Energy is {abs(song_energy - target_energy):.2f} "
        f"from your target (+{energy_points:.2f}/{energy_weight:.0f})",
    ]

    if user_prefs.get("target_popularity") is not None:
        target_popularity = user_prefs["target_popularity"]
        _validate_range(target_popularity, "target_popularity", 0.0, 100.0)
        _validate_range(song["popularity"], "song popularity", 0.0, 100.0)
        similarity = 1.0 - abs(song["popularity"] - target_popularity) / 100.0
        score += similarity
        reasons.append(f"Popularity similarity (+{similarity:.2f}/1)")

    if user_prefs.get("preferred_release_decade") is not None:
        preferred_decade = user_prefs["preferred_release_decade"]
        _validate_decade(preferred_decade, "preferred_release_decade")
        _validate_decade(song["release_decade"], "song release_decade")
        similarity = max(
            0.0,
            1.0 - abs(song["release_decade"] - preferred_decade) / 50.0,
        )
        score += similarity
        reasons.append(f"Release-decade similarity (+{similarity:.2f}/1)")

    if user_prefs.get("preferred_mood_tags") is not None:
        preferred_tags = _normalize_tags(
            user_prefs["preferred_mood_tags"],
            "preferred_mood_tags",
        )
        song_tags = _normalize_tags(song["mood_tags"], "song mood_tags")
        similarity = len(preferred_tags & song_tags) / len(preferred_tags)
        score += similarity
        reasons.append(f"Mood-tag overlap (+{similarity:.2f}/1)")

    if user_prefs.get("preferred_language") is not None:
        preferred_language = user_prefs["preferred_language"]
        if not isinstance(preferred_language, str) or not preferred_language.strip():
            raise ValueError("preferred_language must be a non-empty string")
        song_language = song["language"]
        if not isinstance(song_language, str) or not song_language.strip():
            raise ValueError("song language must be a non-empty string")
        language_match = (
            song_language.strip().casefold()
            == preferred_language.strip().casefold()
        )
        language_points = 1.0 if language_match else 0.0
        score += language_points
        reasons.append(
            f"Language {'matches' if language_match else 'does not match'} "
            f"{preferred_language} (+{language_points:.1f}/1)"
        )

    if user_prefs.get("target_instrumentalness") is not None:
        target_instrumentalness = user_prefs["target_instrumentalness"]
        _validate_range(
            target_instrumentalness,
            "target_instrumentalness",
            0.0,
            1.0,
        )
        _validate_range(song["instrumentalness"], "song instrumentalness", 0.0, 1.0)
        similarity = 1.0 - abs(song["instrumentalness"] - target_instrumentalness)
        score += similarity
        reasons.append(f"Instrumentalness similarity (+{similarity:.2f}/1)")

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weight_shift: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs ranked by score with explanations."""
    if k < 0:
        raise ValueError("k must be non-negative")
    _validate_energy(user_prefs["target_energy"], "target_energy")

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weight_shift=weight_shift)
        scored_songs.append((song, score, "; ".join(reasons)))
    return sorted(
        scored_songs,
        key=lambda recommendation: recommendation[1],
        reverse=True,
    )[:k]
