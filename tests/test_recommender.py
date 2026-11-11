from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)


def test_load_songs_converts_csv_values_to_numbers(tmp_path):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,Test Song,Test Artist,pop,happy,0.8,120,0.9,0.7,0.2\n",
        encoding="utf-8",
    )

    songs = load_songs(str(csv_path))

    assert len(songs) == 1
    assert songs[0]["id"] == 1
    assert isinstance(songs[0]["tempo_bpm"], float)
    for feature in ("energy", "valence", "danceability", "acousticness"):
        assert isinstance(songs[0][feature], float)


def test_score_song_uses_genre_mood_and_energy_weights():
    profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    genre_only = {
        "genre": "pop",
        "mood": "intense",
        "energy": 0.8,
    }
    mood_only = {
        "genre": "rock",
        "mood": "happy",
        "energy": 0.8,
    }

    genre_score, _ = score_song(profile, genre_only)
    mood_score, _ = score_song(profile, mood_only)
    both_score, reasons = score_song(
        profile,
        {"genre": "pop", "mood": "happy", "energy": 0.8},
    )

    assert genre_score == 3.0
    assert mood_score == 2.0
    assert both_score == 4.0
    assert any("Genre matches" in reason for reason in reasons)
    assert any("Mood matches" in reason for reason in reasons)


def test_recommend_songs_ranks_using_genre_and_mood_scores():
    profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }
    songs = [
        {"title": "Mood match", "genre": "rock", "mood": "happy", "energy": 0.8},
        {"title": "Both match", "genre": "pop", "mood": "happy", "energy": 0.8},
    ]

    recommendations = recommend_songs(profile, songs, k=1)

    assert len(recommendations) == 1
    assert recommendations[0][0]["title"] == "Both match"
    assert recommendations[0][1] == 4.0


def test_energy_similarity_decreases_with_distance_from_target():
    profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    exact_energy_score, _ = score_song(
        profile,
        {"genre": "other", "mood": "other", "energy": 0.8},
    )
    distant_energy_score, _ = score_song(
        profile,
        {"genre": "other", "mood": "other", "energy": 0.4},
    )

    assert exact_energy_score == 1.0
    assert distant_energy_score == 0.6

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
