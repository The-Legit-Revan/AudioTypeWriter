# AudioTypeWriter - The Automatic Keyboard Typing and Audio Generator

AudioTypeWriter is a Python script that helps content creators and streamers automate typing large blocks of text or code while looking and sounding realistic. In the current state of this script, you can type text on the screen live and you will get a generated audio file of the keyboard typing that realistically matches the sound and the speed of the text in your video.

In its current state, the audio file must be added in post-production, but it is in the works to make the typing sound play live along with the automatic typing.

## Features

- Automatic setup.
- All required modules are installed in a virtual environment, so the script will not modify your site packages in case you are a programmer.
- Easy to use - simply paste your text into the "Text_to_Write.txt" file and run the start.bat file.
- The program gives you a 5-second countdown before it begins typing, so you have time to prepare.
- You can stop the automatic typing at any time by moving your mouse to the end of any corner of the screen.

## Set Up

Before setting up or using the script, ensure that you have the latest version of [Python](https://www.python.org/downloads/) installed on your computer.

Because Python virtual environments do not transfer well between computers the script is shipped with a setup.bat file. The setup.bat will automatically:

1. Create a Python virtual environment named `'venv'`.
2. Activate the newly created virtual environment.
3. Install all required modules listed in `requirements.txt` via `pip`.
4. Remove the requirements.txt and setup.bat files, as they are no longer needed.

After completing the above steps, your script will be fully configured and ready to use.

## How to Use

All required modules are installed in a Python virtual environment. All you have to do is follow these steps:

1. Input your desired text into the "Text_to_Write.txt" file, and save it. 
2. Launch the program by running the start.bat file, which will automatically activate the Python virtual environment and initiate the typing process.
3. You will see a 5-second countdown before the typing begins. Make sure to select the field you want to type into during this time. 
4. To halt the typing process at any point, simply move your mouse to any corner of the screen. *Note that doing so will terminate the program and prevent the creation of an audio file.*
5. Once the typing is complete, locate your audio file in the `Output` folder. Each file will be time-stamped to simplify the identification process.
6. Composite the audio to the video in the video editing software of your choice.

### Code Editors

Most common code editors today have functionality to aid in code development, however, the following can conflict with the automation of the program: 

- Automatic Indentation.
- Automatic Closing Brackets.
- Automatic Closing Quotes.
- Accepted Suggestions on Enter or Tab Key Press.

Because the program will input the key presses in the identical order of what is inside of the `Text_to_Write.txt` file, any automatic formatting can lead to too many indentations (*which is vital to Python functionality*) and incorrect syntax accordingly.

To combat this issue I have added a feature that will allow you to typewrite into code editors (*only VSC supported at this time*) by editing the settings file of the code editor to temporarily disable the automatic format and suggestion functionality. However code editor mode is disabled by default because if the settings file does not exist on your computer, it will cause the program to crash.

### How to enable code editor mode

To allow the program to disable all the required automatic functionality you will need to do the following to edit a few lines of the code.

1. Open the main.py file in your code editor of choice. If you don't have a code editor notepad will work just fine.

2. Locate the following code segment at the top of the script:
    ```py
    TYPEWRITING_CODE = False

    CODE_EDITOR = {
        "Visual Studio Code": False,
        # "Sublime Text"      : "NOT IMPLEMENTED YET",
        # "Atom"              : "NOT IMPLEMENTED YET",
        # "Notepad++"         : "NOT IMPLEMENTED YET"
    }
    ``` 
3. Change the `TYPEWRITING_CODE` veritable from `False` to `True` to enable the program to search for a settings file.
   
4. Find the code editor you want to use inside of the `CODE_EDITOR` dictionary, and change the respective value to `True`.
   - **NOTE:**
     <!-- - **It is highly recommended that you only have one code editor set to ```True``` at a time!** -->
      - *If the selected code editor does not have a settings file on your computer, the program will crash.*
      - *If the selected code editor does not have the settings file installed at the default location, the program will crash.*

It should be noted that the program is designed to find existing values in the settings file, and if they exist toggle them to their respective *'off'* values, but if they are not found it will add them, and then it will toggle them all back to on once it is done.

This means that if you have some of these values set to off already, they will be toggled back to their respective *'on'* values. Functionality is in Development to make it test for these already existing values, and make it leave them the way it was before you ran the code, but it should be noted that ***THIS IS NOT IMPLEMENTED YET!***

## Features in Development

- More keyboard sound variations per key.
- More keyboard sound types, Mechanical-Plastic-Gaming is the only one available right now.
- Support for Sublime Text, Atom, and Notepad++ in code editor mode.
- Support for settings files that are not installed in default locations in code editor mode.
- Dynamic typing hesitation based on situational context.
  - Examples:
    1. Before typing out a really long, hard, or uncommon word.
    2. When typing non-English words.
       - *Support will be considered to add the same functionality to languages other than English.*
    3. If Typing too many similar words back to back.
    4. When using symbols that require one hand to hold shift and the other hand to leave resting position.
- Dynamic typing hesitation and veritable completion for code editor mode.
  - Example:
    - Hesitation to show contemplation when creating list comprehension (*Python*).
    - Hesitation to show contemplation when using the ternary operator (*Python*).
    - Imitation of tab autocompletion for the following:
      - Variables defined in a earlier part of the code.
      - Built-in Class Methods (*Python*).
      - Methods of a user made class defined in a earlier part of the code (*Python*).
- Dynamic numeric context analysis to simulate usage of the numpad.

# Terms of Use

Pursuant to the terms and conditions of this agreement, the User is hereby granted a non-exclusive, non-transferable license to use the audio files and code included in the program solely for the purpose of using the Program as intended. The User acknowledges and agrees that the audio files and other assets included in the Program are proprietary to the Program's owners and are protected by copyright laws. Any use of the audio files or assets outside of the Program is strictly prohibited and constitutes a violation of this agreement. Any unauthorized use of the audio files or assets may result in immediate termination of this license and may subject the User to civil and/or criminal liability.

## By using the program, you agree to the following terms and conditions:

- Ownership of Generated Content: Any content created using the program is the property of the user and the user retains all copyrights.

- Use of Audio Files and Other Assets: All audio files and other assets in the program are free to use solely as they are intended in the program. Any sharing outside of the program as a whole or reuse for another project is strictly prohibited.

- Prohibited Use of Generated Content: Any generation of content with the intent of splicing out the original audio files is forbidden and will not be considered the property of the user.

- Modification of the Program: Modification of the program is allowed for personal use only, but modification or extraction of the program's code is not allowed to be shared or posted by the user.

- Disclaimer of Warranty: The designers of the program and all content within give no guarantee or warranty that the program will work correctly or that updates to the program may or may not break or remove current content or features of the program. The designers also have no liability for any damage done to the user's system due to modifications made to the program by the user.