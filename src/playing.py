"""Functions for playing games."""

from multiprocessing import Pool

import numpy as np

from src.game_logic import create_deck, play_game


def play_single_game(
    n_players: int,
    n_decks: int,
    deck: list[int],
    use_split: bool,
    ceartainty: float,
) -> tuple[np.ndarray, list[int], list[int]]:
    """Play a single game of blackjack.

    Args:
        n_players (int): Number of players.
        n_decks (int): Number of decks.
        deck (list): Current deck.
        use_split (bool): Should split be used.
        ceartainty (float): How safe must a draw be to take a card.

    Returns:
        game_score (nd.array): Score of the game for each player.
        dealers_hand_open (list): The dealers hand that is visible.
        modified_deck (list): The deck as it looks after the game is finished.
    """
    if len(deck) < n_decks / 2 * 52:
        deck = create_deck(n_decks=n_decks)
    game_score, modified_deck, dealers_hand_open = play_game(
        deck, n_players, use_split, ceartainty
    )
    return game_score, dealers_hand_open, modified_deck


def play_multiple_games(
    n_players: int,
    n_decks: int,
    deck: list[int],
    use_split: bool,
    games_pr_deck: int,
    ceartainty: float,
) -> tuple[list[np.ndarray], list[list[int]]]:
    """Play multiple games of blackjack.

    Args:
        n_players (int): Number of players.
        n_decks (int): Number of decks.
        deck (list): Current deck.
        use_split (bool): Should split be used.
        games_pr_deck (int): Number of games each deck should be used.
        ceartainty (float): How safe must a draw be to take a card.

    Returns:
        game_scores (list): Scores from every game played.
        dealer_hands (list): The hand the dealers ended with in every game.
    """
    game_scores = []
    dealer_hands = []
    for _ in range(games_pr_deck):
        game_score, dealers_hand_open, deck = play_single_game(
            n_players, n_decks, deck, use_split, ceartainty
        )
        game_scores.append(game_score)
        dealer_hands.append(dealers_hand_open)
    return game_scores, dealer_hands


def play_multiple_decks(
    n_players: int,
    n_decks: int,
    n_games: int,
    use_split: bool,
    games_pr_deck: int,
    ceartainty: float = 0.9,
) -> tuple[list[list[np.ndarray]], list[list[int]]]:
    """Play multiple decks at the same time.

    Args:
        n_players (int): Number of players.
        n_decks (int): Number of decks.
        n_games (int): Total number of games.
        use_split (bool): Should split be used.
        games_pr_deck (int): Number of games each deck should be used.
        ceartainty (float, optional): How safe must a draw be to take a card.
                                      Defaults to 0.9.

    Returns:
        all_game_scores (list): Scores from every game played.
        all_dealer_hands (list): The hand the dealers ended with in every game.
    """
    all_game_scores = []
    all_dealer_hands = []

    # Create a list of decks
    decks = [create_deck(n_decks=n_decks) for _ in range(int(n_games / games_pr_deck))]
    try:
        with Pool() as pool:
            results = pool.starmap(
                play_multiple_games,
                [
                    (n_players, n_decks, deck, use_split, games_pr_deck, ceartainty)
                    for deck in decks
                ],
            )

        for game_scores, dealer_hands in results:
            all_game_scores.extend(game_scores)
            all_dealer_hands.extend(dealer_hands)
        return all_game_scores, all_dealer_hands
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()

    return all_game_scores, all_dealer_hands


if __name__ == "__main__":
    pass
