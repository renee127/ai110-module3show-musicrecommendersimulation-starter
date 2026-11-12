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
    reasons = [
        f"Genre {'matches' if genre_match else 'does not match'} "
        f"{user_prefs['favorite_genre']} (+{genre_points:.1f}/{genre_weight:.0f})",
        f"Mood {'matches' if mood_match else 'does not match'} "
        f"{user_prefs['favorite_mood']} (+{mood_points:.1f}/1)",
        f"Energy is {abs(song_energy - target_energy):.2f} "
        f"from your target (+{energy_points:.2f}/{energy_weight:.0f})",
    ]
    return genre_points + mood_points + energy_points, reasons

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
