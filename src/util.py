"""Utility functions."""

from typing import Any

import numpy as np
import pandas as pd

from src.lookups import blackjack_values


def reverse_lookup(values: list[int]) -> Any:
    """Reverse lookup in a dictionary.

    Requires the dictionary values to be unique.

    Args:
        values (int): List of values to lookup.

    Returns:
        Any: The key that mathes the value.
    """
    return {
        value: [key for key, val in blackjack_values.items() if val == value]
        for value in values
    }


def count_lower_cards(deck: list[int], threshold: int) -> int:
    """Count the number of cards in a deck lower than a threshold.

    Args:
        deck (list): Current deck.
        threshold (int): Value of card.

    Returns:
        int: Number of cards lower than threshold.
    """
    return sum(card < threshold for card in deck)


def calculate_hand_value(hand: list[int]) -> np.ndarray:
    """Calculate the possible values of the current hand.

    Usefull for aces.

    Args:
        hand (list): Current hand.

    Returns:
        possible_totals (np.ndarray): Possible values for the current hand.
    """
    aces = hand.count(0)
    try:
        hand.remove(0)
    except ValueError:
        pass
    values = [blackjack_values[card] for card in hand]

    total = sum(values)

    possible_totals = total + 10 * np.arange(aces + 1)

    possible_totals = possible_totals[possible_totals < 22]

    return possible_totals


def format_data(
    scores: list[list[int]], dealer_hands: list[list[int]]
) -> tuple[int, pd.DataFrame]:
    """Format the data to plot dealer hands vs payout.

    Args:
        scores (list): Payout for each game.
        dealer_hands (list): Hand of dealers for each game.

    Returns:
        n_players (int): Number of players.
        df (pd.DataFrame): formated data.
    """
    n_players = len(scores[0])
    scores_by_player = [[row[i] for row in scores] for i in range(n_players)]
    dealer_hands_max = [max(dealer_hand) for dealer_hand in dealer_hands]

    df = pd.DataFrame({"Dealer Hand": dealer_hands_max})
    for player in range(n_players):
        df[f"Player {player + 1}"] = scores_by_player[player]
    return n_players, df


if __name__ == "__main__":
    pass
