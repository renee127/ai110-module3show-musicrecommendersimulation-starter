"""
Command line runner for the Music Recommender Simulation.

This file stress-tests the recommender with several taste profiles.
"""

from textwrap import wrap

from src.recommender import load_songs, recommend_songs


def print_recommendation_table(
    recommendations: list[tuple[dict, float, str]],
    max_score: int = 4,
) -> None:
    """Print ranked songs, scores, and wrapped scoring reasons in an ASCII table."""
    widths = (4, 20, 8, 54)
    headers = ("Rank", "Song", "Score", "Reasons")

    def border() -> str:
        return "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def row(cells: tuple[str, ...]) -> str:
        return "| " + " | ".join(
            cell.ljust(width) for cell, width in zip(cells, widths)
        ) + " |"

    print(border())
    print(row(headers))
    print(border())
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reason_lines = wrap(explanation, width=widths[3]) or [""]
        for line_index, reason_line in enumerate(reason_lines):
            print(
                row(
                    (
                        str(rank) if line_index == 0 else "",
                        song["title"] if line_index == 0 else "",
                        f"{score:.2f}/{max_score}" if line_index == 0 else "",
                        reason_line,
                    )
                )
            )
        print(border())


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
        try:
            recommendations = recommend_songs(user_prefs, songs, k=5)
        except ValueError as error:
            print(f"\nRejected profile {profile_name}: {error}")
            continue

        print(
            f"\nTop recommendations for {profile_name} "
            f"({user_prefs['favorite_genre']} / {user_prefs['favorite_mood']}, "
            f"target energy: {user_prefs['target_energy']:.2f}):\n"
        )
        print_recommendation_table(recommendations)

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
    print_recommendation_table(experiment_recommendations, max_score=5)


if __name__ == "__main__":
    main()
