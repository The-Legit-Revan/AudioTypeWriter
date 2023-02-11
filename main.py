import contextlib
import json
import os
import random
import time
import wave
from datetime import datetime
from typing import Dict, List, Tuple

import numpy as np
import pyautogui
import soundfile as sf
from pympler import asizeof


TYPEWRITING_CODE = False

CODE_EDITOR = {
    "Visual Studio Code": False,
    # "Sublime Text"      : "NOT IMPLEMENTED YET",
    # "Atom"              : "NOT IMPLEMENTED YET",
    # "Notepad++"         : "NOT IMPLEMENTED YET"
}


# Constant variables

KEYS = {
    "\n": ("Enter.wav", "Enter2.wav", "Enter_Hard-Press.wav"),
    " ": ("Spacebar.wav", "Space_Hard-Press.wav", "Space_Hard-Press2.wav", "Space_Hard-Press3.wav"),
    "    ": "Tab.wav",
    "\t": "Tab.wav",
    "'": ("'.wav", "'_Hard-Press.wav"),
    ",": (",.wav", ",_Hard-Press.wav"),
    "-": ("-.wav", "-_Hard-Press.wav"),
    ".": ("..wav", "._Hard-Press.wav"),
    "/": ("Forwardslash.wav", "Forwardslash_Hard-Press.wav"),
    "0": ("0.wav", "0_Hard-Press.wav"),
    "1": ("1.wav", "1_Hard-Press.wav"),
    "2": ("2.wav", "2_Hard-Press.wav"),
    "3": ("3.wav", "3_Hard-Press.wav"),
    "4": ("4.wav", "4_Hard-Press.wav"),
    "5": ("5.wav", "5_Hard-Press.wav"),
    "6": ("6.wav", "6_Hard-Press.wav"),
    "7": ("7.wav", "7_Hard-Press.wav"),
    "8": ("8.wav", "8_Hard-Press.wav"),
    "9": ("9.wav", "9_Hard-Press.wav"),
    ";": (";.wav", ";_Hard-Press.wav"),
    "=": ("=.wav", "=_Hard-Press.wav"),
    "Special Keys": {
        "Shift": ("R-Shift.wav", "R-Shift_Hard-Press.wav", "Shift.wav", "Shift_Hard-Press.wav"),
        "Arrows": {
            "Down": "Arrow_Down.wav",
            "Left": "Arrow_Left.wav",
            "Right": "Arrow_Right.wav",
            "Up": "Arrow_Up.wav",
        },
        "Caps": "Caps_Lock.wav",
        "Ctrl": ("Ctrl.wav", "Ctrl_Hard-Press.wav"),
        "Del": "Backspace.wav",
        "Numpad": {
            "0": "Num_0.wav",
            "1": "Num_1.wav",
            "2": "Num_2.wav",
            "3": "Num_3.wav",
            "4": "Num_4.wav",
            "5": "Num_5.wav",
            "6": "Num_6.wav",
            "7": "Num_7.wav",
            "8": "Num_8.wav",
            "9": "Num_9.wav",
            "/": "Num_Forwardslash.wav",
            "*": "Num_Star.wav",
            "-": "Num_-.wav",
            "+": "Num_+.wav",
            "\n": "Num_Enter.wav",
            ".": "Num_..wav",
        },
    },
    "[": ("[.wav", "[_Hard-Press.wav"),
    "\\": ("Backslash.wav", "Backslash_Hard-Press.wav"),
    "]": ("].wav", "]_Hard-Press.wav"),
    "`": ("`.wav", "`_Hard-Press.wav"),
    "a": ("a.wav", "a_Hard-Press.wav"),
    "b": ("b.wav", "b_Hard-Press.wav"),
    "c": ("c.wav", "c_Hard-Press.wav"),
    "d": ("d.wav", "d_Hard-Press.wav"),
    "e": ("e.wav", "e_Hard-Press.wav"),
    "f": ("f.wav", "f_Hard-Press.wav"),
    "g": ("g.wav", "g_Hard-Press.wav"),
    "h": ("h.wav", "h_Hard-Press.wav"),
    "i": ("i.wav", "i_Hard-Press.wav"),
    "j": ("j.wav", "j_Hard-Press.wav"),
    "k": ("k.wav", "k_Hard-Press.wav"),
    "l": ("l.wav", "l_Hard-Press.wav"),
    "m": ("m.wav", "m_Hard-Press.wav"),
    "n": ("n.wav", "n_Hard-Press.wav"),
    "o": ("o.wav", "o_Hard-Press.wav"),
    "p": ("p.wav", "p_Hard-Press.wav"),
    "q": ("q.wav", "q_Hard-Press.wav"),
    "r": ("r.wav", "r_Hard-Press.wav"),
    "s": ("s.wav", "s_Hard-Press.wav"),
    "t": ("t.wav", "t_Hard-Press.wav"),
    "u": ("u.wav", "u_Hard-Press.wav"),
    "v": ("v.wav", "v_Hard-Press.wav"),
    "w": ("w.wav", "w_Hard-Press.wav"),
    "x": ("x.wav", "x_Hard-Press.wav"),
    "y": ("y.wav", "y_Hard-Press.wav"),
    "z": ("z.wav", "z_Hard-Press.wav"),
}

