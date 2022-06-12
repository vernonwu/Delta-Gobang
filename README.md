# DeltaGobang Documentation

## Introduction

DeltaGobang is an entry-level chess software that provides several basic functions centered around the game of Gobang.



## Versions

**Current Version**: Beta 1.0

**AI Profile**:  Alex, unisex. Its name is designed with tribute to Amazon's voice assistant Alexa (also being the name of the female character in the famous sandbox game MINECRAFT), it is considered to be affectionate.

**Rule Variations:** 

Currently the basic gobang rule with no forbidden moves is used, and five pieces in a row is sufficient as a win.



## Quick Start

Method 1: Simply double-click the .exe file of a preffered version to run it directly after making sure it is under the same root as the two folders "**image**" and "**music**".

Method 2: To interpret the sourcecode, see requirements of needed libraries in requirements.txt. Install with

```bash
pip install -r requirements.txt
```



## Basic Functions

While in game, press F1 to mute.

### PVP



1. Press the "Human versus Human" button at the top-left of the main menu.

2. Hover over the position where you want to drop the chess and **left click** on the mouse to perform a chess move.

3. At the end of the game, you can **save/return to** the main menu by clicking on the game as desired.

   

### PVE



1. Press the "Human versus Machines" button at the top-left of the main menu.

2. Choose Turns. 

3. It usually takes AI 5-10 seconds to figure out their moves, so please be patient!

4. At the end of the game, you can save/return to the main menu by clicking on the game as desired.

   

### Mode Switch

The game mode can be switched at any time during the game (PVE/PVP).



### Play Chess Records

Click on "Load Game" to review the saved previous games. External games are **not** currently supported.

Playback is **controlled** by "step forward/step back" or the arrow keys "left/right"。

Try/AI recommendations are also available during playback.



## Test Results

For the test in WIN11, python = 3.10.3:

| Test item                        | Running Time       |
| -------------------------------- | ------------------ |
| AI Thinking Time (Opening phase) | $6179 \pm 1000$ ms |
| AI Thinking Time (Middle game)   | $8292 \pm 1000$ ms |
| Maximum TIme Recorded            | $9446$ ms          |



## Credits

**Inspiration for the UI Design：**

https://download.csdn.net/download/qq_36408085/10694129

@Author: CSU信息院16张扬 @Email: csuzhangyang@gmai.com  or csuzhangyang@qq.com

