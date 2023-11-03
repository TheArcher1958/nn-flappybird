import pygame
from navigation import Navigation


def main():
    
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.music.load("Waterflame - Glorious Morning 2.mp3")
    pygame.mixer.music.play(-1, fade_ms=3000)
    pygame.display.set_caption("Flapping Birds")

    nav = Navigation()

 
    while nav.current_screen.running: 

        nav.current_screen.screen_loop()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()