SHIFT_KEYS = {
    "!": "1",
    '"': "'",
    "#": "3",
    "$": "4",
    "%": "5",
    "&": "7",
    "(": "9",
    ")": "0",
    "*": "8",
    "+": "=",
    ":": ";",
    "<": ",",
    ">": ".",
    "?": "/",
    "@": "2",
    "A": "a",
    "B": "b",
    "C": "c",
    "D": "d",
    "E": "e",
    "F": "f",
    "G": "g",
    "H": "h",
    "I": "i",
    "J": "j",
    "K": "k",
    "L": "l",
    "M": "m",
    "N": "n",
    "O": "o",
    "P": "p",
    "Q": "q",
    "R": "r",
    "S": "s",
    "T": "t",
    "U": "u",
    "V": "v",
    "W": "w",
    "X": "x",
    "Y": "y",
    "Z": "z",
    "^": "6",
    "_": "-",
    "{": "[",
    "|": "\\",
    "}": "]",
    "~": "`",
}

DURATION = {
    "'.wav": 0.24303854875283445,
    "'_Hard-Press.wav": 0.25825396825396824,
    ",.wav": 0.2308843537414966,
    ",_Hard-Press.wav": 0.24043083900226758,
    "-.wav": 0.2226530612244898,
    "-_Hard-Press.wav": 0.2710657596371882,
    "..wav": 0.2916326530612245,
    "._Hard-Press.wav": 0.2633333333333333,
    "0.wav": 0.20142857142857143,
    "0_Hard-Press.wav": 0.3045578231292517,
    "1.wav": 0.22210884353741497,
    "1_Hard-Press.wav": 0.297437641723356,
    "2.wav": 0.24634920634920635,
    "2_Hard-Press.wav": 0.27936507936507937,
    "3.wav": 0.20324263038548754,
    "3_Hard-Press.wav": 0.2761904761904762,
    "4.wav": 0.2100453514739229,
    "4_Hard-Press.wav": 0.2801814058956916,
    "5.wav": 0.233015873015873,
    "5_Hard-Press.wav": 0.286281179138322,
    "6.wav": 0.21281179138321996,
    "6_Hard-Press.wav": 0.27408163265306124,
    "7.wav": 0.2371201814058957,
    "7_Hard-Press.wav": 0.27714285714285714,
    "8.wav": 0.2272562358276644,
    "8_Hard-Press.wav": 0.27714285714285714,
    "9.wav": 0.22419501133786848,
    "9_Hard-Press.wav": 0.30183673469387756,
    ";.wav": 0.23755102040816325,
    ";_Hard-Press.wav": 0.2978684807256236,
    "=.wav": 0.2289795918367347,
    "=_Hard-Press.wav": 0.27104308390022674,
    "Arrow_Down.wav": 0.27138321995464854,
    "Arrow_Left.wav": 0.26328798185941044,
    "Arrow_Right.wav": 0.2507709750566893,
    "Arrow_Up.wav": 0.2865532879818594,
    "Backslash.wav": 0.24501133786848073,
    "Backslash_Hard-Press.wav": 0.28165532879818594,
    "Backspace.wav": 0.26104308390022674,
    "Caps_Lock.wav": 0.23900226757369614,
    "Ctrl.wav": 0.2710657596371882,
    "Ctrl_Hard-Press.wav": 0.29784580498866214,
    "Enter.wav": 0.2505215419501134,
    "Enter2.wav": 0.28625850340136055,
    "Enter_Hard-Press.wav": 0.2548072562358277,
    "Forwardslash.wav": 0.2754195011337868,
    "Forwardslash_Hard-Press.wav": 0.24562358276643992,
    "Num_+.wav": 0.2801360544217687,
    "Num_-.wav": 0.25528344671201814,
    "Num_..wav": 0.25528344671201814,
    "Num_0.wav": 0.2370294784580499,
    "Num_1.wav": 0.34718820861678007,
    "Num_2.wav": 0.21294784580498866,
    "Num_3.wav": 0.21968253968253967,
    "Num_4.wav": 0.2511337868480726,
    "Num_5.wav": 0.2227891156462585,
    "Num_6.wav": 0.2389342403628118,
    "Num_7.wav": 0.25859410430839,
    "Num_8.wav": 0.3340136054421769,
    "Num_9.wav": 0.2588662131519274,
    "Num_Enter.wav": 0.26328798185941044,
    "Num_Forwardslash.wav": 0.250249433106576,
    "Num_Star.wav": 0.25859410430839,
    "R-Shift.wav": 0.2083219954648526,
    "R-Shift_Hard-Press.wav": 0.24959183673469387,
    "Shift.wav": 0.4148299319727891,
    "Shift_Hard-Press.wav": 0.28757369614512474,
    "Space_Hard-Press.wav": 0.23448979591836736,
    "Space_Hard-Press2.wav": 0.24834467120181405,
    "Space_Hard-Press3.wav": 0.26954648526077096,
    "Spacebar.wav": 0.26564625850340134,
    "Tab.wav": 0.2410657596371882,
    "[.wav": 0.23056689342403627,
    "[_Hard-Press.wav": 0.2565532879818594,
    "].wav": 0.1992063492063492,
    "]_Hard-Press.wav": 0.2633333333333333,
    "`.wav": 0.22210884353741497,
    "`_Hard-Press.wav": 0.297437641723356,
    "a.wav": 0.21866213151927438,
    "a_Hard-Press.wav": 0.25882086167800455,
    "b.wav": 0.2256235827664399,
    "b_Hard-Press.wav": 0.22866213151927436,
    "c.wav": 0.24303854875283445,
    "c_Hard-Press.wav": 0.2633333333333333,
    "d.wav": 0.21065759637188208,
    "d_Hard-Press.wav": 0.24043083900226758,
    "e.wav": 0.24501133786848073,
    "e_Hard-Press.wav": 0.2923809523809524,
    "f.wav": 0.19693877551020408,
    "f_Hard-Press.wav": 0.28165532879818594,
    "g.wav": 0.2,
    "g_Hard-Press.wav": 0.2862358276643991,
    "h.wav": 0.1992063492063492,
    "h_Hard-Press.wav": 0.2473015873015873,
    "i.wav": 0.22038548752834466,
    "i_Hard-Press.wav": 0.2562358276643991,
    "j.wav": 0.22179138321995465,
    "j_Hard-Press.wav": 0.26562358276643994,
    "k.wav": 0.21623582766439908,
    "k_Hard-Press.wav": 0.24501133786848073,
    "l.wav": 0.21065759637188208,
    "l_Hard-Press.wav": 0.22319727891156463,
    "m.wav": 0.23755102040816325,
    "m_Hard-Press.wav": 0.23126984126984126,
    "n.wav": 0.21927437641723355,
    "n_Hard-Press.wav": 0.2175283446712018,
    "o.wav": 0.2363718820861678,
    "o_Hard-Press.wav": 0.2633333333333333,
    "p.wav": 0.22668934240362812,
    "p_Hard-Press.wav": 0.31691609977324264,
    "q.wav": 0.19970521541950115,
    "q_Hard-Press.wav": 0.2801814058956916,
    "r.wav": 0.18319727891156462,
    "r_Hard-Press.wav": 0.28321995464852606,
    "s.wav": 0.2289795918367347,
    "s_Hard-Press.wav": 0.27936507936507937,
    "t.wav": 0.21405895691609977,
    "t_Hard-Press.wav": 0.29845804988662133,
    "u.wav": 0.1980045351473923,
    "u_Hard-Press.wav": 0.2512925170068027,
    "v.wav": 0.2314512471655329,
    "v_Hard-Press.wav": 0.24961451247165534,
    "w.wav": 0.19546485260770974,
    "w_Hard-Press.wav": 0.30759637188208616,
    "x.wav": 0.2234920634920635,
    "x_Hard-Press.wav": 0.26562358276643994,
    "y.wav": 0.2110204081632653,
    "y_Hard-Press.wav": 0.3403174603174603,
    "z.wav": 0.22439909297052155,
    "z_Hard-Press.wav": 0.2634920634920635,
}




