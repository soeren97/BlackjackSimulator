"""All ploting functions."""

import matplotlib.pyplot as plt
import numpy as np

from src.lookups import plotting_map
from src.util import format_data


def plot_score_vs_dealer(
    scores: list[np.ndarray],
    dealer_hands: list[list[int]],
    use_split: bool,
) -> None:
    """Plot the score of players vs the final value of the dealers hand.

    Args:
        scores (list): Scores of all players.
        dealer_hands (list): The hands of the dealers.
        use_split (bool): Was split used.
    """
    n_players, df = format_data(scores, dealer_hands)

    grouped_df = df.groupby("Dealer Hand").sum().reset_index()

    grouped_df.loc[0, "Dealer Hand"] = 16  # Eliminate dead space

    plt.figure(figsize=(10, 6))

    width = 0.15
    multiplier = (1 - n_players) / 2

    for player in grouped_df.columns[1:]:
        offset = width * multiplier
        plt.bar(
            grouped_df["Dealer Hand"] + offset, grouped_df[player], width, label=player
        )
        multiplier += 1

    plt.axhline(0, color="black", linewidth=0.5)

    plt.xticks(list(plotting_map.keys()), list(plotting_map.values()))
    plt.legend()
    plt.xlabel("Dealer score")
    plt.ylabel("Payout")
    plt.tight_layout()

    if use_split:
        path = "dealer_correlation_split"
    else:
        path = "dealer_correlation_no_split"

    plt.savefig(f"Figures/{path}.png")


def plot_score_vs_ceartainty(
    ceartainty_scores: list[list[tuple[np.float64, np.ndarray]]]
) -> None:
    """Plot the scores of players as a function of ceartainty.

    Args:
        ceartainty_scores (list): Ceartainty and scores of players.
    """
    n_players = len(ceartainty_scores[0][1])
    certainties = [entry[0] for entry in ceartainty_scores]
    scores = [entry[1] for entry in ceartainty_scores]
    scores_by_player = [[row[i] for row in scores] for i in range(n_players)]

    plt.figure(figsize=(10, 6))

    for i, scores in enumerate(scores_by_player):
        plt.plot(certainties, scores, label=f"Player {i + 1}")

    plt.axhline(0, color="black", linewidth=0.5)

    plt.legend()
    plt.xlabel("Unceartainty")
    plt.ylabel("Average payout")
    plt.savefig("Figures/Ceartainty.png")


if __name__ == "__main__":
    pass
