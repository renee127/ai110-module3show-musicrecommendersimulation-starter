"""
Command line runner for the Music Recommender Simulation.

This file runs the recommender with an example taste profile.
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(
        "\nTop recommendations for "
        f"{user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} "
        f"(target energy: {user_prefs['target_energy']:.1f}):\n"
    )
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - Score: {score:.2f}/4")
        print(f"   Reasons: {explanation}\n")


if __name__ == "__main__":
    main()
