from score import Score
import random
import pygame
from pipe import Pipe, BluePipe
from math import ceil
from bird import Bird
from gamescreen import GameScreen
from button import Button
from overlay import Overlay
from constants import WIDTH, HEIGHT, CYAN, NewFont


class Game(GameScreen):
    frame_count = 0
    game_state = "play"
    pipes_sprite = pygame.sprite.Group()
    bird_sprite = pygame.sprite.GroupSingle()
    
    active = True
    paused = False
    pause_overlay = Overlay()
    

    def __init__(self, nav, bird_type) -> None:
        self.nav = nav
        self.score = Score()
        
        self.gamefont = pygame.font.SysFont('Comic Sans MS', 30)
        self.bg = Background(WIDTH, HEIGHT)
        self.clock = pygame.time.Clock()
        

        self.bird = Bird(self.screen, bird_type)
        self.bird_sprite.add(self.bird)

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.crash_sound = pygame.mixer.Sound('audio/crash.mp3')
        self.jump_sound.set_volume(0.5)
        self.crash_sound.set_volume(0.5)

        self.death_screen = pygame.Surface((WIDTH / 3 * 2, HEIGHT / 3 * 2))
        self.death_screen_rect = pygame.Rect(WIDTH / 6, HEIGHT / 6, WIDTH / 3 * 2, HEIGHT / 3 * 2)
        self.death_screen.fill(CYAN)

        self.game_over_text = NewFont('sitkaheading', 60, 'Game Over')
        self.game_paused_text = NewFont('sitkaheading', 60, 'Game Paused')
        self.play_button = Button("Play Again", WIDTH/2 + Button.width / 6, HEIGHT/3*2)
        self.home_button = Button("Home", WIDTH/2 - Button.width - Button.width / 6, HEIGHT/3*2)

        self.sound_toggle = PauseButton(WIDTH-75, 25, 50, 50, ["images/sound_on.png","images/sound_off.png"])
        
    def reset_game(self):
        self.pipes_sprite.empty()
        self.score.reset()
        self.bird.rect.y = 50
        self.bird.hit = False
        self.active = True
        self.paused = False

    def screen_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.active == True:
                    if self.active:
                        self.jump_sound.play() if self.sound_toggle.image == self.sound_toggle.off else ""
                        self.bird.jump()
                if event.key == pygame.K_ESCAPE and not self.bird.hit:
                        self.paused = False if self.paused else True
                        self.active = False if self.active else True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.mouse_over():
                    if self.active == False:
                        self.reset_game()
                if self.home_button.mouse_over():
                    self.reset_game()
                    self.nav.navigate('home')
                if self.sound_toggle.mouse_over():
                    self.sound_toggle.image = self.sound_toggle.on if self.sound_toggle.image == self.sound_toggle.off else self.sound_toggle.off
                    pygame.mixer.music.set_volume(0) if self.sound_toggle.image == self.sound_toggle.on else pygame.mixer.music.set_volume(1)


        self.bg.update(self.screen) 
        self.bg.scroll_frame() if self.active else ""

        score_text = self.gamefont.render(f"Score: {str(self.score.normalize())}", False, (0, 0, 0))
        

        if(self.frame_count % 120 == 0):
            if self.active == True:
                self.create_pipes()
           

        for pipe in list(self.pipes_sprite):
            if(pygame.sprite.spritecollide(self.bird, self.pipes_sprite, 0)):
                self.crash_sound.play() if self.active and self.sound_toggle.image == self.sound_toggle.off else ""
                self.active = False
                self.bird.hit = True
                
            if(pipe.rect.x < 0 - Pipe.width):
                self.remove_pipe(pipe)
                self.score.increase()

        if(self.active == True):
            self.pipes_sprite.update()

        self.pipes_sprite.draw(self.screen)
        self.bird_sprite.update() if not self.paused else ""
        self.bird_sprite.draw(self.screen)
                
        self.screen.blit(score_text, (100,50))
        
        if self.paused:
            self.screen.blit(self.pause_overlay.bg, self.pause_overlay.rect)
            self.screen.blit(self.death_screen, self.death_screen_rect)
            self.screen.blit(self.game_paused_text.render_text('Game Paused'), (self.game_paused_text.horizontal_middle(), HEIGHT/3))  
            self.home_button.draw(self.screen)
            self.play_button.draw(self.screen)

        if not self.active and not self.paused:
            self.screen.blit(self.pause_overlay.bg, self.pause_overlay.rect)
            self.screen.blit(self.death_screen, self.death_screen_rect)
            self.screen.blit(self.game_over_text.render_text('Game Over'), (self.game_over_text.horizontal_middle(), HEIGHT/3))  
            self.home_button.draw(self.screen)
            self.play_button.draw(self.screen)

        self.screen.blit(self.sound_toggle.image, (self.sound_toggle.x, self.sound_toggle.y)) 

        self.frame_count += 1
        self.clock.tick(60)


    def create_pipes(self):
        x = self.screen.get_width()
        y = self.screen.get_height()
        
        random_space_height = random.randint(150,230) # random int pixel space for bird to go through
        space_top = int(random.randint(50, y - 50 - random_space_height)) # choose a random value from y 50 to screen height - 110 
        space_bottom = space_top + random_space_height
        direction = random.choice([1,-1])
        if random.randint(0,4) == 0:
            self.pipes_sprite.add(BluePipe(x, 0, Pipe.width, space_top, random_space_height, direction), BluePipe(x, space_bottom, Pipe.width, y - space_bottom, random_space_height, direction))
        else:
            self.pipes_sprite.add(Pipe(x, 0, Pipe.width, space_top), Pipe(x, space_bottom, Pipe.width, y - space_bottom))

    def remove_pipe(self, pipe):
        self.pipes_sprite.remove(pipe)

class Background:

    def __init__(self, width, height) -> None:
        bg = pygame.image.load("images/bg.png").convert() 
        self.bg = pygame.transform.scale(bg, (width, height))
        
        self.scroll = 0
        self.tiles = ceil(width / bg.get_width()) + 1

    def update(self, screen):
        i = 0
        while(i < self.tiles): 
            screen.blit(self.bg, (self.bg.get_width() * i + self.scroll, 0)) 
            i += 1
       

    def scroll_frame(self):
        self.scroll -= 2
    
        if abs(self.scroll) > self.bg.get_width(): 
            self.scroll = 0

class PauseButton(Button):
    def __init__(self, x, y, width, height, images: []) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        off = pygame.image.load(images[0]).convert_alpha()
        self.off = pygame.transform.scale(off, (width, height))
        on = pygame.image.load(images[1]).convert_alpha()
        self.on = pygame.transform.scale(on, (width, height))
        self.image = self.off
        self.active = False
        self.rect = pygame.Rect(x, y, width, height)
        self.bg = pygame.Surface([width, height])
