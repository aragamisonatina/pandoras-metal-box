### PANDORA'S METAL BOX by JVARNEY (IZ) and TTROSSARD (LD)
import math
import numpy as np
import pandas as pd
import random as rd
import time

PATH = "all_tanks.csv"
ALL_TANKS = pd.read_csv(PATH)
SUBTRACTOR_VALUES = [40, 45, 50, 50, 55, 60]
CLASSES = {
    "L": "LIGHT TANK",
    "M": "MEDIUM TANK",
    "H": "HEAVY TANK",
    "SH": "SUPER-HEAVY TANK",
    "TD": "TANK DESTROYER",
    "MBT": "MAIN BATTLE TANK",
    "SPH": "SELF-PROPELLED HOWITZER",
    "SPAA": "SELF-PROPELLED ANTI-AIRCRAFT"
}

DIVISIONS = {
    "AA": "L'EGIDE DOREE",
    "ED": "RISHI LONG",
    "FT": "FROST TITAN",
    "IZ": "IRON ZEPHYR",
    "RS": "KRASNAYA ZVEZDA",
}
RARITIES = {
    "C": "COMMON",
    "UC": "UNCOMMON",
    "R": "RARE",
    "VR": "VERY RARE",
    "L": "LEGENDARY"
}


def _calculate_cost(stars: int, **kwargs) -> int:
    add_ons = 0
    return stars*3000 + add_ons


def fifa_shit(tank_df : pd.DataFrame):
    print(f'\n*** Awaiting... from {DIVISIONS[tank_df["DIVISION"].iloc[0]]} ***')

    time.sleep(3)
    print(f'\n*** RARITY: {RARITIES[tank_df["RARITY"].iloc[0]]} ***')

    time.sleep(1)
    print(f'\n*** {CLASSES[tank_df["CLASS"].iloc[0]]} ***')

    time.sleep(1)
    print(f'\n*** {str(tank_df["STARS"].iloc[0]).upper()} STARS ***')

    time.sleep(1)
    print(f'\n*** {tank_df["OPERATOR"].iloc[0].upper()} ***')

    time.sleep(3)
    print(f'\n\nYou pulled: {tank_df["TANK"].iloc[0].upper()}!!!')



def get_tank_df(name: str) -> pd.DataFrame:
    match = ALL_TANKS[ALL_TANKS["TANK"].str.casefold().eq(name.casefold())]
    if match.empty:
        raise KeyError(f"Tank not found: {name}")
    return match.iloc[[0]]  # keep as DataFrame


def gacha_main(tank_df: pd.DataFrame, premium: bool = False):
    cr = float(tank_df["TCR"].iloc[0])
    mood_d6 = 1 if premium else rd.randint(1, 6)
    subtractor = SUBTRACTOR_VALUES[mood_d6 - 1]
    roll = rd.randint(1, 100)

    multiplier = 0.05 if premium else (0.04 if cr <= 23 else 0.03)

    new_tank_cr = cr + (roll - subtractor) * multiplier
    # quantize DOWN to nearest 0.25 safely
    target_cr = math.floor(new_tank_cr * 4 + 1e-9) / 4

    # precompute sorted unique CRs
    cr_vals = np.sort(ALL_TANKS["TCR"].unique())

    # pick the highest available CR ≤ target_cr
    eligible = cr_vals[cr_vals <= target_cr]
    if eligible.size == 0:
        # if nothing is ≤ target, fall back to the minimum available
        chosen_cr = cr_vals.min()
    else:
        chosen_cr = eligible.max()

    # pull random tank among those with that CR
    filtered = ALL_TANKS[ALL_TANKS["TCR"].eq(chosen_cr)]
    fifa_shit(filtered.sample(1))



def tank_in_database(name: str):
    return name.lower() in ALL_TANKS['TANK'].str.lower().values


def main():
    print(" [Welcome to PANDORA'S METAL BOX] ")
    print("---by J. VARNEY and T. TROSSARD---")
    print("")

    while True:
        try:
            tank = str(input("Choose your tank: "))
            if tank_in_database(tank):
                tank_df = get_tank_df(tank)
                break
            else:
                raise ValueError
        except ValueError:
            print("Please enter a valid tank...\n")

    actual_tank_name = tank_df["TANK"].iloc[0]

    print(f"You're sacrificing your {actual_tank_name}? Interesting.")

    gacha_main(tank_df, premium=False)



if __name__ == '__main__':
    main()