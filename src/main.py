### PANDORA'S METAL BOX by JVARNEY (IZ) and TTROSSARD (LD)
import math
import numpy as np
import pandas as pd
import random as rd
import time
import os
import sys
import pygame

# Handle file paths for both development and PyInstaller executable
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # For development, use the directory where this script is located
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

PATH = resource_path("all_tanks.csv")
ALL_TANKS = pd.read_csv(PATH)
SUBTRACTOR_VALUES = [40, 45, 50, 50, 55, 60]
CLASSES = {
    "L": "LIGHT TANK",
    "M": "MEDIUM TANK",
    "H": "HEAVY TANK",
    "SH": "SUPER-HEAVY TANK",
    "TD": "TANK DESTROYER",
    "IFV": "INFANTRY FIGHTING VEHICLE",
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


# Add near your constants
RARITY_ORDER = ["C", "UC", "R", "VR", "L"]  # low → high

def get_allowed_tanks(tank_df: pd.DataFrame, premium: bool) -> pd.DataFrame:
    """Premium = all tanks.
       No premium + VR → up to VR.
       No premium + R  → up to R.
       Else            → C & UC only.
    """
    if premium:
        return ALL_TANKS

    rarity = str(tank_df["RARITY"].iloc[0])
    if rarity == "VR":
        cap = "VR"
    elif rarity == "R":
        cap = "R"
    else:
        return ALL_TANKS[ALL_TANKS["RARITY"].isin(["C", "UC"])]

    cap_idx = RARITY_ORDER.index(cap)
    allowed_set = set(RARITY_ORDER[:cap_idx + 1])
    return ALL_TANKS[ALL_TANKS["RARITY"].isin(allowed_set)]


def _calculate_cost(stars: int, **kwargs) -> int:
    add_ons = 0
    return stars*3000 + add_ons


def fifa_shit(tank_df : pd.DataFrame):
    # Initialize pygame mixer for audio
    try:
        pygame.mixer.init()
        audio_path = resource_path("fc 25 pull.mp3")
        if os.path.exists(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
        else:
            print(f"Audio file not found: {audio_path}")
    except Exception as e:
        # If audio fails, continue without sound
        print(f"Audio error (continuing without sound): {e}")
    
    print(f'\n*** Awaiting... from {DIVISIONS[tank_df["DIVISION"].iloc[0]]} ***')

    time.sleep(3.14)
    print(f'\n*** RARITY: {RARITIES[tank_df["RARITY"].iloc[0]]} ***')

    time.sleep(1)
    print(f'\n*** {CLASSES[tank_df["CLASS"].iloc[0]]} ***')

    time.sleep(1)
    print(f'\n*** {str(tank_df["STARS"].iloc[0]).upper()} STARS ***')

    time.sleep(5)
    print(f'\n*** {tank_df["OPERATOR"].iloc[0].upper()} ***')

    time.sleep(1.46)
    print(f'\n\nYou pulled: {tank_df["TANK"].iloc[0].upper()}!!!')
    
    
    time.sleep(14)
    # Stop the music after the reveal
    try:
        pygame.mixer.music.stop()
    except:
        pass



def get_tank_df(name: str) -> pd.DataFrame:
    match = ALL_TANKS[ALL_TANKS["TANK"].str.casefold().eq(name.casefold())]
    if match.empty:
        raise KeyError(f"Tank not found: {name}")
    return match.iloc[[0]]  # keep as DataFrame


def gacha_main(tank_df: pd.DataFrame, premium: bool = False):
    # 1 - Pool restriction by rarity
    allowed_tanks = get_allowed_tanks(tank_df, premium=premium)

    # 2 - Roll mood & upgrade math
    cr = float(tank_df["TCR"].iloc[0])
    mood_d6 = 1 if premium else rd.randint(1, 6)
    subtractor = SUBTRACTOR_VALUES[mood_d6 - 1]
    roll = rd.randint(1, 100)

    multiplier = 0.05 if premium else (0.04 if cr <= 23 else 0.03)
    new_tank_cr = cr + (roll - subtractor) * multiplier

    # Quantize DOWN to nearest 0.25 safely
    target_cr = math.floor(new_tank_cr * 4 + 1e-9) / 4

    # 3 - Choose CR from the allowed pool only
    cr_vals = np.sort(allowed_tanks["TCR"].unique())
    eligible = cr_vals[cr_vals <= target_cr]

    if eligible.size == 0:
        # nothing <= target: take the minimum in the allowed pool
        chosen_cr = cr_vals.min()
    else:
        chosen_cr = eligible.max()

    # 4 - If no tank exactly at chosen_cr (float quirks), step down in 0.25 until found
    #    (guard against infinite loop by flooring at min)
    min_allowed = cr_vals.min()
    current = chosen_cr
    while True:
        filtered = allowed_tanks[allowed_tanks["TCR"].eq(current)]
        if not filtered.empty:
            break
        current = round(current - 0.25, 2)  # keep tidy decimals
        if current < min_allowed:
            # fallback: pick the closest lower-or-equal available CR
            current = min_allowed
            filtered = allowed_tanks[allowed_tanks["TCR"].eq(current)]
            break

    # 5) Reveal random pick at that CR
    fifa_shit(filtered.sample(1))




def tank_in_database(name: str):
    return name.lower() in ALL_TANKS['TANK'].str.lower().values


def show_available_tanks():
    """Display some available tanks to help the user"""
    print("\nHere are some available tanks you can sacrifice:")
    sample_tanks = ALL_TANKS['TANK'].sample(8).tolist()  # Show 8 random tanks
    for i, tank in enumerate(sample_tanks, 1):
        print(f"  {i}. {tank}")
    print("  ... and more!")
    print("\nTip: Tank names are case-insensitive.\n")


def main():
    print(" [Welcome to PANDORA'S METAL BOX] ")
    print("---by J. VARNEY and T. TROSSARD---")
    print("")

    # Show available tanks on first run
    show_available_tanks()

    while True:
        # Get tank input
        invalid_attempts = 0
        while True:
            try:
                tank = str(input("Choose your tank: "))
                if tank_in_database(tank):
                    tank_df = get_tank_df(tank)
                    break
                else:
                    invalid_attempts += 1
                    if invalid_attempts == 1:
                        print("Tank not found. Please check the spelling and try again.")
                    elif invalid_attempts == 2:
                        print("Still having trouble? Here are some examples:")
                        show_available_tanks()
                    else:
                        print("Please enter a valid tank name from the list above.\n")
            except ValueError:
                print("Please enter a valid tank...\n")

        actual_tank_name = tank_df["TANK"].iloc[0]
        print(f"You're sacrificing your {actual_tank_name}? Interesting.")

        # Run the gacha
        gacha_main(tank_df, premium=False)
        
        # Ask if user wants to roll again
        print("\n" + "="*50)
        while True:
            try:
                choice = input("\nWould you like to sacrifice another tank? (y/n): ").lower().strip()
                if choice in ['y', 'yes', 'yeah', 'yep', 'ya']:
                    print("\nPrepare another sacrifice...\n")
                    break
                elif choice in ['n', 'no', 'nope', 'nah']:
                    print("\nThanks for using Pandora's Metal Box!")
                    print("May your future rolls be blessed! 🎲")
                    input("\nPress Enter to exit...")
                    return
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
            except (EOFError, KeyboardInterrupt):
                print("\n\nThanks for using Pandora's Metal Box!")
                return



if __name__ == '__main__':
    main()