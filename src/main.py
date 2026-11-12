"""
Command line runner for the Music Recommender Simulation.

This file stress-tests the recommender with several taste profiles.
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    profiles = [
        (
            "High-Energy Pop",
            {
                "favorite_genre": "pop",
                "favorite_mood": "intense",
                "target_energy": 0.93,
            },
        ),
        (
            "Chill Lofi",
            {
                "favorite_genre": "lofi",
                "favorite_mood": "chill",
                "target_energy": 0.4,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.91,
            },
        ),
        (
            "Conflicting: Metal / Melancholic / High Energy",
            {
                "favorite_genre": "metal",
                "favorite_mood": "melancholic",
                "target_energy": 0.96,
            },
        ),
        (
            "Out-of-Range Energy Target",
            {
                "favorite_genre": "country",
                "favorite_mood": "serene",
                "target_energy": 2.0,
            },
        ),
        (
            "Case-Insensitive Labels / Exact Energy",
            {
                "favorite_genre": "LoFi",
                "favorite_mood": "CHILL",
                "target_energy": 0.40,
            },
        ),
    ]

    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(
            f"\nTop recommendations for {profile_name} "
            f"({user_prefs['favorite_genre']} / {user_prefs['favorite_mood']}, "
            f"target energy: {user_prefs['target_energy']:.2f}):\n"
        )
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} - Score: {score:.2f}/4")
            print(f"   Reasons: {explanation}\n")

    experiment_profile_name, experiment_profile = profiles[0]
    experiment_recommendations = recommend_songs(
        experiment_profile,
        songs,
        k=5,
        weight_shift=True,
    )
    print(
        f"\nWeight-shift experiment for {experiment_profile_name} "
        "(genre 2 -> 1, energy 1 -> 2, mood stays 1):\n"
    )
    for rank, (song, score, explanation) in enumerate(
        experiment_recommendations,
        start=1,
    ):
        print(f"{rank}. {song['title']} - Score: {score:.2f}/4")
        print(f"   Reasons: {explanation}\n")


if __name__ == "__main__":
    main()
