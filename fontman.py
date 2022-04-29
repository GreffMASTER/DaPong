# Font Manager (fontman) Luke Lasok 2022
# This module contains fonts and additional functions involving text related actions.

fonts = {}  # Font list

def drawFps(font, fps):      # Creates text surface with FPS counter and color depenfing on FPS value
    color = (255, 255, 255)
    if fps > 40:
        color = (0, 128, 0)   # Green text
    if fps <= 40:
        color = (128, 128, 0) # Yello text
    if fps <= 20:
        color = (128, 0, 0)   # Red text
    return font.render("FPS:" + str(int(fps)), True, color)  # Create text surface

# EOF
