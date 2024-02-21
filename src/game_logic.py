"""All logic connected to the game."""

import random
from typing import Any

import numpy as np

from src.lookups import (
    double_down_table_hard,
    double_down_table_soft,
    split_combinations,
)
from src.util import calculate_hand_value, count_lower_cards, reverse_lookup


def create_deck(n_decks: int) -> list[int]:
    """Create a deck to play with.

    Args:
        n_decks (int): Number of decks to mix together

    Returns:
        total_deck (list): Ready deck.
    """
    basic_cards = list(range(13))

    basic_deck = basic_cards * 4

    total_deck = basic_deck * n_decks

    return total_deck


def draw_card(
    current_deck: list[int], hand: list[int], n_cards: int
) -> tuple[list[int], list[int]]:
    """Draw n cards from the current deck.

    Args:
        current_deck (list): Current deck.
        hand (list): Current hand.
        n_cards (int): Number of cards to draw.

    Returns:
        hand (list): New hand with drawn cards.
        current_deck (list): Current deck.
    """
    cards = random.sample(current_deck, k=n_cards)
    for card in cards:
        del current_deck[current_deck.index(card)]
    hand.extend(cards)
    return hand, current_deck


def check_if_bust(possible_totals: np.ndarray) -> np.ndarray:
    """Check if the values of the hand go over 21 and remove them.

    Args:
        possible_totals (list): Possible values of hand.

    Returns:
        possible_totals (list): Viable card values.
    """
    index = possible_totals > 21
    possible_totals = possible_totals[index]
    return possible_totals


def should_draw(
    possible_totals: np.ndarray,
    deck: list[int],
    is_dealer: bool,
    ceartainty: float,
) -> bool:
    """Decide if a card should be drawn.

    Args:
        possible_totals (list): Possible values of current hand.
        deck (list): Current deck.
        is_dealer (bool): Is the current player the dealer.
        ceartainty (float): How safe must a draw be to take a card.

    Returns:
        bool: Should a card be drawn.
    """
    if np.any(possible_totals > 16) and is_dealer:
        return False
    elif is_dealer:
        return True
    elif np.any(possible_totals > 17):
        return False
    elif np.any(possible_totals < 11):
        return True
    desired_cards = reverse_lookup(21 - possible_totals)
    desired_cards_in_deck = count_lower_cards(
        deck,
        list(desired_cards.values())[0][0],
    )
    chance_of_getting_desired_card = desired_cards_in_deck / len(deck)
    if chance_of_getting_desired_card > ceartainty:
        return True
    else:
        return False


def should_double(current_hand: list[int], dealers_hand_open: list[int]) -> bool:
    """Determine if the player should double down.

    Args:
        current_hand (list): Current hand.
        dealers_hand_open (list): Dealers visible hand.

    Returns:
        bool: Should the player double down.
    """
    possibilities = calculate_hand_value(current_hand)
    try:
        if 0 in current_hand:
            return double_down_table_soft[max(possibilities)][dealers_hand_open[0]]
        else:
            return double_down_table_hard[possibilities[0]][dealers_hand_open[0]]
    except KeyError:
        return False


def draw_until_bust_or_hold(
    current_deck: list[int],
    current_hand: list[int],
    is_dealer: bool,
    ceartainty: float,
) -> tuple[list[int], np.ndarray, list[int]]:
    """Draw cards until the hand is bust or the player should hold.

    Args:
        current_deck (list): Current deck.
        current_hand (list): Current hand.
        is_dealer (bool): Is the current player the dealer.
        ceartainty (float): How safe must a draw be to take a card.

    Returns:
        current_deck (list): Current deck
        possibilities (list): Possible values of current hand.
        current_hand (list): Current hand.
    """
    possibilities = calculate_hand_value(current_hand)

    draw = should_draw(possibilities, current_deck, is_dealer, ceartainty)

    while draw:
        current_hand, current_deck = draw_card(current_deck, current_hand, 2)

        possibilities = calculate_hand_value(current_hand)

        if len(possibilities) < 1:
            return current_deck, [0], current_hand

        draw = should_draw(possibilities, current_deck, is_dealer, ceartainty)
    return current_deck, possibilities, current_hand