# Functions for future application
def get_memory_usage(obj) -> str:
    """Returns the size of the object in memory

    Args:
        obj (any): The Python object you want to know the size of

    Returns:
        str: Returns the size in bytes, MB, GB, and TB respectively
    """

    size = asizeof.asizeof(obj)

    if size >= 10**12:
        return f"{size/10**12:.2f} TB"
    elif size >= 10**9:
        return f"{size/10**9:.2f} GB"
    elif size >= 10**6:
        return f"{size/10**6:.2f} MB"
    else:
        return f"{size} bytes"


def sort_dict(dictionary: dict) -> dict:
    """Sorts the given dictionary by its keys and returns the sorted dictionary.

    Args:
        dictionary (Dict): Dictionary to be sorted.

    Returns:
        Dict: Sorted dictionary.
    """

    return dict(sorted(dictionary.items(), key=lambda item: str(item[0])))


def get_wav_duration(filename: str) -> float:
    """Calculates the duration of a WAV file.

    Args:
        filename (str): Path to the WAV file.

    Returns:
        float: Duration of the WAV file.
    """

    with contextlib.closing(wave.open(filename, "r")) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration




# Main functions
def scan(input_string: str) -> List[str]:
    """Function to take an input string and returns a list of strings, where four consecutive spaces will be replaced by tabs.

    Args:
        input_string (str): The input string to be formatted.

    Returns:
        List[str]: A list of strings, where consecutive spaces have been replaced by tabs.

    Examples:
        >>> scan("Hello   World")
        ['Hello', ' ', ' ', ' ', 'World']
        >>> scan("    Indentation Example")
        ['    ', 'Indentation', ' Example']
    """

    return_list = list(input_string)

    # Initialize the new list to be returned
    # and counter to keep track of consecutive spaces
    temp_list = []
    space_buffer = []
    count = 0

    # Replaces four spaces with a tab
    for element in return_list:
        if element == " ":

            count += 1
            space_buffer.append(" ")

            # If the count reaches 4, append a tab space to the new list
            # and reset the counter
            if count == 4:
                temp_list.append("    ")
                count = 0
                space_buffer.clear()
        # If the element is not a space character, reset the counter
        # and append the element to the new list
        else:
            if space_buffer != []:
                temp_list.extend(space_buffer)
                space_buffer.clear()

            count = 0
            temp_list.append(element)
    return_list = temp_list

    return return_list


