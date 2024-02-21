"""Main script to run everything from."""

import numpy as np

from src.playing import play_multiple_decks
from src.visualization.plotting import plot_score_vs_ceartainty, plot_score_vs_dealer


def main(
    n_players: int = 4,
    n_decks: int = 8,
    n_games: int = 100,
    use_split: bool = True,
    games_pr_deck: int = 40,
    ceartainty: float = 0.85,
) -> None:
    """Runthe main blackjack loop.

    Args:
        n_players (int, optional): Number of players. Defaults to 4.
        n_decks (int, optional): Number of decks. Defaults to 8.
        n_games (int, optional): Total number of games. Defaults to 100.
        use_split (bool, optional): Should split be used. Defaults to True.
        games_pr_deck (int, optional): Number of games for each deck. Defaults to 40.
        ceartainty (float, optional): When should a card be drawn. Defaults to 0.85.
    """
    all_game_scores, all_dealer_hands = play_multiple_decks(
        n_players, n_decks, n_games, use_split, games_pr_deck, ceartainty
    )

    plot_score_vs_dealer(all_game_scores, all_dealer_hands, use_split)

    ceartainty_results = []

    for ceartainty in np.arange(0, 1.05, 0.05):
        # Call play_multiple_decks with current ceartainty value
        all_game_scores, all_dealer_hands = play_multiple_decks(
            n_players, n_decks, n_games, use_split, games_pr_deck, ceartainty
        )

        # Append results to all_results
        ceartainty_results.append(
            (ceartainty, sum(all_game_scores) / n_games)  # type: ignore
        )

    plot_score_vs_ceartainty(ceartainty_results)  # type: ignore


if __name__ == "__main__":
    main()
