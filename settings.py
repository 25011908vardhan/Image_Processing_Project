import pygame

WINDOW_NAME = "HAND GESTURE PROJECT IMAGE PROCESSING"
GAME_TITLE = "INTERACTIVE WORLD"

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700

FPS = 90
DRAW_FPS = True

# sizes
BUTTONS_SIZES = (520, 90)
HAND_SIZE = 200
HAND_HITBOX_SIZE = (60, 80)


# drawing
DRAW_HITBOX = False # will draw all the hitbox

# animation
ANIMATION_SPEED = 0.08 # the frame of the insects will change every X sec

# difficulty
GAME_DURATION = 60 # the game will last X sec


# colors
COLORS = {"title": (70, 129, 244), "score": (70, 129, 244), "timer": (221, 121, 115),
            "buttons": {"default": (90, 219, 181), "second":  (51, 178, 73 ),
                        "text": (255, 255, 255), "shadow": (51, 178, 73,0.1)}} # second is the color when the mouse is on the button

# sounds / music
MUSIC_VOLUME = 0.16 # value between 0 and 1
SOUNDS_VOLUME = 1

# fonts
pygame.font.init()
FONTS = {}
FONTS["small"] = pygame.font.Font(None, 40)
FONTS["medium"] = pygame.font.Font(None, 72)
FONTS["big"] = pygame.font.Font(None, 120)