def toggle_vsc_settings(set_state: bool = None) -> None:
    """Toggles the values of:
        "editor.autoIndent",
        "editor.autoClosingBrackets",
        "editor.autoClosingQuotes",
        and "editor.acceptSuggestionOnEnter" in the VSC settings file.

    Args:
        set_state (bool, optional): The desired state to set the values to. If set to None,
        the function will toggle the values between full/none, languageDefined/never and on/off.
        If set to True, the values will be set to full, languageDefined, and on.
        If set to False, the values will be set to none, never, and off.
        Defaults to None.

    Raises:
        FileNotFoundError: If the settings file is not found in the expected location.
        KeyError: If the desired keys (editor.autoIndent and editor.autoClosingBrackets)
            are not present in the settings file.
    """

    # Get the user's home directory
    home_dir = os.path.expandvars("%APPDATA%")

    # Construct the path to the settings file
    settings_file = os.path.join(home_dir, "Code", "User", "settings.json")

    if not os.path.exists(settings_file):
        raise FileNotFoundError(f"VSC settings file does not exists at {settings_file}")

    # Load the settings file with utf-8 encoding
    with open(settings_file, "r", encoding="utf-8") as f:
        settings = json.load(f)

    # Check if the "editor.autoIndent" setting is present
    if "editor.autoIndent" not in settings:
        # Add the "editor.autoIndent" setting and set its value to "full"
        settings["editor.autoIndent"] = "full"
        print("'editor.autoIndent' setting not found, added with value 'full'")

    # Check if the "editor.autoClosingBrackets" setting is present
    if "editor.autoClosingBrackets" not in settings:
        # Add the "editor.autoClosingBrackets" setting and set its value to "languageDefined"
        settings["editor.autoClosingBrackets"] = "languageDefined"
        print("'editor.autoClosingBrackets' setting not found, added with value 'languageDefined'")

    # Check if the "editor.autoClosingQuotes" setting is present
    if "editor.autoClosingQuotes" not in settings:
        # Add the "editor.autoClosingQuotes" setting and set its value to "languageDefined"
        settings["editor.autoClosingQuotes"] = "languageDefined"
        print("'editor.autoClosingQuotes' setting not found, added with value 'languageDefined'")

    # Check if the "editor.acceptSuggestionOnEnter" setting is present
    if "editor.acceptSuggestionOnEnter" not in settings:
        # Add the "editor.acceptSuggestionOnEnter" setting and set its value to "on"
        settings["editor.acceptSuggestionOnEnter"] = "on"
        print("'editor.acceptSuggestionOnEnter' setting not found, added with value 'on'")

    # If both settings are present, toggle or set their values
    if (
        "editor.autoIndent" in settings
        and "editor.autoClosingBrackets" in settings
        and "editor.autoClosingQuotes" in settings
        and "editor.acceptSuggestionOnEnter" in settings
    ):
        if set_state is None:
            # Toggle the "editor.autoIndent" setting
            if settings["editor.autoIndent"] == "full":
                settings["editor.autoIndent"] = "none"
            else:
                settings["editor.autoIndent"] = "full"

            # Toggle the "editor.autoClosingBrackets" setting
            if settings["editor.autoClosingBrackets"] == "languageDefined":
                settings["editor.autoClosingBrackets"] = "never"
            else:
                settings["editor.autoClosingBrackets"] = "languageDefined"

            # Toggle the "editor.autoClosingQuotes" setting
            if settings["editor.autoClosingQuotes"] == "languageDefined":
                settings["editor.autoClosingQuotes"] = "never"
            else:
                settings["editor.autoClosingQuotes"] = "languageDefined"

            # Toggle the "editor.acceptSuggestionOnEnter" setting
            if settings["editor.acceptSuggestionOnEnter"] == "on":
                settings["editor.acceptSuggestionOnEnter"] = "off"
            else:
                settings["editor.acceptSuggestionOnEnter"] = "on"

        elif set_state:  # If True
            settings["editor.autoIndent"] = "full"
            settings["editor.autoClosingBrackets"] = "languageDefined"
            settings["editor.autoClosingQuotes"] = "languageDefined"
            settings["editor.acceptSuggestionOnEnter"] = "on"
        else:  # If False
            settings["editor.autoIndent"] = "none"
            settings["editor.autoClosingBrackets"] = "never"
            settings["editor.autoClosingQuotes"] = "never"
            settings["editor.acceptSuggestionOnEnter"] = "off"
    else:
        raise KeyError(
            "The desired keys (editor.autoIndent and editor.autoClosingBrackets) were not found in the settings file\nTry restarting the program?"
        )

    # Write the updated settings back to the file
    with open(settings_file, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def typing_hesitation(context: str = None) -> float:
    """DOCSTRING WILL BE ADDED ONCE FINISHED"""

    if context == None:
        start = 0.01
        end = 0.05

        random_number = random.uniform(start, end)

        return random_number

    if context == "Shift":
        start = 0.04
        end = 0.05

        random_number = random.uniform(start, end)

        return random_number


def clipboard_write(inputList: List[str]) -> List[Tuple[str, float]]:
    """Writes the given input list to the computer's clipboard and returns a list of tuples containing each character or space and the time it took to write.

    Args:
        inputList: List[str] - List of characters or spaces to be written to the computer's clipboard

    Returns:
        List[Tuple[str, float]] - A list of tuples where each tuple contains a character or space from inputList and the time it took to write

    """
    # turn off the code editors auto settings
    if TYPEWRITING_CODE:
        if CODE_EDITOR["Visual Studio Code"]:
            toggle_vsc_settings(False)

        "NOT IMPLEMENTED YET"
        # if CODE_EDITOR["Sublime Text"]:
        # pass
        # if CODE_EDITOR["Atom"]:
        # pass
        # if CODE_EDITOR["Notepad++"]:
        # pass

    timespan = []
    start_time = time.time()

    # iterate through each character in the input list
    for letter in inputList:
        # if the character is four spaces, simulate a tab press
        if letter == "    ":
            timespan.append((letter, time.time() - start_time))
            pyautogui.keyDown("tab")

        # if the character is not four spaces, write the character to the clipboard
        else:
            timespan.append((letter, time.time() - start_time))
            pyautogui.write(letter, typing_hesitation())

    # turn back on the code editors auto settings
    if TYPEWRITING_CODE:
        if CODE_EDITOR["Visual Studio Code"]:
            toggle_vsc_settings(True)

        "NOT IMPLEMENTED YET"
        # if CODE_EDITOR["Sublime Text"]:
        # pass
        # if CODE_EDITOR["Atom"]:
        # pass
        # if CODE_EDITOR["Notepad++"]:
        # pass

    return timespan


def create_audio_timestamps(timespan_list: List[Tuple[str, float]]) -> List[Tuple[str, Tuple[float, float]]]:
    """This function takes a list of tuples containing a key (string) and its corresponding timestamp (float) and
    returns a list of tuples, each containing the file path of the corresponding audio file and its start and end timestamps.

    Args:
        timespan_list (List[Tuple[str, float]]): A list of tuples where each tuple contains a key (string) and its corresponding timestamp (float)

    Returns:
        List[Tuple[str, Tuple[float, float]]]: A list of tuples where each tuple contains the file path of the corresponding audio file and its start and end timestamps.

    Example:
        >>> timespan_list = [("a", 1.0), ("b", 2.0), ("c", 3.0)]
        >>> create_audio_timestamps(timespan_list)
    Output:
        >>> [('./Audio/a.wav', (1.0, 1.0 + duration_of_a.wav)),
        >>> ('./Audio/b.wav', (2.0, 2.0 + duration_of_b.wav)),
        >>> ('./Audio/c.wav', (3.0, 3.0 + duration_of_c.wav))]
    """

    # list to store the tuples of audio file paths and start and end timestamps
    output_list = []

    # loop through the list of keys and their timestamps
    for key, timestamp in timespan_list:

        # boolean flags to check if the key is a shift key or non-character key
        is_shift_key = False
        is_noncharacter_key = False

        # check if the key is a shift key
        if key in SHIFT_KEYS.keys():
            is_shift_key = True
            sound_files = KEYS[SHIFT_KEYS[key]]
        else:
            sound_files = KEYS[key]

        # choose a random sound file if there are multiple files for the same key
        if type(sound_files) == tuple:
            file_path = random.choice(sound_files)
        else:
            file_path = sound_files

        # if the key is a shift key, add the corresponding shift key audio file to the output list
        if is_shift_key:
            backTime = typing_hesitation(context="Shift")
            shift_key_file = random.choice(KEYS["Special Keys"]["Shift"])

            output_list.append(
                (
                    rf"./Audio/{shift_key_file}",
                    (timestamp - backTime, timestamp - backTime + DURATION[shift_key_file]),
                )
            )

        # add the corresponding audio file to the output list
        output_list.append((rf"./Audio/{file_path}", (timestamp, timestamp + DURATION[file_path])))

    # return the output list
    return output_list


# NOTE: Function below doesn't work in Python 3.11 but is kept for reference
# import librosa
# def combine_audio_clips(clips_list: List[Tuple[str, Tuple[float, float]]], sr: int = 44100):
#     """
#     Combines multiple audio clips into a single audio track. The audio clips can overlap and play simultaneously
#     if the specified timestamps overlap.

#     Args:
#         clips_list (List[Tuple[str, Tuple[float, float]]]): A list of tuples where each tuple contains a filename and its start and end timestamps (in seconds).
#         sr (int, optional): The sampling rate to use when loading the audio clips. Defaults to 44100.
#     """

#     # Load audio clips into memory
#     clips = {}
#     for filename, timestamp in clips_list:
#         # Load the audio clip using librosa.load and store the audio signal in the clips dictionary
#         clips[filename] = librosa.load(filename, sr=sr)[0]

#     # Create a list of start and end timestamps for each clip
#     timestamps = [timestamp for _, timestamp in clips_list]

#     # Get the maximum end timestamp of all clips
#     max_end = max([timestamp[1] for timestamp in timestamps])

#     # Initialize the combined audio clip with zeros
#     combined_clip = np.zeros(int(sr * max_end))

#     # Add each clip to the combined audio clip at the specified start timestamp
#     for filename, timestamp in clips_list:
#         start, end = timestamp
#         start = int(sr * start)
#         end = int(sr * end)
#         clip = clips[filename]
#         # Check that the start and end timestamps are within the length of the combined audio clip
#         if (start >= 0) & (end <= len(combined_clip)):
#             # Add the clip to the combined audio clip at the specified start and end timestamps
#             combined_clip[start:end] += clip

#     # Write the combined audio clip to a file
#     d = datetime.now()
#     sf.write(f"./Output/Keyboard Generation {d.strftime(r'%Y.%m.%d - %I.%M.%S')}.wav", combined_clip, sr)


def combine_audio_clips(clips_list: List[Tuple[str, Tuple[float, float]]], sr: int = 44100):
    """
    Combines multiple audio clips into a single audio track. The audio clips can overlap and play simultaneously
    if the specified timestamps overlap.

    Args:
        clips_list (List[Tuple[str, Tuple[float, float]]]): A list of tuples where each tuple contains a filename and its start and end timestamps (in seconds).
        sr (int, optional): The sampling rate to use when loading the audio clips. Defaults to 44100.
    """

    # Load audio clips into memory
    clips = {}
    for filename, timestamp in clips_list:
        # Load the audio clip using soundfile. read and store the audio signal in the clips dictionary
        audio, _ = sf.read(filename)
        clips[filename] = audio

    # Create a list of start and end timestamps for each clip
    timestamps = [timestamp for _, timestamp in clips_list]

    # Get the maximum end timestamp of all clips
    max_end = max([timestamp[1] for timestamp in timestamps])

    # Initialize the combined audio clip with zeros
    combined_clip = [0] * int(sr * max_end)

    # Add each clip to the combined audio clip at the specified start timestamp
    for filename, timestamp in clips_list:
        start, end = timestamp
        start_idx = int(sr * start)
        end_idx = int(sr * end)
        clip = clips[filename]
        # Check that the start and end timestamps are within the length of the combined audio clip
        if (start_idx >= 0) & (end_idx <= len(combined_clip)):
            # Add the clip to the combined audio clip at the specified start and end timestamps
            combined_clip[start_idx:end_idx] = [x + y for x, y in zip(combined_clip[start_idx:end_idx], clip)]

    # Write the combined audio clip to a file
    d = datetime.now()
    sf.write(f"./Output/Keyboard - {d.strftime(r'%Y.%m.%d - %I.%M.%S')}.wav", combined_clip, sr)

# Opens the write file
with open(r"./Text_to_Write.txt", "r") as text_to_write_file:
    workString = text_to_write_file.read()


print("MOVE MOUSE TO CORNER OF SCREEN AT ANY POINT TO STOP THE PROGRAM")
# Gives time to select the area to type in
for i in range(5):
    print(f"\rTime: {5-i}", end="")
    time.sleep(1)

combine_audio_clips(create_audio_timestamps(clipboard_write(scan(workString))))