def check_outcome(
    dealers_hand_open: list[int],
    dealer_possibilities: np.ndarray,
    player_hands: list[np.ndarray],
) -> list[float]:
    """Calculate the outcome of a single game.

    Args:
        dealers_hand_open (list): Dealers hand
        dealer_possibilities (list): Value of the dealers hand.
        player_hands (list): Hands of the players.

    Returns:
        outcomes (list): Outcome of the game for each player
    """
    outcomes = [
        (
            1.5
            if 21 in possibilities
            and len(hand) == 2
            and not (
                21 in dealer_possibilities and len(dealers_hand_open)
            )  # Blackjack win
            else (
                1
                if max(possibilities) > max(dealer_possibilities)  # Normal win
                else (
                    0
                    if max(possibilities) == max(dealer_possibilities)
                    and max(possibilities) != 0  # Draw
                    else -1  # Loss
                )
            )
        )
        for possibilities, hand in player_hands
    ]
    return outcomes


def check_outcome_split(
    dealers_hand_open: list[int],
    dealer_possibilities: np.ndarray,
    split_hands: list[list[np.ndarray]],
) -> list[tuple[float, Any]]:
    """Calculate the outcome of all split hands in a single game.

    Args:
        dealers_hand_open (list): Dealers hand
        dealer_possibilities (list): Value of the dealers hand.
        player_hands (list): Hands of the players.

    Returns:
        outcomes (list): Outcome of the game for each player
    """
    outcomes = [
        (
            (
                1.5
                if 21 in possibilities
                and len(hand) == 2
                and not (
                    21 in dealer_possibilities and len(dealers_hand_open)
                )  # Blackjack win
                else (
                    1
                    if max(possibilities) > max(dealer_possibilities)  # Normal win
                    else (
                        0
                        if max(possibilities) == max(dealer_possibilities)
                        and max(possibilities) != 0  # Draw
                        else -1  # Loss
                    )
                )
            ),
            player,
        )
        for possibilities, hand, player in split_hands
    ]
    return outcomes


def play_split_hand(
    split_hands: list[Any],  # TODO: something wrong with split, should be fixed
    player_id: int,
    current_hand: list[int],
    current_deck: list[int],
    ceartainty: float,
) -> tuple[list[int], list[Any]]:
    """Play a split hand.

    Args:
        split_hands (list): List of split hands.
        Player_id (int): Player id.
        current_hand (list): Current hand.
        current_deck (list): Current deck.
        ceartainty (float): How safe must a draw be to take a card.

    Returns:
        current_hand (list): Current hand.
        split_hands (list): list of split hands.
    """
    split_hand = [current_hand[0]]

    current_deck, possibilities, split_hand = draw_until_bust_or_hold(
        current_deck, split_hand, is_dealer=False, ceartainty=ceartainty
    )
    split_hands.append([possibilities, split_hand, player_id])

    current_hand = [current_hand[1]]
    return current_hand, split_hands


def play_game(
    current_deck: list[int],
    n_players: int,
    use_split: bool,
    ceartainty: float,
) -> tuple[np.ndarray, list[int], np.ndarray]:
    """Play blackjack.

    Args:
        current_deck (list): Current Deck.
        n_players (int): Number of players.
        use_split (bool): Should split be used.
        ceartainty (float): How safe must a draw be to take a card.

    Returns:
        returns (np.ndarray): The result of a game for all players.
        current_deck (list): Current deck.
        dealer_posibilities (list): Values of dealers hand.
    """
    # Dealer draws first card
    dealers_hand_open, current_deck = draw_card(current_deck, [], 1)
    multiplyer = np.ones(n_players)
    # Players' turns
    player_hands = []
    split_hands: list[Any] = []
    for i in range(n_players):
        current_hand, current_deck = draw_card(current_deck, [], 2)
        if (
            current_hand[0] == current_hand[1]
            and split_combinations[current_hand[0]][dealers_hand_open[0]]
        ) and use_split:
            current_hand, split_hands = play_split_hand(
                split_hands, i, current_hand, current_deck, ceartainty
            )
        if should_double(current_hand, dealers_hand_open):
            multiplyer[i] = 2
            current_hand, current_deck = draw_card(current_deck, current_hand, 1)
            possibilities = calculate_hand_value(current_hand)
        else:
            current_deck, possibilities, current_hand = draw_until_bust_or_hold(
                current_deck, current_hand, ceartainty=ceartainty, is_dealer=False
            )
        player_hands.append([possibilities, current_hand])

    current_deck, dealer_possibilities, dealers_hand_open = draw_until_bust_or_hold(
        current_deck, dealers_hand_open, ceartainty=ceartainty, is_dealer=True
    )

    returns = check_outcome(
        dealers_hand_open,
        dealer_possibilities,
        player_hands,
    )

    returns *= multiplyer

    returns_split = check_outcome_split(
        dealers_hand_open,
        dealer_possibilities,
        split_hands,
    )

    for result, player in returns_split:
        returns[player] += result

    return returns, current_deck, dealer_possibilities


if __name__ == "__main__":
    pass
