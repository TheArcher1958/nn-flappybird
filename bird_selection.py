from gamescreen import GameScreen
from constants import NewFont
from button import Button
import pygame
from animation import Sprite_Collection
from constants import WIDTH, HEIGHT

class BirdSelection(GameScreen):
    
    def __init__(self, nav) -> None:
        self.nav = nav
        self.heading = NewFont('sitkaheading', 60, 'Choose Your Player!')

        self.button = Button("Play", 100, 500)

        self.bird_buttons = []
        self.birds, self.types = Sprite_Collection.get_all_birds()
        for count, bird in enumerate(self.birds):
            self.bird_buttons.append(BirdButton(100 + count * 150, 200, 128, 100, bird))
        # self.rects = [pygame.Rect(100 + count * 150, 200, 128, 100) for count in range(len(self.birds))]
        

  

    def screen_loop(self):
        for ev in pygame.event.get():  
          
            if ev.type == pygame.QUIT:  
                self.running = False
                
            if ev.type == pygame.MOUSEBUTTONDOWN:  
                
                if self.button.mouse_over():
                    self.nav.navigate('game')
            
                for count, bird_button in enumerate(self.bird_buttons):
                    if bird_button.mouse_over():
                        self.nav.navigate('game', self.types[count])


        
        for count, bird_button in enumerate(self.bird_buttons):
            if bird_button.mouse_over():
                self.bird_buttons[count].bg.set_alpha(255)
            else:
                self.bird_buttons[count].bg.set_alpha(0)
                    
        self.screen.fill((84,194,204))  
        
        for count, bird_button in enumerate(self.bird_buttons):
            # print(count, bird)
            self.screen.blit(self.bird_buttons[count].bg, self.bird_buttons[count].rect)
            self.screen.blit(self.bird_buttons[count].bird, self.bird_buttons[count].rect)
            
        # self.button.draw(self.screen)

        # self.screen.blit(self.heading.render_text('Flappy Birds'), (self.heading.horizontal_middle(), HEIGHT/6))  

class BirdButton(Button):
    def __init__(self, x, y, width, height, bird) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bird = bird
        self.rect = pygame.Rect(x, y, width, height)
        self.bg = pygame.Surface([width, height])
        self.bg.fill("red")

        # super().__init__(text, x, y)