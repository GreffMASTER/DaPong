# Audio Manager (audioman) Luke Lasok 2022
# This module contains all the game sounds. It has a check if the audio mixer was initilized. If not, the game will not load the sounds and will not play them.

from pygame import mixer
import os
print("Adding Audio Manager...")

sfxList = {}

isaudio = False
mixer.init()
if mixer.get_init() != None:
    isaudio = True
    print("Mixer initiated")

if isaudio:
    sfxList = {
        "clickSfx":   mixer.Sound(os.path.join("sounds", "click.wav")),     # Load click sound effect
        "scoreSfx":   mixer.Sound(os.path.join("sounds", "score.wav")),     # Load score sound effect
        "wallBncSfx": mixer.Sound(os.path.join("sounds", "wallBnc.wav")),   # Load wall bounce sound effect
        "paddBncSfx": mixer.Sound(os.path.join("sounds", "paddBnc.wav"))    # Load paddle bounce sound effect
    }

def play(name):
    if isaudio:
        sfxList[name].play()
