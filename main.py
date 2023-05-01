import time
from utility.window_capture import window_capture
import pygame


ppt = window_capture("PuyoPuyoTetris")

pygame.init()
screen = pygame.display.set_mode((480,270))
pygame.display.set_caption("Test")

while True:
    screenshot_array = ppt.get_screenshot()
    print(screenshot_array.shape)
    surf = pygame.surfarray.make_surface(screenshot_array)

    screen.blit(surf, (0,0))

    pygame.display.update()

    time.sleep(1/60)