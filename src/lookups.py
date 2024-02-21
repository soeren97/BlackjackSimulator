"""Lookup tables for game logic."""

import pandas as pd

blackjack_values = {
    0: 1,
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
    10: 10,
    11: 10,
    12: 10,
}

true_row = [True for _ in range(13)]
false_row = [False for _ in range(13)]

split_combinations = pd.DataFrame(
    [
        true_row,
        true_row,
        true_row,
        false_row,
        false_row,
        true_row,
        true_row,
        true_row,
        true_row,
        false_row,
        false_row,
        false_row,
        false_row,
    ],
    columns=[
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
    ],
)

split_combinations.iloc[5] = False
split_combinations.iloc[1:7, 7:13] = False
split_combinations.iloc[1:4, :3] = False
split_combinations.iloc[0, 1:7] = False
split_combinations.iloc[5, 2:6] = True
split_combinations.iloc[8, 9:] = False
split_combinations.iloc[8, 0] = False
split_combinations.iloc[8, 6] = False

double_down_table_soft = {
    14: {5: True, 6: True},
    15: {4: True, 5: True, 6: True},
    16: {4: True, 5: True, 6: True},
    17: {3: True, 4: True, 5: True, 6: True},
    18: {3: True, 4: True, 5: True, 6: True},
}

double_down_table_hard = {
    9: {3: True, 4: True, 5: True, 6: True},
    10: {2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True},
    11: {
        2: True,
        3: True,
        4: True,
        5: True,
        6: True,
        7: True,
        8: True,
        9: True,
        10: True,
    },
}

plotting_map = {
    16: "bust",
    17: 17,
    18: 18,
    19: 19,
    20: 20,
    21: 21,
}

if __name__ == "__main__":
    pass
