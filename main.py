import pygame
import sys
from engine.game import Game


def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
    pygame.display.set_caption("Summoned To Another World and Became A Hero")
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()