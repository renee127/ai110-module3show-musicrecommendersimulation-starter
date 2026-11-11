import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and explain each contribution."""
    genre_match = (
        song["genre"].casefold() == user_prefs["favorite_genre"].casefold()
    )
    mood_match = song["mood"].casefold() == user_prefs["favorite_mood"].casefold()
    energy_similarity = max(
        0.0, 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    )

    genre_points = 2.0 if genre_match else 0.0
    mood_points = 1.0 if mood_match else 0.0
    energy_points = energy_similarity
    reasons = [
        f"Genre {'matches' if genre_match else 'does not match'} "
        f"{user_prefs['favorite_genre']} (+{genre_points:.1f}/2)",
        f"Mood {'matches' if mood_match else 'does not match'} "
        f"{user_prefs['favorite_mood']} (+{mood_points:.1f}/1)",
        f"Energy is {abs(song['energy'] - user_prefs['target_energy']):.2f} "
        f"from your target (+{energy_points:.2f}/1)",
    ]
    return genre_points + mood_points + energy_points, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs ranked by score with explanations."""
    if k < 0:
        raise ValueError("k must be non-negative")

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, "; ".join(reasons)))
    return sorted(
        scored_songs,
        key=lambda recommendation: recommendation[1],
        reverse=True,
    )[:k]
